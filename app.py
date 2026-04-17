"""
팀 프로젝트 관리 시스템
Professional Team Project & Task Management System
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

# ==================== 페이지 설정 ====================
st.set_page_config(
    page_title="팀 프로젝트 관리",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 커스텀 CSS ====================
def load_custom_css():
    st.markdown("""
    <style>
    /* 전체 테마 */
    .main {
        padding: 2rem;
    }
    
    /* 대시보드 메트릭 카드 */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .metric-card h3 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
    }
    
    .metric-card p {
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* 상태 배지 스타일 */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .status-진행중 { background-color: #4299e1; color: white; }
    .status-완료 { background-color: #48bb78; color: white; }
    .status-일정지연 { background-color: #f56565; color: white; }
    .status-검토중 { background-color: #ed8936; color: white; }
    
    /* 테이블 스타일 개선 */
    .dataframe {
        font-size: 0.9rem;
    }
    
    /* 사이드바 스타일 */
    .css-1d391kg {
        padding-top: 2rem;
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* 칸반 카드 스타일 */
    .kanban-card {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .kanban-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transform: translateX(4px);
        transition: all 0.3s;
    }
    
    /* 다크모드 조정 */
    [data-testid="stAppViewContainer"][data-theme="dark"] .kanban-card {
        background: #1e293b;
    }
    
    [data-testid="stAppViewContainer"][data-theme="dark"] .metric-card {
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== 데이터베이스 초기화 ====================
def init_db():
    conn = sqlite3.connect('projects.db', check_same_thread=False)
    c = conn.cursor()
    
    # tasks 테이블 생성
    c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        assignee TEXT,
        category TEXT,
        status TEXT,
        planned_progress INTEGER,
        actual_progress INTEGER,
        completion_rate INTEGER,
        deadline DATE,
        approved INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        archived INTEGER DEFAULT 0
    )
    ''')
    
    # team_members 테이블 생성
    c.execute('''
    CREATE TABLE IF NOT EXISTS team_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        emoji TEXT DEFAULT '👤'
    )
    ''')
    
    # 기본 팀원 등록
    c.execute('SELECT COUNT(*) FROM team_members')
    if c.fetchone()[0] == 0:
        default_members = [
            ('박성숙', '👔'), ('송수용', '💼'), ('이민경', '👩‍💼'),
            ('나의연', '👨‍💻'), ('김지수', '📊'), ('정은지', '🔥')
        ]
        c.executemany('INSERT OR IGNORE INTO team_members (name, emoji) VALUES (?, ?)', default_members)
    
    conn.commit()
    return conn

# ==================== 데이터 로드 함수 ====================
def load_tasks(show_archived=False):
    conn = st.session_state.db_conn
    if show_archived:
        query = "SELECT * FROM tasks ORDER BY created_at DESC"
    else:
        query = "SELECT * FROM tasks WHERE archived = 0 ORDER BY created_at DESC"
    df = pd.read_sql_query(query, conn)
    df['deadline'] = pd.to_datetime(df['deadline'])
    return df

def load_team_members():
    conn = st.session_state.db_conn
    query = "SELECT * FROM team_members ORDER BY name"
    return pd.read_sql_query(query, conn)

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
        st.markdown("### 🔐 팀 프로젝트 관리 시스템")
        st.markdown("---")
        st.text_input(
            "비밀번호를 입력하세요",
            type="password",
            on_change=password_entered,
            key="password",
        )
        st.info("💡 기본 비밀번호: team123")
        return False
    
    elif not st.session_state["password_correct"]:
        st.markdown("### 🔐 팀 프로젝트 관리 시스템")
        st.markdown("---")
        st.text_input(
            "비밀번호를 입력하세요",
            type="password",
            on_change=password_entered,
            key="password",
        )
        st.error("😕 비밀번호가 올바르지 않습니다.")
        return False
    
    else:
        return True

# ==================== 대시보드 뷰 ====================
def show_dashboard(df):
    st.title("📊 대시보드")
    st.markdown("---")
    
    # 주요 메트릭
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <h3>{len(df)}</h3>
            <p>전체 프로젝트</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        in_progress = len(df[df['status'] == '진행 중'])
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);">
            <h3>{in_progress}</h3>
            <p>진행 중</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        completed = len(df[df['status'] == '완료'])
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);">
            <h3>{completed}</h3>
            <p>완료</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_progress = df['completion_rate'].mean()
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);">
            <h3>{avg_progress:.0f}%</h3>
            <p>평균 진척률</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 차트 영역
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 담당자별 워크로드")
        
        # 담당자별 작업 수 계산
        assignee_work = {}
        for assignees in df['assignee'].dropna():
            for person in assignees.split(','):
                person = person.strip()
                assignee_work[person] = assignee_work.get(person, 0) + 1
        
        if assignee_work:
            fig = px.bar(
                x=list(assignee_work.keys()),
                y=list(assignee_work.values()),
                labels={'x': '담당자', 'y': '작업 수'},
                color=list(assignee_work.values()),
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                showlegend=False,
                height=300,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("담당자 데이터가 없습니다.")
    
    with col2:
        st.subheader("📈 상태별 분포")
        
        status_counts = df['status'].value_counts()
        colors = {
            '진행 중': '#4299e1',
            '완료': '#48bb78',
            '일정 지연': '#f56565',
            '검토 중': '#ed8936'
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=.4,
            marker_colors=[colors.get(status, '#999') for status in status_counts.index]
        )])
        fig.update_layout(
            showlegend=True,
            height=300,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 지연 프로젝트 경고
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("⚠️ 지연 프로젝트")
    
    delayed = df[df['status'] == '일정 지연']
    if len(delayed) > 0:
        for _, task in delayed.iterrows():
            st.error(f"**{task['project_name']}** - {task['title']} (마감: {task['deadline'].strftime('%Y-%m-%d')})")
    else:
        st.success("✅ 지연된 프로젝트가 없습니다!")
    
    # 마감 임박 프로젝트
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📅 마감 임박 (7일 이내)")
    
    today = pd.Timestamp.now()
    upcoming = df[(df['deadline'] - today).dt.days.between(0, 7) & (df['status'] != '완료')]
    
    if len(upcoming) > 0:
        for _, task in upcoming.iterrows():
            days_left = (task['deadline'] - today).days
            st.warning(f"**{task['project_name']}** - {task['title']} (D-{days_left})")
    else:
        st.info("마감 임박한 프로젝트가 없습니다.")

# ==================== 프로젝트 테이블 뷰 ====================
def show_project_table(df, show_archived=False):
    st.title("📋 프로젝트 테이블")
    st.markdown("---")
    
    # 필터 영역
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        search_term = st.text_input("🔍 프로젝트명 또는 업무 제목 검색", "")
    with col2:
        team_members = load_team_members()['name'].tolist()
        selected_assignees = st.multiselect("👥 담당자 필터", options=team_members)
    with col3:
        statuses = df['status'].unique().tolist()
        selected_status = st.multiselect("📊 상태 필터", options=statuses)
    with col4:
        categories = df['category'].unique().tolist()
        selected_category = st.multiselect("🗂️ 분류 필터", options=categories)
    
    # 필터 적용
    filtered_df = df.copy()
    if search_term:
        filtered_df = filtered_df[
            filtered_df['project_name'].str.contains(search_term, case=False, na=False) |
            filtered_df['title'].str.contains(search_term, case=False, na=False)
        ]
    if selected_assignees:
        filtered_df = filtered_df[
            filtered_df['assignee'].apply(
                lambda x: any(person in str(x) for person in selected_assignees) if pd.notna(x) else False
            )
        ]
    if selected_status:
        filtered_df = filtered_df[filtered_df['status'].isin(selected_status)]
    if selected_category:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_category)]
    
    st.markdown(f"**총 {len(filtered_df)}개 프로젝트**")
    
    # 테이블 표시
    display_df = filtered_df.copy()
    display_df['deadline'] = pd.to_datetime(display_df['deadline']).dt.strftime('%Y-%m-%d')
    
    if "selected_project_id" not in st.session_state:
        st.session_state.selected_project_id = None
    
    # 데이터프레임 표시 (클릭 가능)
    selected_event = st.dataframe(
        display_df[['project_name', 'title', 'assignee', 'category', 'status',
                    'planned_progress', 'actual_progress', 'completion_rate', 'deadline']],
        column_config={
            "project_name": st.column_config.TextColumn("프로젝트명", width="medium"),
            "title": st.column_config.TextColumn("업무 제목", width="large"),
            "assignee": st.column_config.TextColumn("담당자", width="medium"),
            "category": st.column_config.TextColumn("분류", width="small"),
            "status": st.column_config.TextColumn("진행 현황", width="medium"),
            "planned_progress": st.column_config.ProgressColumn("계획 일정", format="%d%%"),
            "actual_progress": st.column_config.ProgressColumn("실제 진행", format="%d%%"),
            "completion_rate": st.column_config.ProgressColumn("진척률", format="%d%%"),
            "deadline": st.column_config.TextColumn("마감일"),
        },
        hide_index=True,
        use_container_width=True,
        height=550,
        on_select="rerun",
        selection_mode="single-row"
    )

    # 모달 창 열기
    if selected_event.selection and len(selected_event.selection.rows) > 0:
        row_idx = selected_event.selection.rows[0]
        selected_id = int(display_df.iloc[row_idx]['id'])
        st.session_state.selected_project_id = selected_id

        # 상세 모달 창 (에러 방지를 위해 최대한 단순화)
        with st.dialog("Project Detail"):
            task = filtered_df[filtered_df['id'] == selected_id].iloc[0]
            is_archived = task.get('archived', 0) == 1
            
            st.markdown("### 📋 프로젝트 상세 정보 및 수정")
            
            col1, col2 = st.columns(2)
            with col1:
                new_project_name = st.text_input("프로젝트명", value=task['project_name'])
                new_title = st.text_input("업무 제목", value=task['title'])
                new_assignee = st.multiselect(
                    "담당자", 
                    options=load_team_members()['name'].tolist(),
                    default=[x.strip() for x in str(task.get('assignee', '')).split(',')] if task.get('assignee') else []
                )
                new_category = st.selectbox("분류", 
                    options=["규제동향", "허가관리", "실사관리", "협력업체관리", "자율점검", 
                             "교육관리", "직무관리", "품질문화", "기타"])
            
            with col2:
                new_status = st.selectbox("진행 현황", 
                    options=["진행 중", "검토 중", "완료", "일정 지연"])
                new_planned = st.slider("계획 일정 (%)", 0, 100, int(task['planned_progress']))
                new_actual = st.slider("실제 진행 (%)", 0, 100, int(task['actual_progress']))
                new_completion = st.slider("프로젝트 진척률 (%)", 0, 100, int(task['completion_rate']))
                new_deadline = st.date_input("마감일", value=pd.to_datetime(task['deadline']))
            
            new_description = st.text_area("업무 설명", value=task.get('description') or "")

            st.markdown("---")
            col_a, col_b, col_c = st.columns([2, 2, 1])
            
            with col_a:
                if st.button("💾 수정 내용 저장", type="primary"):
                    conn = st.session_state.db_conn
                    c = conn.cursor()
                    assignee_str = ','.join(new_assignee)
                    c.execute('''
                        UPDATE tasks 
                        SET project_name=?, title=?, assignee=?, category=?, status=?,
                            planned_progress=?, actual_progress=?, completion_rate=?, 
                            deadline=?, description=?
                        WHERE id=?
                    ''', (new_project_name, new_title, assignee_str, new_category, new_status,
                          new_planned, new_actual, new_completion, 
                          new_deadline.strftime('%Y-%m-%d'), new_description, selected_id))
                    conn.commit()
                    st.success("✅ 수정이 저장되었습니다!")
                    st.rerun()
            
            with col_b:
                if is_archived:
                    if st.button("🔓 보관 해제하기"):
                        conn = st.session_state.db_conn
                        c = conn.cursor()
                        c.execute("UPDATE tasks SET archived = 0 WHERE id = ?", (selected_id,))
                        conn.commit()
                        st.success("보관이 해제되었습니다.")
                        st.rerun()
                else:
                    if st.button("🗄️ 프로젝트 보관하기"):
                        conn = st.session_state.db_conn
                        c = conn.cursor()
                        c.execute("UPDATE tasks SET archived = 1 WHERE id = ?", (selected_id,))
                        conn.commit()
                        st.success("프로젝트가 보관되었습니다.")
                        st.rerun()
            
            with col_c:
                if st.button("❌ 닫기"):
                    st.session_state.selected_project_id = None
                    st.rerun()

    # Excel 다운로드
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📥 Excel 다운로드"):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            filtered_df.to_excel(writer, index=False)
        output.seek(0)
        st.download_button(
            label="📥 다운로드 시작",
            data=output,
            file_name=f"프로젝트_관리_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# ==================== Kanban 보드 뷰 ====================
def show_kanban_board(df):
    st.title("🗂️ Kanban 보드")
    st.markdown("---")
    
    # 개선된 컬럼 구조: 검토 중 | 진행 중 | 일정 지연 | 완료
    kanban_columns = {
        "검토 중": ["검토 중"],
        "진행 중": ["진행 중"],
        "일정 지연": ["일정 지연"],
        "완료": ["완료"]
    }
    
    # 4개 컬럼 생성
    cols = st.columns(4)
    
    for idx, (column_name, status_list) in enumerate(kanban_columns.items()):
        with cols[idx]:
            # 컬럼 헤더
            count = len(df[df['status'].isin(status_list)])
            st.markdown(f"""
            <h3 style="text-align: center; margin-bottom: 10px;">
                {column_name} <span style="font-size: 0.9rem; color: #718096;">({count})</span>
            </h3>
            """, unsafe_allow_html=True)
            
            # 해당 상태의 업무들 표시
            tasks_in_column = df[df['status'].isin(status_list)].sort_values(by='deadline')
            
            for _, task in tasks_in_column.iterrows():
                # 마감일까지 남은 일수 계산
                days_left = (task['deadline'] - pd.Timestamp.now()).days
                
                if days_left < 0:
                    deadline_status = "🔴 지연"
                    deadline_color = "#f56565"
                elif days_left <= 7:
                    deadline_status = f"🟡 D-{days_left}"
                    deadline_color = "#ed8936"
                else:
                    deadline_status = f"🟢 D-{days_left}"
                    deadline_color = "#48bb78"
                
                st.markdown(f"""
                <div style="background: white; border-radius: 10px; padding: 14px; margin-bottom: 12px; 
                            box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-left: 5px solid {deadline_color};">
                    <div style="font-size: 0.85rem; color: #718096; margin-bottom: 6px;">
                        {task['project_name']}
                    </div>
                    <div style="font-weight: 600; font-size: 1.02rem; margin-bottom: 8px; line-height: 1.3;">
                        {task['title']}
                    </div>
                    <div style="font-size: 0.9rem; margin-bottom: 8px;">
                        👤 {task['assignee']}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem;">
                        <span>📅 {task['deadline'].strftime('%Y-%m-%d')}</span>
                        <span style="color: {deadline_color}; font-weight: 600;">{deadline_status}</span>
                    </div>
                    <div style="margin-top: 10px;">
                        <div style="background: #e2e8f0; height: 6px; border-radius: 10px; overflow: hidden;">
                            <div style="background: #4299e1; height: 100%; width: {task['completion_rate']}%;"></div>
                        </div>
                        <small style="color: #4a5568;">진척률 {task['completion_rate']}%</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # 해당 컬럼에 업무가 없을 때
            if len(tasks_in_column) == 0:
                st.markdown("""
                <div style="text-align: center; padding: 40px 20px; color: #94a3b8; 
                            background: #f8fafc; border-radius: 10px;">
                    업무가 없습니다
                </div>
                """, unsafe_allow_html=True)

# ==================== 새 프로젝트 추가 ====================
def show_add_project():
    st.title("➕ 새 프로젝트/업무 추가")
    st.markdown("---")
    
    with st.form("add_project_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("프로젝트명 *", placeholder="예: 규제동향 모니터링")
            title = st.text_input("업무 제목 *", placeholder="예: 2026년 상반기 규제 변경 분석")
            description = st.text_area("업무 설명", placeholder="상세 업무 내용을 입력하세요")
            
            team_members = load_team_members()['name'].tolist()
            assignee = st.multiselect("담당자 *", options=team_members)
        
        with col2:
            category = st.selectbox("분류 *", options=[
                "규제동향", "허가관리", "실사관리", "협력업체관리", 
                "자율점검", "교육관리", "직무관리", "품질문화", "기타"
            ])
            status = st.selectbox("진행 현황 *", options=["진행 중", "검토 중", "완료", "일정 지연"])
            
            col2_1, col2_2, col2_3 = st.columns(3)
            with col2_1:
                planned_progress = st.slider("계획 일정 (%)", 0, 100, 0)
            with col2_2:
                actual_progress = st.slider("실제 진행 (%)", 0, 100, 0)
            with col2_3:
                completion_rate = st.slider("프로젝트 진척률 (%)", 0, 100, 0)
            
            deadline = st.date_input("마감일 *", value=datetime.now() + timedelta(days=30))
        
        submitted = st.form_submit_button("✅ 프로젝트 추가", use_container_width=True)
        
        if submitted:
            if not project_name or not title or not assignee:
                st.error("필수 항목(*)을 모두 입력해주세요!")
            else:
                conn = st.session_state.db_conn
                c = conn.cursor()
                assignee_str = ','.join(assignee)
                
                c.execute('''
                INSERT INTO tasks 
                (project_name, title, description, assignee, category, status,
                 planned_progress, actual_progress, completion_rate, deadline)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (project_name, title, description, assignee_str, category, status,
                      planned_progress, actual_progress, completion_rate, deadline.strftime('%Y-%m-%d')))
                
                conn.commit()
                st.success(f"✅ '{title}' 업무가 추가되었습니다!")
                st.balloons()
                st.rerun()

# ==================== 팀원 관리 ====================
def show_team_management():
    st.title("👥 팀원 관리")
    st.markdown("---")
    
    # 현재 팀원 목록
    team_members = load_team_members()
    
    st.subheader("현재 팀원")
    
    # 팀원 표시
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
                except sqlite3.IntegrityError:
                    st.error("이미 존재하는 이름입니다!")
            else:
                st.error("이름을 입력해주세요!")

# ==================== 메인 앱 ====================
def main():
    # 비밀번호 체크
    if not check_password():
        return
    
    # 데이터베이스 초기화
    if 'db_conn' not in st.session_state:
        st.session_state.db_conn = init_db()
    
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
        
        # 다크모드 토글 (Streamlit 네이티브 사용)
        st.markdown("### ⚙️ 설정")
        
        # 통계 요약
        df = load_tasks(show_archived=show_archived)
        st.markdown("### 📈 빠른 통계")
        st.metric("전체 프로젝트", len(df))
        st.metric("진행 중", len(df[df['status'] == '진행 중']))
        st.metric("평균 진척률", f"{df['completion_rate'].mean():.0f}%")
        
        st.markdown("---")
        st.markdown("**개발:** Claude + Streamlit")
        st.markdown("**버전:** 1.0.0")
    
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
