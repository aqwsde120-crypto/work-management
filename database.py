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
        
        # emoji 컬럼이 없으면 기본값 추가
        if 'emoji' not in df.columns:
            df['emoji'] = '👤'
        
        return df
        
    except Exception as e:
        st.error(f"❌ team_members 불러오기 실패: {e}")
        return pd.DataFrame()


def save_task(project_name, title, description, assignee, category, status,
              planned_progress, actual_progress, completion_rate, deadline, part):
    """새 프로젝트 저장"""
    supabase: Client = st.session_state.db_conn
    try:
        # assignee 처리 개선
        if isinstance(assignee, list):
            assignee_str = ','.join(assignee)
        elif assignee is None or assignee == "Choose options" or assignee == "":
            assignee_str = ""
        else:
            assignee_str = str(assignee)

        data = {
            "project_name": project_name,
            "title": title,
            "description": description or "",
            "assignee": assignee_str,
            "category": category,
            "status": status,
            "planned_progress": float(planned_progress) if planned_progress else 0,
            "actual_progress": float(actual_progress) if actual_progress else 0,
            "completion_rate": float(completion_rate) if completion_rate else 0,
            "deadline": deadline,
            "part": part,
            "archived": False
        }
        
        response = supabase.table("tasks").insert(data).execute()
        
        # 캐시 무효화
        load_tasks.clear()
        
        st.success("✅ 프로젝트가 성공적으로 저장되었습니다!")
        st.balloons()  # 저장 성공 시 효과
        return response.data
        
    except Exception as e:
        st.error(f"❌ 프로젝트 저장 실패: {e}")
        return None
