# pages/add_project.py
import streamlit as st
from datetime import datetime, timedelta
import time
from config import PARTS, CATEGORIES, STATUSES
from database import load_team_members, save_task

def show_add_project():
    """새 프로젝트/업무 추가 화면 (Supabase 버전)"""
    st.title("➕ 새 프로젝트/업무 추가")
    st.markdown("---")
    
    with st.form("add_project_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("프로젝트명 *", placeholder="예: 규제동향 모니터링")
            title = st.text_input("업무 제목 *", placeholder="예: 2026년 상반기 규제 변경 분석")
            description = st.text_area("업무 설명", placeholder="상세 업무 내용을 입력하세요")
            
            team_members = load_team_members()['name'].tolist()
            assignee = st.multiselect("담당자 *", options=team_members)
        
        with col2:
            part = st.selectbox("파트 *", options=PARTS)
            category = st.selectbox("분류 *", options=CATEGORIES)
            status = st.selectbox("진행 현황 *", options=STATUSES)
            
            col2_1, col2_2, col2_3 = st.columns(3)
            with col2_1:
                planned_progress = st.slider("계획 일정 (%)", 0, 100, 0)
            with col2_2:
                actual_progress = st.slider("실제 진행 (%)", 0, 100, 0)
            with col2_3:
                completion_rate = st.slider("프로젝트 진척률 (%)", 0, 100, 0)
            
            deadline = st.date_input("마감일 *", value=datetime.now() + timedelta(days=30))
        
        submitted = st.form_submit_button("✅ 프로젝트 추가", use_container_width=True)
        
        if submitted:
            if not project_name or not title or not assignee or not part:
                st.error("❌ 필수 항목(*)을 모두 입력해주세요!")
            else:
                try:
                    save_task(
                        project_name=project_name,
                        title=title,
                        description=description,
                        assignee=assignee,
                        category=category,
                        status=status,
                        planned_progress=planned_progress,
                        actual_progress=actual_progress,
                        completion_rate=completion_rate,
                        deadline=deadline.strftime('%Y-%m-%d'),
                        part=part
                    )
                    
                    st.success(f"🎉 '{title}' 업무가 성공적으로 추가되었습니다! (파트: {part})")
                    st.balloons()
                    st.toast(f"프로젝트 '{title}'가 추가되었습니다!", icon="✅")
                    
                    time.sleep(1.5)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"저장 중 오류가 발생했습니다: {str(e)}")
