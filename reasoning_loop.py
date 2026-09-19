from concepts import get_concepts
from scenario_generator import generate_scenario
from evaluator import safe_evaluate

from database import (
    init_db,
    create_user,
    create_concept,
    create_run,
    save_attempt,
    save_evaluation,
    update_run_status,
    save_flag
)


MAX_ATTEMPTS = 3


def run_reasoning_check():
    init_db()

    # ------------------------------------------
    # STUDENT
    # ------------------------------------------

    student_name = input("\nEnter student name: ").strip()

    if not student_name:
        student_name = "Demo Student"

    # ------------------------------------------
    # CONCEPT SELECTION
    # ------------------------------------------

    concepts = get_concepts()

    print("\nAvailable concepts:\n")

    for i, concept in enumerate(concepts, start=1):
        print(f"{i}. {concept}")

    while True:
        try:
            choice = int(
                input("\nChoose a concept number: ")
            )

            if 1 <= choice <= len(concepts):
                break

            print(
                f"Please choose a number from "
                f"1 to {len(concepts)}."
            )

        except ValueError:
            print("Please enter a valid number.")

    concept = concepts[choice - 1]

    # ------------------------------------------
    # GENERATE SCENARIO
    # ------------------------------------------

    scenario_data = generate_scenario(concept)

    scenario = scenario_data["scenario"]
    expected_reasoning = scenario_data["expected_reasoning"]

    print(f"\nConcept: {concept}")

    print("\nScenario:")
    print(scenario)

    # ------------------------------------------
    # CREATE DATABASE RECORDS
    # ------------------------------------------

    user_id = create_user(student_name)

    concept_id = create_concept(
        concept,
        "medium",
        "Explain the reasoning behind the observed result."
    )

    run_id = create_run(
        concept_id,
        user_id,
        scenario,
        expected_reasoning
    )

    update_run_status(
        run_id,
        "awaiting_response"
    )

    print(f"\nRun created. Run ID: {run_id}")

    # ------------------------------------------
    # REASONING LOOP
    # ------------------------------------------

    attempts = 0

    while attempts < MAX_ATTEMPTS:
        attempts += 1

        print(
            f"\nAttempt {attempts} "
            f"of {MAX_ATTEMPTS}"
        )

        student_answer = input(
            "\nEnter your reasoning: "
        )

        # --------------------------------------
        # SAVE STUDENT ATTEMPT
        # --------------------------------------

        attempt_id = save_attempt(
            run_id,
            attempts,
            student_answer
        )

        update_run_status(
            run_id,
            "evaluating"
        )

        # --------------------------------------
        # AI EVALUATION
        # --------------------------------------

        evaluation = safe_evaluate(
            concept=concept,
            scenario=scenario,
            expected_reasoning=expected_reasoning,
            student_response=student_answer,
            attempt=attempts
        )

        quality = evaluation["quality"]
        reasoning = evaluation["reasoning"]
        hint = evaluation["hint"]

        print(
            f"\nAI Evaluation: {quality}"
        )

        print(
            f"Reasoning: {reasoning}"
        )

        # --------------------------------------
        # SAVE EVALUATION
        # --------------------------------------

        save_evaluation(
            attempt_id,
            quality,
            reasoning,
            hint
        )

        # --------------------------------------
        # PASSED
        # --------------------------------------

        if quality == "strong":
            update_run_status(
                run_id,
                "passed"
            )

            print(
                "\nReasoning check passed."
            )

            print(
                f"Run {run_id} saved successfully."
            )

            return "passed"

        # --------------------------------------
        # RETRY
        # --------------------------------------

        if attempts < MAX_ATTEMPTS:
            update_run_status(
                run_id,
                "awaiting_response"
            )

            if hint:
                print("\nHint:")
                print(hint)

            print("\nTry again.")

    # ------------------------------------------
    # FLAG AFTER 3 UNSUCCESSFUL ATTEMPTS
    # ------------------------------------------

    print(
        "\nYou have used all 3 attempts."
    )

    flag_id = save_flag(
        run_id,
        (
            "Student did not demonstrate "
            "strong reasoning after 3 attempts."
        )
    )

    print(
        "Result: Flagged for professor review."
    )

    print(
        f"Flag ID: {flag_id}"
    )

    print(
        f"Run {run_id} saved successfully."
    )

    return "flagged"


if __name__ == "__main__":
    run_reasoning_check()

