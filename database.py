import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime

DB_DIR = Path("data")
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "Learning_agent.db"


class LearningAgentDatabase(ABC):
    @abstractmethod
    def create_user(self, name):
        """Create and return a user id for the supplied name."""

    @abstractmethod
    def create_concept(self, name, difficulty, what_to_do):
        """Create and return a concept id for the supplied concept."""

    @abstractmethod
    def create_run(self, concept_id, user_id, scenario, expecting_reasoning):
        """Create a new run and return its id."""

    @abstractmethod
    def save_attempt(self, run_id, attempt_number, student_response):
        """Persist a student attempt and return its new id."""

    @abstractmethod
    def save_evaluation(self, attempt_id, quality, reasoning, hint):
        """Store evaluation feedback for an attempt and return its id."""

    @abstractmethod
    def update_run_status(self, run_id, status):
        """Update the status of the run."""

    @abstractmethod
    def save_flag(self, run_id, reason):
        """Create a flag for a run and return the new flag id."""

    @abstractmethod
    def get_flagged_students(self):
        """Return pending flagged students in reverse chronological order."""

    @abstractmethod
    def save_professor_review(self, flag_id, decision, comments):
        """Save a professor review for a flagged submission."""

    @abstractmethod
    def get_run_details(self, run_id):
        """Return a single run's summary fields."""

    @abstractmethod
    def get_complete_run_details(self, run_id):
        """Return the full run context including attempts and feedback."""


class SQLiteLearningAgentDatabase(LearningAgentDatabase):
    def __init__(self, db_path=DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True, parents=True)
        init_db()

    def create_user(self, name):
        return create_user(name)

    def create_concept(self, name, difficulty, what_to_do):
        return create_concept(name, difficulty, what_to_do)

    def create_run(self, concept_id, user_id, scenario, expecting_reasoning):
        return create_run(concept_id, user_id, scenario, expecting_reasoning)

    def save_attempt(self, run_id, attempt_number, student_response):
        return save_attempt(run_id, attempt_number, student_response)

    def save_evaluation(self, attempt_id, quality, reasoning, hint):
        return save_evaluation(attempt_id, quality, reasoning, hint)

    def update_run_status(self, run_id, status):
        update_run_status(run_id, status)

    def save_flag(self, run_id, reason):
        return save_flag(run_id, reason)

    def get_flagged_students(self):
        return get_flagged_students()

    def save_professor_review(self, flag_id, decision, comments):
        return save_professor_review(flag_id, decision, comments)

    def get_run_details(self, run_id):
        return get_run_details(run_id)

    def get_complete_run_details(self, run_id):
        return get_complete_run_details(run_id)



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
            created_at TEXT NOT NULL,
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

