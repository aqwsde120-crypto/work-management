# database.py
import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, timedelta

@st.cache_resource
def get_supabase_client():
    """Supabase 클라이언트 (한 번만 생성)"""
    url = st.secrets["supabase"]["SUPABASE_URL"]
    key = st.secrets["supabase"]["SUPABASE_KEY"]
    return create_client(url, key)

@st.cache_data(ttl=60)   # 60초 동안 캐싱 (필요시 시간 조정)
def load_tasks(show_archived=False):
    """태스크 불러오기 - 캐싱 적용"""
    supabase = get_supabase_client()
    
    if show_archived:
        response = supabase.table("tasks").select("*").order("created_at", desc=True).execute()
    else:
        response = supabase.table("tasks").select("*").eq("archived", False).order("created_at", desc=True).execute()
    
    df = pd.DataFrame(response.data)
    if not df.empty:
        df['deadline'] = pd.to_datetime(df['deadline'], errors='coerce')
    return df

@st.cache_data(ttl=300)   # 팀원은 5분 동안 캐싱
def load_team_members():
    """팀원 불러오기 - 캐싱 적용"""
    supabase = get_supabase_client()
    response = supabase.table("team_members").select("*").order("name").execute()
    return pd.DataFrame(response.data)

def save_task(project_name, title, description, assignee, category, status,
              planned_progress, actual_progress, completion_rate, deadline, part):
    """새 프로젝트 저장"""
    supabase = get_supabase_client()
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
