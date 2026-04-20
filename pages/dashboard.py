# pages/dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def show_dashboard(df):
    """대시보드 화면"""
    st.title("📊 대시보드")
    st.markdown("---")
    
    # 주요 메트릭
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
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
        avg_progress = df['completion_rate'].mean() if not df.empty else 0
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
            fig.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("담당자 데이터가 없습니다.")
    
    with col2:
        st.subheader("📈 상태별 분포")
        status_counts = df['status'].value_counts()
        colors = {'진행 중': '#4299e1', '완료': '#48bb78', '일정 지연': '#f56565', '검토 중': '#ed8936'}
        
        fig = go.Figure(data=[go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=.4,
            marker_colors=[colors.get(status, '#999') for status in status_counts.index]
        )])
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)
    
    # 지연 프로젝트
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
