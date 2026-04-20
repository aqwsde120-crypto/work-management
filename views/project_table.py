# pages/project_table.py
import streamlit as st
import pandas as pd
import io
from datetime import datetime
from config import PARTS, CATEGORIES, STATUSES

def show_project_table(df, show_archived=False):
    """프로젝트 테이블 화면 (파트 컬럼 포함)"""
    st.title("📋 프로젝트 테이블")
    st.markdown("---")
    
    # 필터 영역
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        search_term = st.text_input("🔍 프로젝트명 또는 업무 제목 검색", "")
    with col2:
        team_members = st.session_state.team_members['name'].tolist() if 'team_members' in st.session_state else []
        selected_assignees = st.multiselect("👥 담당자 필터", options=team_members)
    with col3:
        statuses = df['status'].unique().tolist()
        selected_status = st.multiselect("📊 상태 필터", options=statuses)
    with col4:
        categories = df['category'].unique().tolist()
        selected_category = st.multiselect("🗂️ 분류 필터", options=categories)
    with col5:
        parts = df['part'].unique().tolist() if 'part' in df.columns else PARTS
        selected_part = st.multiselect("📌 파트 필터", options=parts)
    
    # 필터 적용
    filtered_df = df.copy()
    if search_term:
        filtered_df = filtered_df[
            filtered_df['project_name'].str.contains(search_term, case=False, na=False) |
            filtered_df['title'].str.contains(search_term, case=False, na=False)
        ]
    if selected_assignees:
        filtered_df = filtered_df[
            filtered_df['assignee'].apply(
                lambda x: any(person in str(x) for person in selected_assignees) if pd.notna(x) else False
            )
        ]
    if selected_status:
        filtered_df = filtered_df[filtered_df['status'].isin(selected_status)]
    if selected_category:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_category)]
    if selected_part:
        filtered_df = filtered_df[filtered_df['part'].isin(selected_part)]
    
    st.markdown(f"**총 {len(filtered_df)}개 프로젝트**")
    
    # 테이블 표시
    display_df = filtered_df.copy()
    if not display_df.empty:
        display_df['deadline'] = pd.to_datetime(display_df['deadline']).dt.strftime('%Y-%m-%d')
    
    st.dataframe(
        display_df[['id', 'part', 'project_name', 'title', 'assignee', 'category', 'status',
                    'planned_progress', 'actual_progress', 'completion_rate', 'deadline']],
        column_config={
            "id": st.column_config.TextColumn("ID", width="small", disabled=True),
            "part": st.column_config.TextColumn("파트", width="small"),
            "project_name": st.column_config.TextColumn("프로젝트명", width="medium"),
            "title": st.column_config.TextColumn("업무 제목", width="large"),
            "assignee": st.column_config.TextColumn("담당자", width="medium"),
            "category": st.column_config.TextColumn("분류", width="small"),
            "status": st.column_config.TextColumn("진행 현황", width="medium"),
            "planned_progress": st.column_config.ProgressColumn("계획 일정", format="%d%%"),
            "actual_progress": st.column_config.ProgressColumn("실제 진행", format="%d%%"),
            "completion_rate": st.column_config.ProgressColumn("진척률", format="%d%%"),
            "deadline": st.column_config.TextColumn("마감일"),
        },
        hide_index=True,
        use_container_width=True,
        height=600
    )

    # ==================== 프로젝트 수정 ====================
    st.markdown("---")
    st.subheader("✏️ 프로젝트 수정")
    if len(filtered_df) > 0:
        project_to_edit = st.selectbox(
            "수정할 프로젝트 선택",
            options=filtered_df['id'].tolist(),
            format_func=lambda x: f"[{filtered_df[filtered_df['id']==x]['part'].iloc[0]}] "
                                 f"{filtered_df[filtered_df['id']==x]['project_name'].iloc[0]} - "
                                 f"{filtered_df[filtered_df['id']==x]['title'].iloc[0]}"
        )
        
        if project_to_edit:
            task = filtered_df[filtered_df['id'] == project_to_edit].iloc[0]
            
            with st.form("edit_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_project_name = st.text_input("프로젝트명", value=task['project_name'])
                    new_title = st.text_input("업무 제목", value=task['title'])
                    new_assignee = st.text_input("담당자", value=task['assignee'])
                    new_part = st.selectbox("파트", options=PARTS, 
                                          index=PARTS.index(task.get('part', '미지정')))
                    new_category = st.selectbox("분류", options=CATEGORIES, 
                                              index=CATEGORIES.index(task['category']) if task['category'] in CATEGORIES else 0)
                
                with col2:
                    new_status = st.selectbox("진행 현황", options=STATUSES, 
                                            index=STATUSES.index(task['status']) if task['status'] in STATUSES else 0)
                    new_planned = st.slider("계획 일정 (%)", 0, 100, int(task['planned_progress']))
                    new_actual = st.slider("실제 진행 (%)", 0, 100, int(task['actual_progress']))
                    new_completion = st.slider("프로젝트 진척률 (%)", 0, 100, int(task['completion_rate']))
                    new_deadline = st.date_input("마감일", value=pd.to_datetime(task['deadline']))
                
                new_description = st.text_area("업무 설명", value=task.get('description') or "")
                
                submitted = st.form_submit_button("💾 수정 내용 저장")
                
                if submitted:
                    conn = st.session_state.db_conn
                    c = conn.cursor()
                    c.execute('''
                        UPDATE tasks 
                        SET project_name = ?, title = ?, assignee = ?, category = ?, 
                            status = ?, planned_progress = ?, actual_progress = ?, 
                            completion_rate = ?, deadline = ?, description = ?, part = ?
                        WHERE id = ?
                    ''', (new_project_name, new_title, new_assignee, new_category, new_status,
                          new_planned, new_actual, new_completion, new_deadline.strftime('%Y-%m-%d'),
                          new_description, new_part, project_to_edit))
                    conn.commit()
                    st.success("✅ 수정이 저장되었습니다!")
                    st.rerun()

    # 아카이브 관리
    st.markdown("---")
    st.subheader("🗄️ 아카이브 관리")
    all_df = st.session_state.load_tasks_func(show_archived=True)
    if len(all_df) > 0:
        selected_ids = st.multiselect(
            "보관하거나 보관 해제할 프로젝트 선택",
            options=all_df['id'].tolist(),
            format_func=lambda x: f"{'🗄️ ' if all_df[all_df['id']==x]['archived'].iloc[0]==1 else '✅ '}"
                                 f"[{all_df[all_df['id']==x]['part'].iloc[0]}] "
                                 f"{all_df[all_df['id']==x]['project_name'].iloc[0]} - "
                                 f"{all_df[all_df['id']==x]['title'].iloc[0]}"
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🗄️ 선택한 프로젝트 보관하기", use_container_width=True):
                if selected_ids:
                    to_archive = [i for i in selected_ids if all_df[all_df['id']==i]['archived'].iloc[0] == 0]
                    if to_archive:
                        conn = st.session_state.db_conn
                        c = conn.cursor()
                        c.executemany("UPDATE tasks SET archived = 1 WHERE id = ?", [(i,) for i in to_archive])
                        conn.commit()
                        st.success(f"{len(to_archive)}개 프로젝트를 보관했습니다.")
                        st.rerun()
        with col_b:
            if st.button("🔓 선택한 프로젝트 보관 해제하기", use_container_width=True):
                if selected_ids:
                    to_unarchive = [i for i in selected_ids if all_df[all_df['id']==i]['archived'].iloc[0] == 1]
                    if to_unarchive:
                        conn = st.session_state.db_conn
                        c = conn.cursor()
                        c.executemany("UPDATE tasks SET archived = 0 WHERE id = ?", [(i,) for i in to_unarchive])
                        conn.commit()
                        st.success(f"{len(to_unarchive)}개 프로젝트를 보관 해제했습니다.")
                        st.rerun()

    # Excel 다운로드
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📥 Excel 다운로드"):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            filtered_df.to_excel(writer, index=False)
        output.seek(0)
        st.download_button(
            label="📥 다운로드 시작",
            data=output,
            file_name=f"프로젝트_관리_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
