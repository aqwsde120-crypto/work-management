# pages/project_table.py
import streamlit as st
import pandas as pd
import io
import time
from datetime import datetime
from config import PARTS, CATEGORIES, STATUSES
from database import load_team_members, load_tasks

def show_project_table(df, show_archived=False):
    st.title("📋 프로젝트 테이블")
    st.markdown("---")
    
    # 팀원 목록
    try:
        team_df = load_team_members()
        team_members = team_df['name'].tolist() if not team_df.empty and 'name' in team_df.columns else []
    except:
        team_members = []
    
    # 필터
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        search_term = st.text_input("🔍 검색", "")
    with col2:
        selected_assignees = st.multiselect("👥 담당자", options=team_members)
    with col3:
        statuses = df['status'].unique().tolist() if 'status' in df.columns and not df.empty else STATUSES
        selected_status = st.multiselect("📊 상태", options=statuses)
    with col4:
        categories = df['category'].unique().tolist() if 'category' in df.columns and not df.empty else CATEGORIES
        selected_category = st.multiselect("🗂️ 분류", options=categories)
    with col5:
        parts = df['part'].unique().tolist() if 'part' in df.columns and not df.empty else PARTS
        selected_part = st.multiselect("📌 파트", options=parts)
    
    filtered_df = df.copy()
    if search_term and not filtered_df.empty:
        filtered_df = filtered_df[
            filtered_df.get('project_name', pd.Series()).str.contains(search_term, case=False, na=False) |
            filtered_df.get('title', pd.Series()).str.contains(search_term, case=False, na=False)
        ]
    if selected_assignees and not filtered_df.empty and 'assignee' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['assignee'].apply(lambda x: any(person in str(x) for person in selected_assignees))]
    if selected_status and not filtered_df.empty and 'status' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['status'].isin(selected_status)]
    if selected_category and not filtered_df.empty and 'category' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_category)]
    if selected_part and not filtered_df.empty and 'part' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['part'].isin(selected_part)]
    
    st.markdown(f"**총 {len(filtered_df)}개 프로젝트**")
    
    if not filtered_df.empty:
        display_df = filtered_df.copy()
        if 'deadline' in display_df.columns:
            display_df['deadline'] = pd.to_datetime(display_df['deadline'], errors='coerce').dt.strftime('%Y-%m-%d')
        
        st.dataframe(
            display_df[['id', 'part', 'project_name', 'title', 'assignee', 'category', 'status',
                        'planned_progress', 'actual_progress', 'completion_rate', 'deadline']],
            column_config={
                "id": st.column_config.TextColumn("ID", disabled=True),
                "part": st.column_config.TextColumn("파트"),
                "project_name": st.column_config.TextColumn("프로젝트명"),
                "title": st.column_config.TextColumn("업무 제목"),
                "assignee": st.column_config.TextColumn("담당자"),
                "category": st.column_config.TextColumn("분류"),
                "status": st.column_config.TextColumn("진행 현황"),
                "planned_progress": st.column_config.ProgressColumn("계획 일정", format="%d%%"),
                "actual_progress": st.column_config.ProgressColumn("실제 진행", format="%d%%"),
                "completion_rate": st.column_config.ProgressColumn("진척률", format="%d%%"),
                "deadline": st.column_config.TextColumn("마감일"),
            },
            hide_index=True,
            use_container_width=True,
            height=650
        )

    # ==================== 프로젝트 수정 / 삭제 ====================
    st.markdown("---")
    st.subheader("✏️ 프로젝트 수정 / 삭제")
    
    if not filtered_df.empty:
        project_to_edit = st.selectbox(
            "수정하거나 삭제할 프로젝트 선택",
            options=filtered_df['id'].tolist(),
            format_func=lambda x: f"[{filtered_df[filtered_df['id']==x].get('part', pd.Series(['미지정'])).iloc[0]}] "
                                 f"{filtered_df[filtered_df['id']==x]['project_name'].iloc[0]}"
        )
        
        tab1, tab2 = st.tabs(["📝 수정하기", "🗑️ 삭제하기"])
        
        with tab1:
            with st.form("edit_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_project_name = st.text_input("프로젝트명", value=filtered_df[filtered_df['id']==project_to_edit]['project_name'].iloc[0])
                    new_title = st.text_input("업무 제목", value=filtered_df[filtered_df['id']==project_to_edit]['title'].iloc[0])
                    new_assignee = st.text_input("담당자", value=filtered_df[filtered_df['id']==project_to_edit]['assignee'].iloc[0])
                    new_part = st.selectbox("파트", options=PARTS, 
                                          index=PARTS.index(filtered_df[filtered_df['id']==project_to_edit]['part'].iloc[0]))
                    new_category = st.selectbox("분류", options=CATEGORIES)
                
                with col2:
                    new_status = st.selectbox("진행 현황", options=STATUSES)
                    new_planned = st.slider("계획 일정 (%)", 0, 100, int(filtered_df[filtered_df['id']==project_to_edit]['planned_progress'].iloc[0]))
                    new_actual = st.slider("실제 진행 (%)", 0, 100, int(filtered_df[filtered_df['id']==project_to_edit]['actual_progress'].iloc[0]))
                    new_completion = st.slider("진척률 (%)", 0, 100, int(filtered_df[filtered_df['id']==project_to_edit]['completion_rate'].iloc[0]))
                    new_deadline = st.date_input("마감일", value=pd.to_datetime(filtered_df[filtered_df['id']==project_to_edit]['deadline'].iloc[0]))
                
                new_description = st.text_area("업무 설명", value=filtered_df[filtered_df['id']==project_to_edit].get('description', pd.Series([''])).iloc[0] or '')
                
                if st.form_submit_button("💾 수정 저장", type="primary"):
                    st.info("프로젝트 수정 기능은 Supabase 완전 연동 후 업데이트 예정입니다.")
        
        with tab2:
            st.warning("⚠️ 삭제하면 복구할 수 없습니다!")
            if st.button("🗑️ 이 프로젝트 삭제하기", type="secondary"):
                if st.checkbox("정말 삭제하시겠습니까? (확인 체크)", key=f"delete_confirm_{project_to_edit}"):
                    try:
                        supabase = st.session_state.db_conn
                        supabase.table("tasks").delete().eq("id", project_to_edit).execute()
                        st.success("✅ 프로젝트가 삭제되었습니다.")
                        time.sleep(1.5)
                        st.rerun()
                    except Exception as e:
                        st.error(f"삭제 실패: {str(e)}")

    # ==================== 아카이브 관리 ====================
    st.markdown("---")
    st.subheader("🗄️ 아카이브 관리")
    
    try:
        all_df = load_tasks(show_archived=True)
    except:
        all_df = pd.DataFrame()
    
    if not all_df.empty:
        selected_ids = st.multiselect(
            "보관하거나 보관 해제할 프로젝트 선택",
            options=all_df['id'].tolist(),
            format_func=lambda x: f"{'🗄️ 보관됨' if all_df[all_df['id']==x].get('archived', pd.Series([False])).iloc[0] else '✅ 활성'} | "
                                 f"[{all_df[all_df['id']==x].get('part', pd.Series(['미지정'])).iloc[0]}] "
                                 f"{all_df[all_df['id']==x]['project_name'].iloc[0]} - "
                                 f"{all_df[all_df['id']==x]['title'].iloc[0]}"
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🗄️ 선택한 프로젝트 보관하기", use_container_width=True):
                if not selected_ids:
                    st.warning("프로젝트를 선택해주세요.")
                else:
                    supabase = st.session_state.db_conn
                    count = 0
                    for tid in selected_ids:
                        try:
                            current = all_df[all_df['id'] == tid]['archived'].iloc[0]
                            if not current:
                                supabase.table("tasks").update({"archived": True}).eq("id", tid).execute()
                                count += 1
                        except:
                            pass
                    if count > 0:
                        st.success(f"🗄️ {count}개 프로젝트를 보관했습니다.")
                        time.sleep(2.0)
                        st.rerun()
                    else:
                        st.info("선택한 프로젝트는 이미 보관 상태입니다.")
        
        with col_b:
            if st.button("🔓 선택한 프로젝트 보관 해제하기", use_container_width=True):
                if not selected_ids:
                    st.warning("프로젝트를 선택해주세요.")
                else:
                    supabase = st.session_state.db_conn
                    count = 0
                    for tid in selected_ids:
                        try:
                            current = all_df[all_df['id'] == tid]['archived'].iloc[0]
                            if current:
                                supabase.table("tasks").update({"archived": False}).eq("id", tid).execute()
                                count += 1
                        except:
                            pass
                    if count > 0:
                        st.success(f"🔓 {count}개 프로젝트를 보관 해제했습니다.")
                        time.sleep(2.0)
                        st.rerun()
                    else:
                        st.info("선택한 프로젝트는 이미 활성 상태입니다.")
    else:
        st.info("아카이브 관리할 프로젝트가 없습니다.")

    # Excel 다운로드
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📥 Excel 다운로드") and not filtered_df.empty:
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
