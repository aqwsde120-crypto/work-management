# utils.py
import streamlit as st
from datetime import datetime

def load_custom_css():
    """커스텀 CSS 로드"""
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
    </style>
    """, unsafe_allow_html=True)
