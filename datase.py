import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_DIR = Path("data")
DB_DIR.mkdir(exist_ok=True)

DB_PATH = DB_DIR / "Learning_agent.db"


# ============================================================
# DATABASE INTERFACE
# ============================================================

class LearningAgentDatabase(ABC):

    @abstractmethod
    def create_user(self, name):
        """Create and return a user ID."""

    @abstractmethod
    def create_concept(self, name, difficulty, what_to_do):
        """Create and return a concept ID."""

    @abstractmethod
    def create_run(self, concept_id, user_id, scenario, expecting_reasoning):
        """Create and return a run ID."""

    @abstractmethod
    def save_attempt(self, run_id, attempt_number, student_response):
        """Save a student attempt and return its ID."""

    @abstractmethod
    def save_evaluation(self, attempt_id, quality, reasoning, hint):
        """Save evaluation feedback and return its ID."""

    @abstractmethod
    def update_run_status(self, run_id, status):
        """Update the status of a run."""

    @abstractmethod
    def save_flag(self, run_id, reason):
        """Flag a run for professor review."""

    @abstractmethod
    def get_flagged_students(self):
        """Return pending flagged students."""

    @abstractmethod
    def save_professor_review(self, flag_id, decision, comments):
        """Save professor review."""

    @abstractmethod
    def get_run_details(self, run_id):
        """Return summary information for a run."""

    @abstractmethod
    def get_complete_run_details(self, run_id):
        """Return complete run information including attempts/evaluations."""


# ============================================================
# SQLITE DATABASE IMPLEMENTATION
# ============================================================

