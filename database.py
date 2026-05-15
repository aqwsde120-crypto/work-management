import streamlit as st
import pandas as pd
from supabase import create_client, Client


@st.cache_resource
def get_supabase_client():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_ANON_KEY"]
        
        client = create_client(url, key)
        return client   # 성공 메시지는 주석 처리 (매번 뜨지 않게)
    except KeyError as e:
        st.error(f"❌ Secrets 키 누락: {e}")
        st.info("Streamlit Cloud → Settings → Secrets 에 SUPABASE_URL과 SUPABASE_ANON_KEY를 추가했는지 확인해주세요.")
        st.stop()   # 앱 멈추기
    except Exception as e:
        st.error(f"❌ Supabase 연결 실패: {e}")
        st.stop()


def init_db():
    """Supabase 초기화"""
    if 'db_conn' not in st.session_state:
        st.session_state.db_conn = get_supabase_client()
    return st.session_state.db_conn


@st.cache_data(ttl=60)
def load_tasks(show_archived=False):
    """태스크 불러오기"""
    supabase: Client = st.session_state.db_conn
    try:
        if show_archived:
            response = supabase.table("tasks").select("*").order("created_at", desc=True).execute()
        else:
            response = supabase.table("tasks").select("*").eq("archived", False).order("created_at", desc=True).execute()
        
        df = pd.DataFrame(response.data)
        if not df.empty:
            df['deadline'] = pd.to_datetime(df['deadline'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"tasks 불러오기 실패: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=60)
def load_team_members():
    """팀원 불러오기"""
    supabase: Client = st.session_state.db_conn
    try:
        response = (
            supabase
            .table("team_members")
            .select("*")
            .order("id", desc=True)
            .execute()
        )
        
        df = pd.DataFrame(response.data)
        
        if df.empty:
            st.info("📭 team_members 테이블에 데이터가 없습니다.")
            return pd.DataFrame()
        
        # emoji → avatar 매핑 (기존 UI와 호환되도록)
        if 'emoji' in df.columns:
            df = df.rename(columns={'emoji': 'avatar'})
        elif 'avatar' not in df.columns:
            df['avatar'] = None
        
        st.success(f"✅ 팀원 {len(df)}명 불러오기 성공")
        
        return df
        
    except Exception as e:
        st.error(f"❌ team_members 불러오기 실패: {e}")
        return pd.DataFrame()


def save_task(project_name, title, description, assignee, category, status,
              planned_progress, actual_progress, completion_rate, deadline, part):
    """새 프로젝트 저장"""
    supabase: Client = st.session_state.db_conn
    try:
        assignee_str = ','.join(assignee) if isinstance(assignee, list) else str(assignee)
        
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
        st.success("✅ 태스크가 성공적으로 저장되었습니다.")
        return response.data
    except Exception as e:
        st.error(f"태스크 저장 실패: {e}")
        return None
