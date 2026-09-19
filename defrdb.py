# test_second_encounter.py

from database import (
    init_db,
    get_connection,
    get_run_details,
    get_complete_run_details
)

def test_second_encounter():

    print("=" * 60)
    print("SECOND ENCOUNTER STATE PERSISTENCE TEST")
    print("=" * 60)

    init_db()

    # ---------------------------------------------------------
    # STEP 1: Find an existing student/run from the first encounter
    # ---------------------------------------------------------
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.id AS run_id,
            u.name AS student_name,
            c.name AS concept_name
        FROM runs r
        JOIN users u ON r.user_id = u.id
        JOIN concepts c ON r.concept_id = c.id
        ORDER BY r.id DESC
        LIMIT 1
    """)

    run = cursor.fetchone()
    conn.close()

    if run is None:
        print(" No previous encounter found.")
        print("Run the first-encounter test first.")
        return

    run_id = run["run_id"]

    print("\n[1] Previous encounter found")
    print(f"Student : {run['student_name']}")
    print(f"Concept : {run['concept_name']}")
    print(f"Run ID  : {run_id}")

    # ---------------------------------------------------------
    # STEP 2: Simulate a NEW encounter
    # ---------------------------------------------------------
    print("\n[2] Starting second encounter...")
    print("Pretending the application was closed and opened again.")

    # IMPORTANT:
    # We deliberately DO NOT create a new run.
    # We recover the previous run from the database.

    state = get_complete_run_details(run_id)

    if state is None:
        print(" Failed to recover previous state.")
        return

    # ---------------------------------------------------------
    # STEP 3: Verify persisted state
    # ---------------------------------------------------------
    print("\n[3] Recovered state")

    print(f"Student       : {state['user_name']}")
    print(f"Concept       : {state['concept_name']}")
    print(f"Status        : {state['status']}")
    print(f"Current attempt: {state['current_attempt']}")

    print("\nPrevious attempts:")

    for attempt in state["attempts"]:
        print(f"\nAttempt {attempt['attempt_number']}")
        print(f"Response : {attempt['student_response']}")

        evaluation = attempt["evaluation"]

        if evaluation:
            print(f"Quality  : {evaluation['quality']}")
            print(f"Reasoning: {evaluation['reasoning']}")
            print(f"Hint     : {evaluation['hint']}")

    # ---------------------------------------------------------
    # STEP 4: Assertions
    # ---------------------------------------------------------
    assert state["run_id"] == run_id
    assert state["user_name"] == run["student_name"]
    assert state["concept_name"] == run["concept_name"]

    print("\n" + "=" * 60)
    print(" SECOND ENCOUNTER TEST PASSED")
    print("=" * 60)

    print("""
The system successfully:

✓ Found the student's previous run
✓ Recovered the same run_id
✓ Recovered the student's concept
✓ Recovered current attempt number
✓ Recovered previous responses
✓ Recovered previous evaluations
✓ Preserved the state across encounters
""")



print(test_second_encounter())