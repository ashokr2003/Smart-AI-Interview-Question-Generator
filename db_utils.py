# db_utils.py
import sqlite3

def init_db():
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_role TEXT,
            topic TEXT,
            question TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_questions(job_role, topic, questions):
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    for q in questions:
        cursor.execute("INSERT INTO questions (job_role, topic, question) VALUES (?, ?, ?)", 
                       (job_role, topic, q))
    conn.commit()
    conn.close()

def fetch_recent_questions(limit=20):
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT job_role, topic, question FROM questions ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows
