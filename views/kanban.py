# pages/kanban.py
import streamlit as st
import pandas as pd

def show_kanban_board(df):
    """Kanban 보드 화면 - 완료 상태는 지연 표시 안 함"""
    st.title("🗂️ Kanban 보드")
    st.markdown("---")
    
    if df.empty or 'status' not in df.columns:
        st.info("아직 등록된 프로젝트가 없습니다. 새 프로젝트를 추가해주세요.")
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
            st.subheader(f"{column_name} ({count})")
            
            tasks = df[df['status'].isin(status_list)].sort_values(by='deadline', na_position='last')
            
            for _, task in tasks.iterrows():
                with st.container(border=True):
                    # 분류
                    category = task.get('category', '미분류')
                    st.markdown(f"**{category}**")
                    
                    # 프로젝트명
                    st.caption(task.get('project_name', 'Untitled'))
                    
                    # 업무 제목
                    st.markdown(f"**{task.get('title', '')}**")
                    
                    # 담당자
                    st.write(f"👤 {task.get('assignee', '미지정')}")
                    
                    # 마감일 및 상태
                    deadline = task.get('deadline')
                    if pd.notna(deadline):
                        try:
                            deadline_dt = pd.to_datetime(deadline)
                            days_left = (deadline_dt - pd.Timestamp.now()).days
                            
                            if task.get('status') == "완료":
                                status_text = "✅ 완료"
                                status_color = "green"
                            elif days_left < 0:
                                status_text = f"🔴 지연 (D{days_left})"
                                status_color = "red"
                            elif days_left <= 7:
                                status_text = f"🟡 D-{days_left}"
                                status_color = "orange"
                            else:
                                status_text = f"🟢 D-{days_left}"
                                status_color = "green"
                                
                            st.write(f"📅 {deadline_dt.strftime('%Y-%m-%d')} **{status_text}**")
                        except:
                            st.write(f"📅 {deadline}")
                    else:
                        st.write("📅 미정")
                    
                    # 진척률
                    progress = int(task.get('completion_rate', 0))
                    st.progress(progress)
                    st.caption(f"진척률 {progress}%")
                    
                    st.divider()
            
            if len(tasks) == 0:
                st.info("해당 상태의 업무가 없습니다.")