#add user function
def create_user(name):
    conn = get_connection()
    cursor = conn.cursor()

    # Check whether the user already exists
    cursor.execute(
        "SELECT id FROM users WHERE name = ?",
        (name,)
    )

    existing_user = cursor.fetchone()

    if existing_user is not None:
        user_id = existing_user["id"]
        conn.close()
        return user_id

    # Create a new user if one does not exist
    created_at = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO users (name, created_at)
        VALUES (?, ?)
        """,
        (name, created_at)
    )

    user_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return user_id


def create_concept(name, difficulty, what_to_do):
    conn = get_connection()
    cursor = conn.cursor()

    # Check whether the concept already exists
    cursor.execute(
        "SELECT id FROM concepts WHERE name = ?",
        (name,)
    )

    existing_concept = cursor.fetchone()

    if existing_concept is not None:
        concept_id = existing_concept["id"]
        conn.close()
        return concept_id

    # Create a new concept if one does not exist
    created_at = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO concepts (
            name,
            difficulty,
            what_to_do,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            name,
            difficulty,
            what_to_do,
            created_at
        )
    )

    concept_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return concept_id

#add run function
def create_run(concept_id, user_id, scenario, expecting_reasoning):
    conn = get_connection()
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    updated_at = created_at
    cursor.execute('''INSERT INTO runs (concept_id, user_id, scenario, expecting_reasoning, created_at, updated_at, status, current_attempt) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (concept_id, user_id, scenario, expecting_reasoning, created_at, updated_at, 'generating', 0))
    run_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return run_id
#add attempt function
def save_attempt(run_id, attempt_number, student_response):
    conn = get_connection()
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    cursor.execute('''INSERT INTO attempts (run_id, attempt_number, student_response, created_at) VALUES (?, ?, ?, ?)''', (run_id, attempt_number, student_response, created_at))
    attempt_id = cursor.lastrowid
    # update the current_attempt in runs table
    cursor.execute('''UPDATE runs SET current_attempt = ?, status = 'in_progress', updated_at = ? WHERE id = ?''', (attempt_number, datetime.now().isoformat(), run_id))
    conn.commit()
    conn.close()
    return attempt_id

#evaluation function
def save_evaluation(attempt_id, quality, reasoning, hint):
    conn = get_connection()
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    cursor.execute('''INSERT INTO evaluations (attempt_id, quality, reasoning, hint, created_at) VALUES (?, ?, ?, ?, ?)''', (attempt_id, quality, reasoning, hint, created_at))
    evaluation_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return evaluation_id


#update run status function
def update_run_status(run_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    updated_at = datetime.now().isoformat()
    cursor.execute('''UPDATE runs SET status = ?, updated_at = ? WHERE id = ?''', (status, updated_at, run_id))
    conn.commit()
    conn.close()

#flag function
def save_flag(run_id, reason):
    conn = get_connection()
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    cursor.execute('''INSERT INTO flags (run_id, reason,status ,created_at) VALUES (?, ?, ?, ?)''', (run_id, reason, 'pending', created_at))
    flag_id = cursor.lastrowid
    conn.execute('''UPDATE runs SET status = 'flagged', updated_at = ? WHERE id = ?''', (datetime.now().isoformat(), run_id))
    conn.commit()
    conn.close()
    return flag_id

#flagged students
def get_flagged_students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            f.id AS flag_id,
            f.run_id,
            u.name AS student_name,
            c.name AS concept_name,
            f.reason,
            f.status,
            f.created_at
        FROM flags f
        JOIN runs r ON f.run_id = r.id
        JOIN users u ON r.user_id = u.id
        JOIN concepts c ON r.concept_id = c.id
        WHERE f.status = 'pending'
        ORDER BY f.created_at DESC
    ''')

    flagged_students = cursor.fetchall()
    conn.close()

    return [dict(student) for student in flagged_students]

#professor review function
def save_professor_review(flag_id, decision, comments):
    conn = get_connection()
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    cursor.execute('''INSERT INTO professor_reviews (flag_id, decision, comments, created_at) VALUES (?, ?, ?, ?)''', (flag_id, decision, comments, created_at))
    review_id = cursor.lastrowid
    # update the status of the flag based on the professor's decision
    new_status = 'resolved' if decision == 'approve' else 'rejected'
    cursor.execute('''UPDATE flags SET status = ? WHERE id = ?''', (new_status, flag_id))
    conn.commit()
    conn.close()
    return review_id

#get run details function
def get_run_details(run_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT r.id as run_id, r.scenario, r.expecting_reasoning, r.status, r.current_attempt, r.created_at, r.updated_at, r.completed_at,
                      u.name as user_name, c.name as concept_name, c.difficulty, c.what_to_do
                      FROM runs r
                      JOIN users u ON r.user_id = u.id
                      JOIN concepts c ON r.concept_id = c.id
                      WHERE r.id = ?''', (run_id,))
    run_details = cursor.fetchone()
    conn.close()
    return dict(run_details) if run_details else None

#get complete run details function
def get_complete_run_details(run_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT r.id as run_id, r.scenario, r.expecting_reasoning, r.status, r.current_attempt, r.created_at, r.updated_at, r.completed_at,
                      u.name as user_name, c.name as concept_name, c.difficulty, c.what_to_do,
                      a.id as attempt_id, a.attempt_number, a.student_response, a.created_at as attempt_created_at,
                      e.id as evaluation_id, e.quality, e.reasoning, e.hint, e.created_at as evaluation_created_at
                      FROM runs r
                      JOIN users u ON r.user_id = u.id
                      JOIN concepts c ON r.concept_id = c.id
                      LEFT JOIN attempts a ON r.id = a.run_id
                      LEFT JOIN evaluations e ON a.id = e.attempt_id
                      WHERE r.id = ?''', (run_id,))
    run_details = cursor.fetchall()
    conn.close()

    if not run_details:
        return None

    # Organize the data into a structured format
    run_info = {
        "run_id": run_details[0]["run_id"],
        "scenario": run_details[0]["scenario"],
        "expecting_reasoning": run_details[0]["expecting_reasoning"],
        "status": run_details[0]["status"],
        "current_attempt": run_details[0]["current_attempt"],
        "created_at": run_details[0]["created_at"],
        "updated_at": run_details[0]["updated_at"],
        "completed_at": run_details[0]["completed_at"],
        "user_name": run_details[0]["user_name"],
        "concept_name": run_details[0]["concept_name"],
        "difficulty": run_details[0]["difficulty"],
        "what_to_do": run_details[0]["what_to_do"],
        "attempts": []
    }

    for row in run_details:
        if row["attempt_id"] is not None:
            attempt_info = {
                "attempt_id": row["attempt_id"],
                "attempt_number": row["attempt_number"],
                "student_response": row["student_response"],
                "created_at": row["attempt_created_at"],
                "evaluation": {
                    "evaluation_id": row["evaluation_id"],
                    "quality": row["quality"],
                    "reasoning": row["reasoning"],
                    "hint": row["hint"],
                    "created_at": row["evaluation_created_at"]
                } if row["evaluation_id"] is not None else None
            }
            run_info["attempts"].append(attempt_info)

    return run_info