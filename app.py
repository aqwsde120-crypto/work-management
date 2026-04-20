# app.py
"""
종근당 바이오QA팀 프로젝트 관리 시스템
"""
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="종근당 바이오QA팀 프로젝트 관리",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 모듈 import
from config import APP_TITLE, APP_VERSION
from database import init_db, load_tasks, load_team_members, save_task
from utils import load_custom_css

from views.dashboard import show_dashboard
from views.project_table import show_project_table
from views.kanban import show_kanban_board
from views.add_project import show_add_project
from views.team_management import show_team_management

# ==================== 메인 앱 ====================
def main():
    # Supabase 연결
    if 'db_conn' not in st.session_state:
        st.session_state.db_conn = init_db()

    # 팀원 데이터 로드
    if 'team_members' not in st.session_state:
        st.session_state.team_members = load_team_members()

    load_custom_css()

    # 사이드바
    with st.sidebar:
        st.title("🎯 종근당 바이오QA팀 프로젝트 관리")
        st.markdown("---")
        
        show_archived = st.checkbox("🗄️ 아카이브된 프로젝트도 보기", value=False)
        
        menu = st.radio(
            "메뉴",
            ["📊 대시보드", "📋 프로젝트 테이블", "🗂️ Kanban 보드",
             "➕ 새 프로젝트/업무 추가", "👥 팀원 관리"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### 📈 빠른 통계")
        df = load_tasks(show_archived=show_archived)
        st.metric("전체 프로젝트", len(df))
        st.metric("진행 중", len(df[df['status'] == '진행 중']) if not df.empty else 0)
        st.metric("평균 진척률", f"{df['completion_rate'].mean():.0f}%" if not df.empty else "0%")
        
        st.markdown("---")
        st.markdown("### 👤 만든 사람")
        st.markdown("""
        **바이오QA팀**  
        송수용  
        ssy@ckdpharm.com
        """)
        
        st.markdown("---")
        st.markdown(f"**개발:** Claude + Streamlit")
        st.markdown(f"**버전:** {APP_VERSION}")

    # 데이터 로드
    df = load_tasks()

    # 메뉴 표시
    if menu == "📊 대시보드":
        show_dashboard(df)
    elif menu == "📋 프로젝트 테이블":
        show_project_table(df, show_archived=show_archived)
    elif menu == "🗂️ Kanban 보드":
        show_kanban_board(df)
    elif menu == "➕ 새 프로젝트/업무 추가":
        show_add_project()
    elif menu == "👥 팀원 관리":
        show_team_management()

if __name__ == "__main__":
    main()
