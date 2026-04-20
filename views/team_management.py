# pages/team_management.py
import streamlit as st
from database import load_team_members

def show_team_management():
    """팀원 관리 화면 - Supabase 버전"""
    st.title("👥 팀원 관리")
    st.markdown("---")
    
    # 현재 팀원 목록
    team_members = load_team_members()
    
    st.subheader("현재 팀원")
    
    if not team_members.empty:
        for _, member in team_members.iterrows():
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                st.markdown(f"## {member.get('emoji', '👤')}")
            with col2:
                st.markdown(f"### {member.get('name', '')}")
            with col3:
                if st.button("🗑️ 삭제", key=f"delete_{member.get('id')}"):
                    try:
                        supabase = st.session_state.db_conn
                        supabase.table("team_members").delete().eq("id", member.get('id')).execute()
                        st.success(f"{member.get('name')} 삭제됨")
                        st.rerun()
                    except Exception as e:
                        st.error(f"삭제 실패: {str(e)}")
    else:
        st.info("등록된 팀원이 없습니다.")

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
                try:
                    supabase = st.session_state.db_conn
                    data = {"name": new_name, "emoji": new_emoji}
                    supabase.table("team_members").insert(data).execute()
                    st.success(f"✅ {new_name} 추가됨!")
                    st.rerun()
                except Exception as e:
                    if "duplicate" in str(e).lower():
                        st.error("이미 존재하는 이름입니다!")
                    else:
                        st.error(f"추가 실패: {str(e)}")
            else:
                st.error("이름을 입력해주세요!")
