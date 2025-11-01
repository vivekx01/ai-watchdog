from presidio_analyzer import PatternRecognizer, Pattern

recognizers = [
    PatternRecognizer(
        supported_entity="IN_AADHAAR",
        name="AadhaarRecognizer",
        patterns=[
            Pattern(name="aadhaar_number", regex=r"\b\d{4}\s?\d{4}\s?\d{4}\b", score=0.85),
        ],
        context=["aadhaar", "uidai", "identity", "id"],
    ),
]
