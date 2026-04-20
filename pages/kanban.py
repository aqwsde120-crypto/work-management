# pages/kanban.py
import streamlit as st
import pandas as pd
from config import PARTS

def show_kanban_board(df):
    """Kanban 보드 화면"""
    st.title("🗂️ Kanban 보드")
    st.markdown("---")
    
    kanban_columns = {
        "검토 중": ["검토 중"],
        "진행 중": ["진행 중"],
        "일정 지연": ["일정 지연"],
        "완료": ["완료"]
    }
    
    cols = st.columns(4)
    
    for idx, (column_name, status_list) in enumerate(kanban_columns.items()):
        with cols[idx]:
            count = len(df[df['status'].isin(status_list)])
            st.markdown(f"""
            <h3 style="text-align: center; margin-bottom: 10px;">
                {column_name} <span style="font-size: 0.9rem; color: #718096;">({count})</span>
            </h3>
            """, unsafe_allow_html=True)
            
            tasks_in_column = df[df['status'].isin(status_list)].sort_values(by='deadline')
            
            for _, task in tasks_in_column.iterrows():
                is_completed = task['status'] == "완료"
                days_left = (task['deadline'] - pd.Timestamp.now()).days
                
                if is_completed:
                    deadline_status = "✅ 완료"
                    deadline_color = "#48bb78"
                elif days_left < 0:
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
            
            if len(tasks_in_column) == 0:
                st.markdown("""
                <div style="text-align: center; padding: 40px 20px; color: #94a3b8;
                            background: #f8fafc; border-radius: 10px;">
                    업무가 없습니다
                </div>
                """, unsafe_allow_html=True)
