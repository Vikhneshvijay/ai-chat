import os
from typing import List, Dict, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/ai_chat")

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id SERIAL PRIMARY KEY,
            session_id VARCHAR(255) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            session_id VARCHAR(255) NOT NULL,
            role VARCHAR(50) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def session_exists(session_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id FROM chat_sessions WHERE session_id = %s",
            (session_id,)
        )
        return cursor.fetchone() is not None
    finally:
        cursor.close()
        conn.close()

def create_session(session_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO chat_sessions (session_id) VALUES (%s)",
            (session_id,)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def save_message(session_id: str, role: str, content: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (%s, %s, %s)",
            (session_id, role, content)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def get_messages(session_id: str) -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            "SELECT role, content, created_at FROM messages WHERE session_id = %s ORDER BY created_at",
            (session_id,)
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def delete_session(session_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM messages WHERE session_id = %s", (session_id,))
        cursor.execute("DELETE FROM chat_sessions WHERE session_id = %s", (session_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
