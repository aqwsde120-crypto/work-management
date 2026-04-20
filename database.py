# database.py
import sqlite3
import pandas as pd
import streamlit as st

def init_db():
    """기존 프로젝트 데이터를 최대한 보호하면서 초기화"""
    conn = sqlite3.connect('projects.db', check_same_thread=False)
    c = conn.cursor()
    
    # tasks 테이블 존재 여부 확인
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
    tasks_exists = c.fetchone() is not None
    
    if tasks_exists:
        # 기존 테이블에 part 컬럼이 없으면 추가
        c.execute("PRAGMA table_info(tasks)")
        columns = [info[1] for info in c.fetchall()]
        if 'part' not in columns:
            try:
                c.execute("ALTER TABLE tasks ADD COLUMN part TEXT DEFAULT '미지정'")
                print("part 컬럼 추가 완료")
            except Exception as e:
                print(f"part 컬럼 추가 실패: {e}")
    else:
        # 테이블이 아예 없으면 새로 생성
        c.execute('''
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            assignee TEXT,
            category TEXT,
            status TEXT,
            planned_progress INTEGER DEFAULT 0,
            actual_progress INTEGER DEFAULT 0,
            completion_rate INTEGER DEFAULT 0,
            deadline DATE,
            approved INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            archived INTEGER DEFAULT 0,
            part TEXT DEFAULT '미지정'
        )
        ''')
    
    # team_members 테이블
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


def load_tasks(show_archived=False):
    conn = st.session_state.db_conn
    if show_archived:
        query = "SELECT * FROM tasks ORDER BY created_at DESC"
    else:
        query = "SELECT * FROM tasks WHERE archived = 0 ORDER BY created_at DESC"
    
    df = pd.read_sql_query(query, conn)
    if not df.empty:
        df['deadline'] = pd.to_datetime(df['deadline'], errors='coerce')
    return df


def load_team_members():
    conn = st.session_state.db_conn
    query = "SELECT * FROM team_members ORDER BY name"
    return pd.read_sql_query(query, conn)
