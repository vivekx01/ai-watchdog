from pydantic import BaseModel, Field
from typing import Optional
import unicodedata

class InvisibleTextOutput(BaseModel):
    result: bool = Field(..., description='Returns true if no invisible or obfuscated text is detected (passes scanner), false otherwise')
    details: Optional[str] = Field(None, description='Single line explanation')

SCANNER_NAME = "detect_invisible_text"
DEFAULT_MODE = "logic"
AVAILABLE_MODES = ["logic"]
SCANNER_TYPE = ["input"]
OUTPUT_MODEL = InvisibleTextOutput


def run_logic_based_scan(text: str) -> InvisibleTextOutput:
    """
    Detects invisible or non-printable Unicode characters in the given text.

    Args:
        text (str): The text to scan.

    Returns:
        InvisibleTextOutput: Result indicating presence of invisible characters.
    """
    banned_categories = {"Cf", "Co", "Cn"}

    def contains_unicode(t: str) -> bool:
        return any(ord(char) > 127 for char in t)

    # If text has no unicode chars, it's safe
    if not contains_unicode(text):
        return InvisibleTextOutput(
            result=True,
            details="No invisible characters detected."
        )

    invisible_chars = []
    for char in text:
        if unicodedata.category(char) in banned_categories:
            invisible_chars.append(char)
            text = text.replace(char, "")

    if invisible_chars:
        return InvisibleTextOutput(
            result=False,
            details=f"Invisible characters found and removed: {len(invisible_chars)}"
        )

    return InvisibleTextOutput(
        result=True,
        details="No invisible characters detected."
    )

