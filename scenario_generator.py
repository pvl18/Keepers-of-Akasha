from concepts import get_concepts


SCENARIOS = {
    "Gram Staining": {
        "scenario": """
A student performs Gram staining on a bacterial sample.
They leave the decolorizer on for too long.
The final slide appears much paler than expected.

What do you think happened, and why did the decolorization time
affect the result?
""",
        "expected_reasoning": """
The decolorizer was left on for too long, causing excessive
decolorization and removal of stain from the bacterial cells.
This can make the final slide appear much paler than expected.
"""
    },

    "Thin Layer Chromatography (TLC)": {
        "scenario": """
A student separates a mixture using thin-layer chromatography.
They place the TLC plate in the solvent with the solvent level
above the sample spots.

The final separation is poor and the spots appear distorted.

What likely went wrong, and why did the position of the solvent
affect the separation?
""",
        "expected_reasoning": """
The solvent level was above the sample spots, allowing the sample
to dissolve directly into the solvent instead of moving properly
up the TLC plate with the solvent front. This can cause poor or
distorted separation.
"""
    },

    "Fermentation": {
        "scenario": """
A student sets up a fermentation experiment using microorganisms
and a sugar-containing medium.

The experiment produces much less expected product than usual,
even though the microorganisms were added correctly.

What could explain the reduced fermentation, and what process-related
factor would you investigate first?
""",
        "expected_reasoning": """
A process condition may have reduced microbial growth or metabolic
activity, leading to lower product formation. Factors such as
temperature, pH, nutrient availability, oxygen conditions, or
fermentation time could be investigated.
"""
    },

    "Protein Purification": {
        "scenario": """
A student is purifying a protein from a biological sample.
After one purification step, most of the target protein is found
in the discarded fraction instead of the collected fraction.

What might have happened, and why could the purification conditions
cause the target protein to be lost?
""",
        "expected_reasoning": """
The target protein may not have interacted properly with the
purification medium under the conditions used. If it failed to bind
or was not retained during the purification step, it could pass into
the discarded fraction instead of the collected fraction.
"""
    },

    "Aseptic Techniques": {
        "scenario": """
A student prepares a microbial culture using an aseptic procedure.
After incubation, unexpected microbial growth appears in a control
that should have remained uncontaminated.

What likely happened, and how could a failure in aseptic technique
lead to this result?
""",
        "expected_reasoning": """
The control was likely contaminated by unwanted microorganisms.
A failure in aseptic technique could introduce contaminants during
sample handling, transfer, preparation, or exposure to the
environment.
"""
    },

    "Enzyme Activity Assays": {
        "scenario": """
A student performs an enzyme activity assay.
The measured enzyme activity is much lower than expected, even
though the same amount of enzyme was added as in a successful trial.

What could have caused the lower activity, and why would experimental
conditions affect the enzyme reaction?
""",
        "expected_reasoning": """
The enzyme may have been operating under unsuitable conditions,
such as an incorrect pH or temperature, or there may have been
problems with substrate concentration or assay conditions. These
factors can reduce enzyme activity and therefore produce a lower
measured reaction rate.
"""
    },

    "Microscopy": {
        "scenario": """
A student prepares a sample for microscopic observation.
The image appears blurry and important structures cannot be seen
clearly, even though the sample is present on the slide.

What could be causing the poor image quality, and how could the
microscope setup affect what the student observes?
""",
        "expected_reasoning": """
The microscope may not be properly focused or the optical setup
may be incorrect. Problems with focusing, objective selection,
illumination, or sample preparation can reduce image clarity and
make structures difficult to observe.
"""
    },

    "Spectrophotometry": {
        "scenario": """
A student measures a sample using a spectrophotometer.
The absorbance reading is unexpectedly high compared with the
expected value.

What could cause an unusually high absorbance reading, and how
could the measurement setup contribute to the result?
""",
        "expected_reasoning": """
The high reading could be caused by an overly concentrated sample,
contamination, an incorrect blank, or problems with the cuvette
or measurement setup. These factors can cause the measured
absorbance to be higher than expected.
"""
    },

    "Centrifugation": {
        "scenario": """
A student centrifuges a biological sample expecting the material
of interest to form a pellet.

After centrifugation, very little material is found in the pellet.

What could explain this result, and why would the centrifugation
conditions affect where the material ends up?
""",
        "expected_reasoning": """
The centrifugation conditions may not have been sufficient to
pellet the material. Centrifugal force, speed, time, sample
properties, and density differences affect whether particles
sediment into the pellet or remain in the supernatant.
"""
    },

    "pH Measurement": {
        "scenario": """
A student measures the pH of a biological solution.
The reading is very different from the expected value, even though
the solution was prepared using the correct ingredients.

What could have caused the unexpected pH reading, and why might
the measurement procedure affect the result?
""",
        "expected_reasoning": """
The unexpected reading could be caused by an improperly calibrated
pH meter, an unclean or improperly prepared electrode, or incorrect
measurement procedure. These factors can cause the measured pH to
differ from the actual pH of the solution.
"""
    }
}


def generate_scenario(concept):
    """
    Return a scenario and expected reasoning for the selected concept.
    """

    if concept not in get_concepts():
        return {
            "scenario": "Invalid concept selected.",
            "expected_reasoning": ""
        }

    return SCENARIOS.get(
        concept,
        {
            "scenario": "No scenario is available for this concept.",
            "expected_reasoning": ""
        }
    )


if __name__ == "__main__":
    concepts = get_concepts()

    print("Available concepts:\n")

    for i, concept in enumerate(concepts, start=1):
        print(f"{i}. {concept}")

    choice = int(input("\nChoose a concept number: "))

    if 1 <= choice <= len(concepts):
        selected_concept = concepts[choice - 1]

        result = generate_scenario(selected_concept)

        print(f"\nSelected concept: {selected_concept}")
        print("\nScenario:")
        print(result["scenario"])

        print("\nExpected reasoning:")
        print(result["expected_reasoning"])
    else:
        print("\nInvalid choice.")