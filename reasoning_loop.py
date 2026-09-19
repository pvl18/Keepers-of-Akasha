from concepts import get_concepts
from scenario_generator import generate_scenario
from evaluator import evaluate_answer


MAX_ATTEMPTS = 3


def give_hint(result):
    if result == "partial":
        return "You are on the right track. Try explaining more clearly why the cause you identified leads to the observed result."

    if result == "missing":
        return "Think about what changed in the scenario and how that change could cause the observed result."

    return ""


def run_reasoning_check():
    concepts = get_concepts()

    print("\nAvailable concepts:\n")

    for i, concept in enumerate(concepts, start=1):
        print(f"{i}. {concept}")

    while True:
        try:
            choice = int(input("\nChoose a concept number: "))

            if 1 <= choice <= len(concepts):
                break

            print(f"Please choose a number from 1 to {len(concepts)}.")

        except ValueError:
            print("Please enter a valid number.")

    concept = concepts[choice - 1]

    scenario = generate_scenario(concept)

    print(f"\nConcept: {concept}")
    print("\nScenario:")
    print(scenario)

    attempts = 0

    while attempts < MAX_ATTEMPTS:
        attempts += 1

        print(f"\nAttempt {attempts} of {MAX_ATTEMPTS}")

        student_answer = input("\nEnter your reasoning: ")

        result = evaluate_answer(
            concept,
            scenario,
            student_answer
        )

        print(f"\nAI Evaluation: {result}")

        if result == "strong":
            print("\nReasoning check passed.")
            return "passed"

        if attempts < MAX_ATTEMPTS:
            hint = give_hint(result)

            print("\nHint:")
            print(hint)

            print("\nTry again.")

    print("\nYou have used all 3 attempts.")
    print("Result: Flagged for professor review.")

    return "flagged"


if __name__ == "__main__":
    run_reasoning_check()