```python
def generate_scenario(concept):
    scenarios = {
        "Gram staining": """
A student performs Gram staining on a bacterial sample.
They follow the staining steps but leave the decolorizer on for too long.
The final slide appears much paler than expected.

What do you think happened, and why did the decolorization time affect the result?
""",

        "Thin-layer chromatography (TLC)": """
A student uses TLC to separate compounds in a sample.
After developing the plate, the spots are very close to the starting line.

What could have caused this result, and what would you change in the experiment?
""",

        "Fermentation": """
A student sets up a fermentation experiment, but very little product is
formed compared with what they expected.

What factors could explain the result, and how would you reason about the
possible cause?
""",

        "Microscopy": """
A student prepares a sample for microscopic observation, but the image is
blurry and important structures cannot be identified clearly.

What could have caused this problem, and what would you check first?
""",

        "Centrifugation": """
A student centrifuges a biological sample, but the expected separation
between the components is not clearly visible.

What might have gone wrong, and how would you determine the likely cause?
"""
    }

    return scenarios.get(
        concept,
        "No scenario is available for this concept."
    )


if __name__ == "__main__":
    concept = "Gram staining"

    scenario = generate_scenario(concept)

    print("Generated Scenario:")
    print(scenario)
```
