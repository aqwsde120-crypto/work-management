# database.py
import streamlit as st
import pandas as pd
from supabase import create_client, Client

@st.cache_resource
def get_supabase_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]

    st.write("현재 연결된 Supabase URL:", url)

    return create_client(url, key)
def init_db():
    """Supabase 초기화 (클라이언트 반환)"""
    return get_supabase_client()

@st.cache_data(ttl=60)
def load_tasks(show_archived=False):
    """태스크 불러오기"""
    supabase: Client = st.session_state.db_conn
    
    if show_archived:
        response = supabase.table("tasks").select("*").order("created_at", desc=True).execute()
    else:
        response = supabase.table("tasks").select("*").eq("archived", False).order("created_at", desc=True).execute()
    
    df = pd.DataFrame(response.data)
    if not df.empty:
        df['deadline'] = pd.to_datetime(df['deadline'], errors='coerce')
    return df

@st.cache_data(ttl=300)
def load_team_members():
    """팀원 불러오기"""
    supabase: Client = st.session_state.db_conn

    response = (
        supabase
        .table("team_members")
        .select("*")
        .execute()
    )

    st.write("team_members 데이터:", response.data)

    return pd.DataFrame(response.data)

def save_task(project_name, title, description, assignee, category, status,
              planned_progress, actual_progress, completion_rate, deadline, part):
    """새 프로젝트 저장"""
    supabase: Client = st.session_state.db_conn
    assignee_str = ','.join(assignee) if isinstance(assignee, list) else assignee
    
    data = {
        "project_name": project_name,
        "title": title,
        "description": description,
        "assignee": assignee_str,
        "category": category,
        "status": status,
        "planned_progress": planned_progress,
        "actual_progress": actual_progress,
        "completion_rate": completion_rate,
        "deadline": deadline,
        "part": part
    }
    
    response = supabase.table("tasks").insert(data).execute()
    # 캐시 무효화
    load_tasks.clear()
    return response.data
