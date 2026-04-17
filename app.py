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
    
    # 기본 팀원 데이터만 삽입 (샘플 프로젝트는 삭제)
    c.execute('SELECT COUNT(*) FROM team_members')
    if c.fetchone()[0] == 0:
        default_members = [
            ('박성숙', '👔'), 
            ('송수용', '💼'), 
            ('이민경', '👩‍💼'), 
            ('나의연', '👨‍💻'), 
            ('김지수', '📊'), 
            ('정은지', '🔧')
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
def show_project_table(df, show_archived=False):   # ← 이전에 아카이브 추가했다면 show_archived 유지
    st.title("📋 프로젝트 테이블")
    st.markdown("---")
    
    # 필터 영역 (기존과 완전히 동일)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        search_term = st.text_input("🔍 프로젝트명 검색", "")
    with col2:
        team_members = load_team_members()['name'].tolist()
        selected_assignees = st.multiselect("👥 담당자 필터", options=team_members)
    with col3:
        statuses = df['status'].unique().tolist()
        selected_status = st.multiselect("📊 상태 필터", options=statuses)
    with col4:
        categories = df['category'].unique().tolist()
        selected_category = st.multiselect("🗂️ 분류 필터", options=categories)
    
    # 필터 적용 (기존 로직 그대로)
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
    
    # ==================== ★★★ 여기서부터 수정 ★★★ ====================
    # 수정 가능한 데이터프레임 준비
    editor_df = filtered_df.copy()
    editor_df['deadline'] = editor_df['deadline'].dt.strftime('%Y-%m-%d')
    
    # st.data_editor로 변경 (진척률 3개 컬럼만 수정 가능)
    edited_df = st.data_editor(
        editor_df[['id', 'project_name', 'title', 'assignee', 'category', 'status',
                   'planned_progress', 'actual_progress', 'completion_rate', 
                   'deadline', 'approved']],
        column_config={
            "id": st.column_config.TextColumn("ID", width="small", disabled=True),
            "project_name": st.column_config.TextColumn("프로젝트명", width="medium", disabled=True),
            "title": st.column_config.TextColumn("업무 제목", width="large", disabled=True),
            "assignee": st.column_config.TextColumn("담당자", width="medium", disabled=True),
            "category": st.column_config.TextColumn("분류", width="small", disabled=True),
            "status": st.column_config.TextColumn("진행 현황", width="medium", disabled=True),
            "planned_progress": st.column_config.NumberColumn(
                "계획 일정 (%)", min_value=0, max_value=100, format="%d%%", step=1
            ),
            "actual_progress": st.column_config.NumberColumn(
                "실제 진행 (%)", min_value=0, max_value=100, format="%d%%", step=1
            ),
            "completion_rate": st.column_config.NumberColumn(
                "프로젝트 진척률 (%)", min_value=0, max_value=100, format="%d%%", step=1
            ),
            "deadline": st.column_config.TextColumn("마감일", width="medium", disabled=True),
            "approved": st.column_config.CheckboxColumn("승인", disabled=True),
        },
        hide_index=True,
        use_container_width=True,
        height=600,
        num_rows="fixed"
    )
    
    # ==================== 변경 사항 저장 버튼 ====================
    st.markdown("---")
    col_save, col_info = st.columns([1, 4])
    with col_save:
        if st.button("💾 변경 사항 저장", type="primary", use_container_width=True):
            # 변경된 행만 찾아서 DB 업데이트
            changed = False
            conn = st.session_state.db_conn
            c = conn.cursor()
            
            for idx, row in edited_df.iterrows():
                original = filtered_df[filtered_df['id'] == row['id']].iloc[0]
                
                if (row['planned_progress'] != original['planned_progress'] or
                    row['actual_progress'] != original['actual_progress'] or
                    row['completion_rate'] != original['completion_rate']):
                    
                    c.execute('''
                        UPDATE tasks 
                        SET planned_progress = ?, 
                            actual_progress = ?, 
                            completion_rate = ?
                        WHERE id = ?
                    ''', (row['planned_progress'], row['actual_progress'], 
                          row['completion_rate'], row['id']))
                    changed = True
            
            if changed:
                conn.commit()
                st.success("✅ 진행 상황이 성공적으로 업데이트되었습니다!")
                st.rerun()
            else:
                st.info("변경된 내용이 없습니다.")
    
    # 테이블 표시용 데이터 준비
    display_df = filtered_df.copy()
    display_df['deadline'] = display_df['deadline'].dt.strftime('%Y-%m-%d')
    
    # 프로페셔널한 테이블 표시
    st.dataframe(
        display_df[['project_name', 'title', 'assignee', 'category', 'status', 
                    'planned_progress', 'actual_progress', 'completion_rate', 
                    'deadline', 'approved']],
        column_config={
            "project_name": st.column_config.TextColumn(
                "프로젝트명",
                width="medium",
                help="프로젝트 이름"
            ),
            "title": st.column_config.TextColumn(
                "업무 제목",
                width="large",
            ),
            "assignee": st.column_config.TextColumn(
                "담당자",
                width="medium",
            ),
            "category": st.column_config.TextColumn(
                "분류",
                width="small",
            ),
            "status": st.column_config.TextColumn(
                "진행 현황",
                width="medium",
            ),
            "planned_progress": st.column_config.ProgressColumn(
                "계획 일정",
                format="%d%%",
                min_value=0,
                max_value=100,
            ),
            "actual_progress": st.column_config.ProgressColumn(
                "실제 진행",
                format="%d%%",
                min_value=0,
                max_value=100,
            ),
            "completion_rate": st.column_config.ProgressColumn(
                "프로젝트 진척률",
                format="%d%%",
                min_value=0,
                max_value=100,
            ),
            "deadline": st.column_config.TextColumn(
                "마감일",
                width="medium",
            ),
            "approved": st.column_config.CheckboxColumn(
                "승인",
                help="프로젝트 승인 여부",
                default=False,
            ),
        },
        hide_index=True,
        use_container_width=True,
        height=600
    )
    
    # 엑셀 다운로드 버튼
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("📥 Excel 다운로드"):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                filtered_df.to_excel(writer, index=False, sheet_name='프로젝트')
            output.seek(0)
            st.download_button(
                label="📥 다운로드 시작",
                data=output,
                file_name=f"프로젝트_관리_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# ==================== 칸반 보드 뷰 ====================
def show_kanban_board(df):
    st.title("🗂️ Kanban 보드")
    st.markdown("---")
    
    # 칸반 컬럼 매핑
    kanban_columns = {
        '할 일': ['검토 중'],
        '진행 중': ['진행 중'],
        '일정 지연': ['일정 지연'],
        '완료': ['완료']
    }
    
    cols = st.columns(4)
    
    for idx, (column_name, statuses) in enumerate(kanban_columns.items()):
        with cols[idx]:
            # 컬럼 헤더
            count = len(df[df['status'].isin(statuses)])
            st.markdown(f"### {column_name} ({count})")
            
            # 카드 표시
            tasks_in_column = df[df['status'].isin(statuses)]
            
            for _, task in tasks_in_column.iterrows():
                # 마감일까지 남은 일수 계산
                days_left = (task['deadline'] - pd.Timestamp.now()).days
                deadline_color = "🔴" if days_left < 0 else "🟡" if days_left < 7 else "🟢"
                
                st.markdown(f"""
                <div class="kanban-card">
                    <small style="color: #718096;">{task['project_name']}</small>
                    <h4 style="margin: 0.5rem 0; font-size: 1rem;">{task['title']}</h4>
                    <p style="margin: 0.3rem 0; font-size: 0.85rem;">
                        👤 {task['assignee']}<br>
                        📅 {task['deadline'].strftime('%Y-%m-%d')} {deadline_color}
                    </p>
                    <div style="margin-top: 0.5rem;">
                        <div style="background: #e2e8f0; border-radius: 10px; height: 8px; overflow: hidden;">
                            <div style="background: #4299e1; height: 100%; width: {task['completion_rate']}%;"></div>
                        </div>
                        <small style="color: #718096;">{task['completion_rate']}% 완료</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ==================== 새 프로젝트 추가 ====================
def show_add_project():
    st.title("➕ 새 프로젝트/업무 추가")
    st.markdown("---")
    
    with st.form("add_project_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("프로젝트명 *", placeholder="예: 2024 마케팅 캠페인")
            title = st.text_input("업무 제목 *", placeholder="예: Q1 디지털 광고 전략 수립")
            description = st.text_area("업무 설명", placeholder="상세 업무 내용을 입력하세요")
            
            team_members = load_team_members()['name'].tolist()
            assignee = st.multiselect("담당자 *", options=team_members)
        
        with col2:
            category = st.selectbox("분류 *", options=["MD #1", "MD #2", "GTM", "기타"])
            status = st.selectbox("진행 현황 *", options=["진행 중", "완료", "일정 지연", "검토 중"])
            
            col2_1, col2_2, col2_3 = st.columns(3)
            with col2_1:
                planned_progress = st.slider("계획 일정 (%)", 0, 100, 0)
            with col2_2:
                actual_progress = st.slider("실제 진행 (%)", 0, 100, 0)
            with col2_3:
                completion_rate = st.slider("진척률 (%)", 0, 100, 0)
            
            deadline = st.date_input("마감일 *", value=datetime.now() + timedelta(days=30))
            approved = st.checkbox("승인됨")
        
        submitted = st.form_submit_button("✅ 프로젝트 추가", use_container_width=True)
        
        if submitted:
            if not project_name or not title or not assignee:
                st.error("필수 항목(*)을 모두 입력해주세요!")
            else:
                conn = st.session_state.db_conn
                c = conn.cursor()
                
                assignee_str = ','.join(assignee)
                
                c.execute('''
                INSERT INTO tasks (project_name, title, description, assignee, category, status,
                                 planned_progress, actual_progress, completion_rate, deadline, approved)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (project_name, title, description, assignee_str, category, status,
                      planned_progress, actual_progress, completion_rate, deadline.strftime('%Y-%m-%d'), 
                      1 if approved else 0))
                
                conn.commit()
                st.success(f"✅ '{title}' 프로젝트가 추가되었습니다!")
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
