# pages/project_table.py
import streamlit as st
import pandas as pd
import io
from datetime import datetime
from config import PARTS, CATEGORIES, STATUSES
from database import load_team_members

def show_project_table(df, show_archived=False):
    """프로젝트 테이블 화면 - Supabase 안전 버전"""
    st.title("📋 프로젝트 테이블")
    st.markdown("---")
    
    # 팀원 목록 안전하게 불러오기
    try:
        team_df = load_team_members()
        team_members = team_df['name'].tolist() if not team_df.empty and 'name' in team_df.columns else []
    except:
        team_members = []
    
    # 필터 영역
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        search_term = st.text_input("🔍 프로젝트명 또는 업무 제목 검색", "")
    with col2:
        selected_assignees = st.multiselect("👥 담당자 필터", options=team_members)
    with col3:
        statuses = df['status'].unique().tolist() if 'status' in df.columns and not df.empty else STATUSES
        selected_status = st.multiselect("📊 상태 필터", options=statuses)
    with col4:
        categories = df['category'].unique().tolist() if 'category' in df.columns and not df.empty else CATEGORIES
        selected_category = st.multiselect("🗂️ 분류 필터", options=categories)
    with col5:
        parts = df['part'].unique().tolist() if 'part' in df.columns and not df.empty else PARTS
        selected_part = st.multiselect("📌 파트 필터", options=parts)
    
    # 필터 적용
    filtered_df = df.copy()
    if search_term and not filtered_df.empty:
        filtered_df = filtered_df[
            filtered_df.get('project_name', pd.Series()).str.contains(search_term, case=False, na=False) |
            filtered_df.get('title', pd.Series()).str.contains(search_term, case=False, na=False)
        ]
    if selected_assignees and not filtered_df.empty and 'assignee' in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df['assignee'].apply(
                lambda x: any(person in str(x) for person in selected_assignees) if pd.notna(x) else False
            )
        ]
    if selected_status and not filtered_df.empty and 'status' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['status'].isin(selected_status)]
    if selected_category and not filtered_df.empty and 'category' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_category)]
    if selected_part and not filtered_df.empty and 'part' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['part'].isin(selected_part)]
    
    st.markdown(f"**총 {len(filtered_df)}개 프로젝트**")
    
    # 테이블 표시
    if not filtered_df.empty:
        display_df = filtered_df.copy()
        if 'deadline' in display_df.columns:
            display_df['deadline'] = pd.to_datetime(display_df['deadline'], errors='coerce').dt.strftime('%Y-%m-%d')
        
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
    else:
        st.info("표시할 프로젝트가 없습니다. 새 프로젝트를 추가해보세요.")

    # 프로젝트 수정 (간단 버전 - Supabase 연동 준비)
    st.markdown("---")
    st.subheader("✏️ 프로젝트 수정")
    st.info("프로젝트 수정 기능은 Supabase 완전 연동 후 추가됩니다.")

    # 아카이브 관리
    st.markdown("---")
    st.subheader("🗄️ 아카이브 관리")
    st.info("아카이브 기능은 Supabase 완전 연동 후 추가됩니다.")

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
