from presidio_analyzer import PatternRecognizer, Pattern

recognizers = [
    PatternRecognizer(
        supported_entity="IN_PAN",
        name="PANRecognizer",
        patterns=[
            Pattern(name="pan_number", regex=r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", score=0.9),
        ],
        context=["pan", "income tax", "financial", "id"],
    ),
]
