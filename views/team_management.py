# pages/team_management.py
import streamlit as st
from database import load_team_members

def show_team_management():
    """팀원 관리 화면"""
    st.title("👥 팀원 관리")
    st.markdown("---")
    
    # 현재 팀원 목록
    team_members = load_team_members()
    
    st.subheader("현재 팀원")
    
    for _, member in team_members.iterrows():
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.markdown(f"## {member['emoji']}")
        with col2:
            st.markdown(f"### {member['name']}")
        with col3:
            if st.button("🗑️ 삭제", key=f"delete_{member['id']}"):
                conn = st.session_state.db_conn
                c = conn.cursor()
                c.execute('DELETE FROM team_members WHERE id = ?', (member['id'],))
                conn.commit()
                st.success(f"{member['name']} 삭제됨")
                st.rerun()
    
    st.markdown("---")
    st.subheader("새 팀원 추가")
    
    with st.form("add_member_form"):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_name = st.text_input("이름", placeholder="예: 홍대리")
        with col2:
            new_emoji = st.text_input("이모지", value="👤", max_chars=2)
        
        submitted = st.form_submit_button("➕ 추가", use_container_width=True)
        
        if submitted:
            if new_name:
                conn = st.session_state.db_conn
                c = conn.cursor()
                try:
                    c.execute('INSERT INTO team_members (name, emoji) VALUES (?, ?)',
                             (new_name, new_emoji))
                    conn.commit()
                    st.success(f"✅ {new_name} 추가됨!")
                    st.rerun()
                except st.errors.DuplicateKeyError:
                    st.error("이미 존재하는 이름입니다!")
            else:
                st.error("이름을 입력해주세요!")
