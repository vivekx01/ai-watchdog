from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from pydantic import BaseModel
from ai_watchdog.resources.registry_loader import load_all_recognizers_from_resources


class PIIDetectionResult(BaseModel):
    result: bool                # True if PII found
    details: str                # Message about what happened
    pii_found: list[str]        # List of detected PII entities
    sanitized_text: str | None  # Redacted version of the text (if redact mode)


SCANNER_NAME = "secrets_detection"
SCANNER_TYPE = ["input"]
DEFAULT_MODE = "logic"
AVAILABLE_MODES = ["logic"]
OUTPUT_MODEL = PIIDetectionResult


def run_logic_based_scan(text: str, mode: str = "block") -> PIIDetectionResult:
    """
    Run Presidio PII detection with a choice to either block or redact.

    Args:
        text (str): Input text to scan.
        mode (str): Either 'block' or 'redact'. Defaults to 'block'.

    Returns:
        PIIDetectionResult: Object containing detection result, details, and optional sanitized text.
    """

    analyzer = AnalyzerEngine()
    analyzer = load_all_recognizers_from_resources(analyzer)

    # Analyze
    results = analyzer.analyze(text=text, entities=[], language="en")

    if not results:
        return PIIDetectionResult(
            result=True,
            details="No PII found.",
            pii_found=[],
            sanitized_text=text,
        )

    # Gather detected entities
    pii_entities = [res.entity_type for res in results]

    if mode == "redact":
        anonymizer = AnonymizerEngine()
        anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
        return PIIDetectionResult(
            result=True,
            details="PII detected and redacted successfully.",
            pii_found=pii_entities,
            sanitized_text=anonymized.text,
        )
    else:  # block
        return PIIDetectionResult(
            result=False,
            details="PII detected. Text blocked due to policy.",
            pii_found=pii_entities,
            sanitized_text=None,
        )


