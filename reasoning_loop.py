from evaluator import evaluate_answer


def get_hint(concept, result):
    """
    Give a small hint based on the evaluation result.
    """

    if result == "partial":
        return f"Think about which step or condition in {concept} could have caused the unexpected result."

    if result == "missing":
        return f"Focus on the main scientific reason behind what happened in the {concept} experiment."

    return ""


def run_reasoning_loop(concept, scenario):
    """
    Run the student reasoning loop.

    The student gets up to 3 attempts.
    A strong answer passes immediately.
    After 3 unsuccessful attempts, the student is flagged.
    """

    print("\nScenario:")
    print(scenario)

    for attempt in range(1, 4):

        print(f"\nAttempt {attempt} of 3")
        student_answer = input("Your reasoning: ")

        result = evaluate_answer(concept, student_answer)

        print("Evaluation:", result)

        if result == "strong":
            print("\nPassed! Your reasoning shows a strong understanding.")
            return "passed"

        if attempt < 3:
            hint = get_hint(concept, result)
            print("\nHint:", hint)

        else:
            print("\nThree unsuccessful attempts.")
            print("This attempt will be flagged for professor review.")
            return "flagged"


if __name__ == "__main__":
    concept = "Gram staining"

    scenario = """
A student performs Gram staining on a bacterial sample.
They leave the decolorizer on for too long.
The final slide appears much paler than expected.

What do you think happened, and why did the decolorization time
affect the result?
"""

    result = run_reasoning_loop(concept, scenario)

    print("\nFinal status:", result)
