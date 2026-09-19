# agent.py

# --------------------------------------------------
# STATES
# --------------------------------------------------

GENERATING = "generating"
AWAITING_RESPONSE = "awaiting_response"
EVALUATING = "evaluating"
PASSED = "passed"
FLAGGED = "flagged"
REVIEWED = "reviewed"


# Maximum number of student attempts
MAX_ATTEMPTS = 3


# ==================================================
# START A NEW LEARNING RUN
# ==================================================

def start_run(user_id, concept_id, concept_name):
    """
    Start a new student reasoning run.

    Flow:

    Student selects concept
            ↓
        GENERATING
            ↓
    Scenario generated
            ↓
        SQLite saves run
            ↓
    AWAITING_RESPONSE
    """

    # ------------------------------------------
    # STATE: GENERATING
    # ------------------------------------------

    from ai_engine.generator import generate_scenario

    scenario = generate_scenario(concept_name)

    # ------------------------------------------
    # CREATE PERSISTENT RUN
    # ------------------------------------------

    from database import (
        create_run,
        update_run_status,
    )

    run_id = create_run(
        user_id=user_id,
        concept_id=concept_id,
        scenario=scenario["scenario"],
        expecting_reasoning=str(
            scenario["expected_reasoning"]
        )
    )

    # ------------------------------------------
    # STATE: AWAITING_RESPONSE
    # ------------------------------------------

    update_run_status(
        run_id,
        AWAITING_RESPONSE
    )

    return run_id


# ==================================================
# SUBMIT AND EVALUATE STUDENT ANSWER
# ==================================================

def submit_answer(run_id, student_response):
    """
    Process one student answer.

    Flow:

    AWAITING_RESPONSE
            ↓
        EVALUATING
            ↓
       AI evaluation
        ↙        ↘
     PASS       RETRY
                  ↓
          HINT + RETRY
                  ↓
        AWAITING_RESPONSE

    After 3 unsuccessful attempts:
                  ↓
               FLAGGED
    """

    # ------------------------------------------
    # DATABASE FUNCTIONS
    # ------------------------------------------

    from database import (
        get_complete_run_details,
        save_attempt,
        save_evaluation,
        update_run_status,
        save_flag,
    )

    # ------------------------------------------
    # GET CURRENT RUN STATE
    # ------------------------------------------

    state = get_complete_run_details(run_id)

    if state is None:
        raise ValueError("Run not found")

    # ------------------------------------------
    # MAKE SURE STUDENT CAN ANSWER
    # ------------------------------------------

    if state["status"] != AWAITING_RESPONSE:
        raise ValueError(
            f"Run is not accepting an answer. "
            f"Current state: {state['status']}"
        )

    # ------------------------------------------
    # DETERMINE ATTEMPT NUMBER
    # ------------------------------------------

    attempt_number = state["current_attempt"] + 1

    # Safety check
    if attempt_number > MAX_ATTEMPTS:
        raise ValueError(
            "Maximum number of attempts reached."
        )

    # ------------------------------------------
    # STATE: EVALUATING
    # ------------------------------------------

    update_run_status(
        run_id,
        EVALUATING
    )

    # ------------------------------------------
    # SAVE STUDENT RESPONSE
    # ------------------------------------------

    attempt_id = save_attempt(
        run_id=run_id,
        attempt_number=attempt_number,
        student_response=student_response
    )

    # ------------------------------------------
    # GET INFORMATION NEEDED BY EVALUATOR
    # ------------------------------------------

    scenario = state["scenario"]

    expecting_reasoning = state[
        "expecting_reasoning"
    ]

    concept = state["concept_name"]

    # ------------------------------------------
    # AI EVALUATION
    # ------------------------------------------

    from ai_engine.evaluator import safe_evaluate

    evaluation = safe_evaluate(
        concept=concept,
        scenario=scenario,
        expected_reasoning=expecting_reasoning,
        student_response=student_response,
        attempt=attempt_number
    )

    # ------------------------------------------
    # SAVE AI EVALUATION
    # ------------------------------------------

    save_evaluation(
        attempt_id=attempt_id,
        quality=evaluation["quality"],
        reasoning=evaluation["reasoning"],
        hint=evaluation["hint"]
    )

    # ------------------------------------------
    # STUDENT PASSED
    # ------------------------------------------

    if evaluation["quality"] == "strong":

        update_run_status(
            run_id,
            PASSED
        )

        return {
            "status": PASSED,
            "evaluation": evaluation,
            "attempt": attempt_number
        }

    # ------------------------------------------
    # STUDENT NEEDS ANOTHER ATTEMPT
    # ------------------------------------------

    if attempt_number < MAX_ATTEMPTS:

        update_run_status(
            run_id,
            AWAITING_RESPONSE
        )

        return {
            "status": AWAITING_RESPONSE,
            "evaluation": evaluation,
            "attempt": attempt_number
        }

    # ------------------------------------------
    # 3 UNSUCCESSFUL ATTEMPTS → FLAGGED
    # ------------------------------------------

    flag_id = save_flag(
        run_id=run_id,
        reason=(
            "Student did not demonstrate "
            "sufficient reasoning after "
            "3 attempts."
        )
    )

    update_run_status(
        run_id,
        FLAGGED
    )

    return {
        "status": FLAGGED,
        "evaluation": evaluation,
        "attempt": attempt_number,
        "flag_id": flag_id
    }


# ==================================================
# RESUME AN EXISTING RUN
# ==================================================

def resume_run(run_id):
    """
    Retrieve the current state of an existing run.

    The database returns:
    - run information
    - current attempt
    - previous attempts
    - evaluations
    - hints

    This allows the application to resume
    an existing reasoning run.
    """

    from database import get_complete_run_details

    state = get_complete_run_details(run_id)

    if state is None:
        raise ValueError("Run not found")

    return state