class SQLiteLearningAgentDatabase(LearningAgentDatabase):

    def __init__(self, db_path=DB_PATH):
        self.db_path = Path(db_path)

        # Create parent directory if required
        self.db_path.parent.mkdir(exist_ok=True, parents=True)

        # Initialize THIS database
        self.init_db()

    # --------------------------------------------------------
    # CONNECTION
    # --------------------------------------------------------

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")

        return conn

    # --------------------------------------------------------
    # INITIALIZE DATABASE
    # --------------------------------------------------------

    def init_db(self):

        conn = self.get_connection()
        cursor = conn.cursor()

        # ====================================================
        # USERS
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        # ====================================================
        # CONCEPTS
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS concepts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                difficulty TEXT,
                what_to_do TEXT
            )
        """)

        # ====================================================
        # RUNS
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                concept_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,

                scenario TEXT,
                expecting_reasoning TEXT,

                current_attempt INTEGER DEFAULT 0,

                status TEXT DEFAULT 'generating',

                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                completed_at TEXT,

                FOREIGN KEY (concept_id)
                    REFERENCES concepts(id),

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
            )
        """)

        # ====================================================
        # ATTEMPTS
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                run_id INTEGER NOT NULL,

                attempt_number INTEGER NOT NULL,

                student_response TEXT,

                created_at TEXT NOT NULL,

                FOREIGN KEY (run_id)
                    REFERENCES runs(id),

                UNIQUE(run_id, attempt_number)
            )
        """)

        # ====================================================
        # EVALUATIONS
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                attempt_id INTEGER NOT NULL,

                quality TEXT NOT NULL,
                reasoning TEXT,
                hint TEXT,

                created_at TEXT NOT NULL,

                FOREIGN KEY (attempt_id)
                    REFERENCES attempts(id)
            )
        """)

        # ====================================================
        # FLAGS
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS flags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                run_id INTEGER NOT NULL,

                reason TEXT,

                status TEXT DEFAULT 'pending',

                created_at TEXT NOT NULL,

                FOREIGN KEY (run_id)
                    REFERENCES runs(id)
            )
        """)

        # ====================================================
        # PROFESSOR REVIEWS
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS professor_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                flag_id INTEGER NOT NULL,

                decision TEXT,
                comments TEXT,

                created_at TEXT NOT NULL,

                FOREIGN KEY (flag_id)
                    REFERENCES flags(id)
            )
        """)

        conn.commit()
        conn.close()

    # ========================================================
    # USER
    # ========================================================

    def create_user(self, name):

        conn = self.get_connection()
        cursor = conn.cursor()

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

    # ========================================================
    # CONCEPT
    # ========================================================

    def create_concept(self, name, difficulty, what_to_do):

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO concepts
            (name, difficulty, what_to_do)
            VALUES (?, ?, ?)
            """,
            (
                name,
                difficulty,
                what_to_do
            )
        )

        concept_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return concept_id

    # ========================================================
    # CREATE RUN
    # ========================================================

    def create_run(
        self,
        concept_id,
        user_id,
        scenario,
        expecting_reasoning
    ):

        conn = self.get_connection()
        cursor = conn.cursor()

        created_at = datetime.now().isoformat()

        cursor.execute(
            """
            INSERT INTO runs (
                concept_id,
                user_id,
                scenario,
                expecting_reasoning,
                created_at,
                updated_at,
                status,
                current_attempt
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                concept_id,
                user_id,
                scenario,
                expecting_reasoning,
                created_at,
                created_at,
                "generating",
                0
            )
        )

        run_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return run_id

    # ========================================================
    # SAVE ATTEMPT
    # ========================================================

    def save_attempt(
        self,
        run_id,
        attempt_number,
        student_response
    ):

        conn = self.get_connection()
        cursor = conn.cursor()

        created_at = datetime.now().isoformat()

        # Insert attempt
        cursor.execute(
            """
            INSERT INTO attempts (
                run_id,
                attempt_number,
                student_response,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                run_id,
                attempt_number,
                student_response,
                created_at
            )
        )

        attempt_id = cursor.lastrowid

        # Update run state
        cursor.execute(
            """
            UPDATE runs
            SET
                current_attempt = ?,
                status = 'in_progress',
                updated_at = ?
            WHERE id = ?
            """,
            (
                attempt_number,
                created_at,
                run_id
            )
        )

        conn.commit()
        conn.close()

        return attempt_id

    # ========================================================
    # SAVE EVALUATION
    # ========================================================

    def save_evaluation(
        self,
        attempt_id,
        quality,
        reasoning,
        hint
    ):

        conn = self.get_connection()
        cursor = conn.cursor()

        created_at = datetime.now().isoformat()

        cursor.execute(
            """
            INSERT INTO evaluations (
                attempt_id,
                quality,
                reasoning,
                hint,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                attempt_id,
                quality,
                reasoning,
                hint,
                created_at
            )
        )

        evaluation_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return evaluation_id

    # ========================================================
    # UPDATE RUN STATUS
    # ========================================================

    def update_run_status(self, run_id, status):

        conn = self.get_connection()
        cursor = conn.cursor()

        updated_at = datetime.now().isoformat()

        # Statuses that mean the run is finished
        completed_statuses = {
            "passed",
            "completed",
            "failed",
            "flagged"
        }

        if status in completed_statuses:

            cursor.execute(
                """
                UPDATE runs
                SET
                    status = ?,
                    updated_at = ?,
                    completed_at = ?
                WHERE id = ?
                """,
                (
                    status,
                    updated_at,
                    updated_at,
                    run_id
                )
            )

        else:

            cursor.execute(
                """
                UPDATE runs
                SET
                    status = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    status,
                    updated_at,
                    run_id
                )
            )

        conn.commit()
        conn.close()

    # ========================================================
    # SAVE FLAG
    # ========================================================

    def save_flag(self, run_id, reason):

        conn = self.get_connection()
        cursor = conn.cursor()

        created_at = datetime.now().isoformat()

        # Create flag
        cursor.execute(
            """
            INSERT INTO flags (
                run_id,
                reason,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                run_id,
                reason,
                "pending",
                created_at
            )
        )

        flag_id = cursor.lastrowid

        # Update run status
        cursor.execute(
            """
            UPDATE runs
            SET
                status = 'flagged',
                updated_at = ?,
                completed_at = ?
            WHERE id = ?
            """,
            (
                created_at,
                created_at,
                run_id
            )
        )

        conn.commit()
        conn.close()

        return flag_id

    # ========================================================
    # GET FLAGGED STUDENTS
    # ========================================================

    def get_flagged_students(self):

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                f.id AS flag_id,

                f.run_id,

                f.reason AS flag_reason,

                f.status AS flag_status,

                f.created_at AS flag_created_at,

                u.id AS user_id,

                u.name AS user_name,

                c.id AS concept_id,

                c.name AS concept_name,

                c.difficulty,

                r.status AS run_status,

                r.current_attempt,

                r.scenario,

                r.expecting_reasoning

            FROM flags f

            JOIN runs r
                ON f.run_id = r.id

            JOIN users u
                ON r.user_id = u.id

            JOIN concepts c
                ON r.concept_id = c.id

            WHERE f.status = 'pending'

            ORDER BY f.created_at DESC
            """
        )

        flagged_students = cursor.fetchall()

        conn.close()

        return [
            dict(student)
            for student in flagged_students
        ]

    # ========================================================
    # PROFESSOR REVIEW
    # ========================================================

    def save_professor_review(
        self,
        flag_id,
        decision,
        comments
    ):

        conn = self.get_connection()
        cursor = conn.cursor()

        created_at = datetime.now().isoformat()

        # Get associated run
        cursor.execute(
            """
            SELECT run_id
            FROM flags
            WHERE id = ?
            """,
            (flag_id,)
        )

        flag = cursor.fetchone()

        if flag is None:
            conn.close()
            raise ValueError(
                f"Flag with ID {flag_id} does not exist."
            )

        run_id = flag["run_id"]

        # Save professor review
        cursor.execute(
            """
            INSERT INTO professor_reviews (
                flag_id,
                decision,
                comments,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                flag_id,
                decision,
                comments,
                created_at
            )
        )

        review_id = cursor.lastrowid

        # Update flag and run based on decision
        if decision == "approve":

            flag_status = "resolved"
            run_status = "completed"

        elif decision == "reject":

            flag_status = "rejected"
            run_status = "in_progress"

        else:

            # Unknown/custom decision
            flag_status = "reviewed"
            run_status = "flagged"

        cursor.execute(
            """
            UPDATE flags
            SET status = ?
            WHERE id = ?
            """,
            (
                flag_status,
                flag_id
            )
        )

        cursor.execute(
            """
            UPDATE runs
            SET
                status = ?,
                updated_at = ?,
                completed_at = CASE
                    WHEN ? = 'completed'
                    THEN ?
                    ELSE completed_at
                END
            WHERE id = ?
            """,
            (
                run_status,
                created_at,
                run_status,
                created_at,
                run_id
            )
        )

        conn.commit()
        conn.close()

        return review_id

    # ========================================================
    # GET RUN DETAILS
    # ========================================================

    def get_run_details(self, run_id):

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT

                r.id AS run_id,

                r.scenario,

                r.expecting_reasoning,

                r.status,

                r.current_attempt,

                r.created_at,

                r.updated_at,

                r.completed_at,

                u.id AS user_id,

                u.name AS user_name,

                c.id AS concept_id,

                c.name AS concept_name,

                c.difficulty,

                c.what_to_do

            FROM runs r

            JOIN users u
                ON r.user_id = u.id

            JOIN concepts c
                ON r.concept_id = c.id

            WHERE r.id = ?
            """,
            (run_id,)
        )

        run_details = cursor.fetchone()

        conn.close()

        return (
            dict(run_details)
            if run_details
            else None
        )

    # ========================================================
    # GET COMPLETE RUN DETAILS
    # ========================================================

    def get_complete_run_details(self, run_id):

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT

                r.id AS run_id,

                r.scenario,

                r.expecting_reasoning,

                r.status,

                r.current_attempt,

                r.created_at,

                r.updated_at,

                r.completed_at,

                u.id AS user_id,

                u.name AS user_name,

                c.id AS concept_id,

                c.name AS concept_name,

                c.difficulty,

                c.what_to_do,

                a.id AS attempt_id,

                a.attempt_number,

                a.student_response,

                a.created_at AS attempt_created_at,

                e.id AS evaluation_id,

                e.quality,

                e.reasoning,

                e.hint,

                e.created_at AS evaluation_created_at

            FROM runs r

            JOIN users u
                ON r.user_id = u.id

            JOIN concepts c
                ON r.concept_id = c.id

            LEFT JOIN attempts a
                ON r.id = a.run_id

            LEFT JOIN evaluations e
                ON a.id = e.attempt_id

            WHERE r.id = ?

            ORDER BY a.attempt_number ASC
            """,
            (run_id,)
        )

        rows = cursor.fetchall()

        conn.close()

        if not rows:
            return None

        # ----------------------------------------------------
        # RUN INFORMATION
        # ----------------------------------------------------

        first_row = rows[0]

        run_info = {
            "run_id": first_row["run_id"],

            "scenario": first_row["scenario"],

            "expecting_reasoning":
                first_row["expecting_reasoning"],

            "status": first_row["status"],

            "current_attempt":
                first_row["current_attempt"],

            "created_at":
                first_row["created_at"],

            "updated_at":
                first_row["updated_at"],

            "completed_at":
                first_row["completed_at"],

            "user_id":
                first_row["user_id"],

            "user_name":
                first_row["user_name"],

            "concept_id":
                first_row["concept_id"],

            "concept_name":
                first_row["concept_name"],

            "difficulty":
                first_row["difficulty"],

            "what_to_do":
                first_row["what_to_do"],

            "attempts": []
        }

        # ----------------------------------------------------
        # ATTEMPTS
        # ----------------------------------------------------

        for row in rows:

            if row["attempt_id"] is None:
                continue

            attempt_info = {

                "attempt_id":
                    row["attempt_id"],

                "attempt_number":
                    row["attempt_number"],

                "student_response":
                    row["student_response"],

                "created_at":
                    row["attempt_created_at"],

                "evaluation": None
            }

            # Add evaluation if one exists
            if row["evaluation_id"] is not None:

                attempt_info["evaluation"] = {

                    "evaluation_id":
                        row["evaluation_id"],

                    "quality":
                        row["quality"],

                    "reasoning":
                        row["reasoning"],

                    "hint":
                        row["hint"],

                    "created_at":
                        row["evaluation_created_at"]
                }

            run_info["attempts"].append(
                attempt_info
            )

        return run_info


