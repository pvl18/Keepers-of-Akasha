def evaluate_answer(concept, student_answer):
    """
    Evaluate the student's reasoning for the selected concept.

    Returns one of:
    - strong
    - partial
    - missing
    """

    if not student_answer.strip():
        return "missing"

    answer = student_answer.lower()

    if concept == "Gram staining":
        if "decolor" in answer and ("time" in answer or "over" in answer):
            return "strong"
        elif "stain" in answer or "decolor" in answer:
            return "partial"
        else:
            return "missing"

    if concept == "Thin-layer chromatography (TLC)":
        if "solvent" in answer or "mobile phase" in answer:
            return "strong"
        elif "spot" in answer or "separation" in answer:
            return "partial"
        else:
            return "missing"

    if concept == "Fermentation":
        if "temperature" in answer or "ph" in answer or "substrate" in answer:
            return "strong"
        elif "condition" in answer or "growth" in answer:
            return "partial"
        else:
            return "missing"

    if concept == "Microscopy":
        if "focus" in answer or "magnification" in answer:
            return "strong"
        elif "image" in answer or "lens" in answer:
            return "partial"
        else:
            return "missing"

    if concept == "Centrifugation":
        if "speed" in answer or "rpm" in answer or "time" in answer:
            return "strong"
        elif "separation" in answer or "centrifug" in answer:
            return "partial"
        else:
            return "missing"

    return "missing"


if __name__ == "__main__":
    concept = "Gram staining"

    student_answer = input("Enter the student's reasoning: ")

    result = evaluate_answer(concept, student_answer)

    print("\nEvaluation:", result)
