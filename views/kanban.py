# pages/kanban.py
import streamlit as st
import pandas as pd

def show_kanban_board(df):
    """Kanban 보드 화면 - Supabase 안정 버전"""
    st.title("🗂️ Kanban 보드")
    st.markdown("---")
    
    if df.empty or 'status' not in df.columns:
        st.info("아직 등록된 프로젝트가 없습니다. '새 프로젝트/업무 추가'에서 프로젝트를 등록해주세요.")
        return
    
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
            <h3 style="text-align: center; margin-bottom: 15px;">
                {column_name} <span style="font-size: 0.9rem; color: #718096;">({count})</span>
            </h3>
            """, unsafe_allow_html=True)
            
            tasks_in_column = df[df['status'].isin(status_list)].sort_values(by='deadline', na_position='last')
            
            for _, task in tasks_in_column.iterrows():
                deadline = pd.to_datetime(task.get('deadline'))
                days_left = (deadline - pd.Timestamp.now()).days if pd.notna(deadline) else 0
                
                is_completed = task.get('status') == "완료"
                
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
                
                # 분류 배지 색상
                category = task.get('category', '미분류')
                category_color = {
                    "규제동향": "#667eea", "허가관리": "#9f7aea", "실사관리": "#ed8936",
                    "협력업체관리": "#48bb78", "자율점검": "#38b2ac", "교육관리": "#4299e1",
                    "직무관리": "#805ad5", "품질문화": "#f56565", "기타": "#718096"
                }.get(category, "#718096")
                
                st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 16px; margin-bottom: 12px; 
                            box-shadow: 0 2px 10px rgba(0,0,0,0.08); border-left: 5px solid {deadline_color};">
                    
                    <div style="display: inline-block; background: {category_color}; color: white; 
                                font-size: 0.78rem; padding: 3px 9px; border-radius: 9999px; margin-bottom: 8px;">
                        {category}
                    </div>
                    
                    <div style="font-size: 0.86rem; color: #64748b; margin-bottom: 6px;">
                        {task.get('project_name', 'Untitled')}
                    </div>
                    
                    <div style="font-weight: 600; font-size: 1.05rem; line-height: 1.35; margin-bottom: 10px;">
                        {task.get('title', '')}
                    </div>
                    
                    <div style="font-size: 0.92rem; margin-bottom: 10px; color: #475569;">
                        👤 {task.get('assignee', '미지정')}
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.86rem;">
                        <span>📅 {deadline.strftime('%Y-%m-%d') if pd.notna(deadline) else '미정'}</span>
                        <span style="color: {deadline_color}; font-weight: 600;">{deadline_status}</span>
                    </div>
                    
                    <div style="margin-top: 12px;">
                        <div style="background: #e2e8f0; height: 7px; border-radius: 9999px; overflow: hidden;">
                            <div style="background: #3b82f6; height: 100%; width: {task.get('completion_rate', 0)}%;"></div>
                        </div>
                        <div style="font-size: 0.8rem; color: #64748b; margin-top: 4px;">
                            진척률 {task.get('completion_rate', 0)}%
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if len(tasks_in_column) == 0:
                st.markdown("""
                <div style="text-align: center; padding: 50px 20px; color: #94a3b8; 
                            background: #f8fafc; border-radius: 12px; border: 2px dashed #e2e8f0;">
                    해당 상태의 업무가 없습니다
                </div>
                """, unsafe_allow_html=True)