# ============================================================
# BACKWARD-COMPATIBILITY FUNCTIONS
# ============================================================
#
# These allow existing code that currently does:
#
#     import database
#     database.create_user(...)
#
# to continue working.
#
# New code can instead use:
#
#     db = SQLiteLearningAgentDatabase()
#     db.create_user(...)
#
# ============================================================

_default_db = SQLiteLearningAgentDatabase()


def get_connection():
    return _default_db.get_connection()


def init_db():
    _default_db.init_db()


def create_user(name):
    return _default_db.create_user(name)


def create_concept(name, difficulty, what_to_do):
    return _default_db.create_concept(
        name,
        difficulty,
        what_to_do
    )


def create_run(
    concept_id,
    user_id,
    scenario,
    expecting_reasoning
):
    return _default_db.create_run(
        concept_id,
        user_id,
        scenario,
        expecting_reasoning
    )


def save_attempt(
    run_id,
    attempt_number,
    student_response
):
    return _default_db.save_attempt(
        run_id,
        attempt_number,
        student_response
    )


def save_evaluation(
    attempt_id,
    quality,
    reasoning,
    hint
):
    return _default_db.save_evaluation(
        attempt_id,
        quality,
        reasoning,
        hint
    )


def update_run_status(run_id, status):
    return _default_db.update_run_status(
        run_id,
        status
    )


def save_flag(run_id, reason):
    return _default_db.save_flag(
        run_id,
        reason
    )


def get_flagged_students():
    return _default_db.get_flagged_students()


def save_professor_review(
    flag_id,
    decision,
    comments
):
    return _default_db.save_professor_review(
        flag_id,
        decision,
        comments
    )


def get_run_details(run_id):
    return _default_db.get_run_details(run_id)


def get_complete_run_details(run_id):
    return _default_db.get_complete_run_details(run_id)


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print("Database initialized successfully.")

    print(f"Database path: {DB_PATH}")

    print("Tables are ready for the learning-agent workflow.")
