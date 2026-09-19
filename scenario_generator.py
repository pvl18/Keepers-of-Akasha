from concepts import get_concepts


SCENARIOS = {
    "Gram Staining": """
A student performs Gram staining on a bacterial sample.
They leave the decolorizer on for too long.
The final slide appears much paler than expected.

What do you think happened, and why did the decolorization time
affect the result?
""",

    "Thin Layer Chromatography (TLC)": """
A student separates a mixture using thin-layer chromatography.
They place the TLC plate in the solvent with the solvent level
above the sample spots.

The final separation is poor and the spots appear distorted.

What likely went wrong, and why did the position of the solvent
affect the separation?
""",

    "Fermentation": """
A student sets up a fermentation experiment using microorganisms
and a sugar-containing medium.

The experiment produces much less expected product than usual,
even though the microorganisms were added correctly.

What could explain the reduced fermentation, and what process-related
factor would you investigate first?
""",

    "Protein Purification": """
A student is purifying a protein from a biological sample.
After one purification step, most of the target protein is found
in the discarded fraction instead of the collected fraction.

What might have happened, and why could the purification conditions
cause the target protein to be lost?
""",

    "Aseptic Techniques": """
A student prepares a microbial culture using an aseptic procedure.
After incubation, unexpected microbial growth appears in a control
that should have remained uncontaminated.

What likely happened, and how could a failure in aseptic technique
lead to this result?
""",

    "Enzyme Activity Assays": """
A student performs an enzyme activity assay.
The measured enzyme activity is much lower than expected, even
though the same amount of enzyme was added as in a successful trial.

What could have caused the lower activity, and why would experimental
conditions affect the enzyme reaction?
""",

    "Microscopy": """
A student prepares a sample for microscopic observation.
The image appears blurry and important structures cannot be seen
clearly, even though the sample is present on the slide.

What could be causing the poor image quality, and how could the
microscope setup affect what the student observes?
""",

    "Spectrophotometry": """
A student measures a sample using a spectrophotometer.
The absorbance reading is unexpectedly high compared with the
expected value.

What could cause an unusually high absorbance reading, and how
could the measurement setup contribute to the result?
""",

    "Centrifugation": """
A student centrifuges a biological sample expecting the material
of interest to form a pellet.

After centrifugation, very little material is found in the pellet.

What could explain this result, and why would the centrifugation
conditions affect where the material ends up?
""",

    "pH Measurement": """
A student measures the pH of a biological solution.
The reading is very different from the expected value, even though
the solution was prepared using the correct ingredients.

What could have caused the unexpected pH reading, and why might
the measurement procedure affect the result?
"""
}


def generate_scenario(concept):
    """
    Return a scenario for the selected concept.
    """

    if concept not in get_concepts():
        return "Invalid concept selected."

    return SCENARIOS.get(
        concept,
        "No scenario is available for this concept."
    )


if __name__ == "__main__":
    concepts = get_concepts()

    print("Available concepts:\n")

    for i, concept in enumerate(concepts, start=1):
        print(f"{i}. {concept}")

    choice = int(input("\nChoose a concept number: "))

    if 1 <= choice <= len(concepts):
        selected_concept = concepts[choice - 1]

        print(f"\nSelected concept: {selected_concept}")
        print("\nScenario:")
        print(generate_scenario(selected_concept))
    else:
        print("\nInvalid choice.")
