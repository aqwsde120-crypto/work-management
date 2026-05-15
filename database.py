import streamlit as st
import pandas as pd
from supabase import create_client, Client


@st.cache_resource
def get_supabase_client():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_ANON_KEY"]
        
        client = create_client(url, key)
        st.success("✅ Supabase 연결 성공")
        return client
    except Exception as e:
        st.error(f"❌ Supabase secrets 설정 오류: {e}")
        st.info("Streamlit Cloud → Settings → Secrets 를 확인해주세요.")
        raise


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
    """팀원 불러오기 - 개선 버전"""
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
        
        # 디버깅 정보 (필요시 st.write 대신 사용)
        if df.empty:
            st.info("📭 team_members 테이블에 데이터가 없습니다.")
        else:
            st.success(f"✅ 팀원 {len(df)}명 불러오기 성공")
        
        # emoji 컬럼을 avatar으로 변환 (UI에서 편하게 사용하기 위함)
        if 'emoji' in df.columns:
            df = df.rename(columns={'emoji': 'avatar'})
        
        # 컬럼 순서 정리
        desired_columns = ['id', 'name', 'avatar']
        for col in desired_columns:
            if col not in df.columns:
                df[col] = None
                
        return df[desired_columns] if not df.empty else pd.DataFrame(columns=desired_columns)
        
    except Exception as e:
        st.error(f"❌ team_members 불러오기 실패: {e}")
        return pd.DataFrame(columns=['id', 'name', 'avatar'])


def save_task(project_name, title, description, assignee, category, status,
              planned_progress, actual_progress, completion_rate, deadline, part):
    """새 프로젝트 저장"""
    supabase: Client = st.session_state.db_conn
    try:
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
        st.success("✅ 태스크가 성공적으로 저장되었습니다.")
        return response.data
    except Exception as e:
        st.error(f"태스크 저장 실패: {e}")
        return None
