# app.py
"""
팀 프로젝트 관리 시스템
Professional Team Project & Task Management System
"""
import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="팀 프로젝트 관리",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 모듈 import
from config import PARTS, APP_TITLE, APP_VERSION
from database import init_db, load_tasks, load_team_members
from utils import load_custom_css
from pages.dashboard import show_dashboard
from pages.project_table import show_project_table
from pages.kanban import show_kanban_board
from pages.add_project import show_add_project
from pages.team_management import show_team_management

# ==================== 비밀번호 체크 ====================
def check_password():
    """간단한 비밀번호 보호"""
    def password_entered():
        if st.session_state["password"] == st.secrets.get("app_password", "team123"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown(f"### 🔐 {APP_TITLE}")
        st.markdown("---")
        st.text_input("비밀번호를 입력하세요", type="password", on_change=password_entered, key="password")
        st.info("💡 기본 비밀번호: team123")
        return False

    elif not st.session_state["password_correct"]:
        st.markdown(f"### 🔐 {APP_TITLE}")
        st.markdown("---")
        st.text_input("비밀번호를 입력하세요", type="password", on_change=password_entered, key="password")
        st.error("😕 비밀번호가 올바르지 않습니다.")
        return False

    else:
        return True

# ==================== 메인 앱 ====================
def main():
    # 비밀번호 체크
    if not check_password():
        return

    # 데이터베이스 초기화
    if 'db_conn' not in st.session_state:
        st.session_state.db_conn = init_db()
    
    # 팀원 데이터 미리 로드 (세션에 저장)
    if 'team_members' not in st.session_state:
        st.session_state.team_members = load_team_members()
    
    # load_tasks 함수를 세션에 저장 (다른 페이지에서 사용)
    if 'load_tasks_func' not in st.session_state:
        st.session_state.load_tasks_func = load_tasks

    # 커스텀 CSS 로드
    load_custom_css()

    # 사이드바
    with st.sidebar:
        st.title("🎯 팀 프로젝트 관리")
        st.markdown("---")
        
        # 네비게이션
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
        st.metric("진행 중", len(df[df['status'] == '진행 중']))
        st.metric("평균 진척률", f"{df['completion_rate'].mean():.0f}%" if not df.empty else "0%")
        
        st.markdown("---")
        st.markdown(f"**개발:** Claude + Streamlit")
        st.markdown(f"**버전:** {APP_VERSION}")

    # 데이터 로드
    df = load_tasks()

    # 선택된 메뉴에 따라 화면 표시
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
