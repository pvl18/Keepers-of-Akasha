import sqlite3
from pathlib import Path
from datetime import datetime

DB_DIR = Path("data")
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "Learning_agent.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create the users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    # Create the concepts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS concepts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            difficulty TEXT,
            what_to_do TEXT
        )
    ''')
    # Create the runs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concept_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            scenario TEXT,
            expecting_reasoning TEXT,
            current_attempt integer DEFAULT 0,
            status TEXT DEFAULT 'generating',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            completed_at TEXT,
            FOREIGN KEY (concept_id) REFERENCES concepts(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    # Create the attempts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            attempt_number INTEGER NOT NULL,
            student_response TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (run_id) REFERENCES runs(id)
        )
    ''')
    #create for evaluation table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attempt_id INTEGER NOT NULL,
            quality text NOT NULL,
            reasoning text,
            hint text,
            created_at TEXT NOT NULL,
            FOREIGN KEY (attempt_id) REFERENCES attempts(id)
        )
    ''')
    # create for flags table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            reason text,
            status text DEFAULT 'pending',
            created_at TEXT NOT NULL,
            FOREIGN KEY (run_id) REFERENCES runs(id)
        )
    ''')
    # create for professors review table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS professor_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flag_id INTEGER NOT NULL,
            decision text,
            comments text,
            created_at TEXT NOT NULL,
            FOREIGN KEY (flag_id) REFERENCES flags(id)
        )
    ''')

    conn.commit()
    conn.close()

