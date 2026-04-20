# database.py
import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime

@st.cache_resource
def get_supabase_client():
    """Supabase 클라이언트 생성"""
    url = st.secrets["supabase"]["SUPABASE_URL"]
    key = st.secrets["supabase"]["SUPABASE_KEY"]
    return create_client(url, key)

def init_db():
    """Supabase는 별도 초기화 불필요 (테이블은 Supabase에서 이미 생성)"""
    return get_supabase_client()

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

def load_team_members():
    """팀원 불러오기"""
    supabase: Client = st.session_state.db_conn
    response = supabase.table("team_members").select("*").order("name").execute()
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
    return response.data
