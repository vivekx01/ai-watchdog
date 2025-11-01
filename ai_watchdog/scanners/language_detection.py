from pydantic import BaseModel, Field
from typing import Optional

class LanguageDetectionOutput(BaseModel):
    detected_language: str = Field(..., description='The primary language identified in the text')
    is_authentic: bool = Field(..., description='Returns true if the text appears naturally written by a fluent speaker, false if it seems machine-translated or unnatural')
    details: Optional[str] = Field(None, description='Single line explanation or reasoning')

SCANNER_NAME = "language_detection"
DEFAULT_MODE = "llm"
SCANNER_TYPE = ["input", "output"]
AVAILABLE_MODES = ["llm"]
OUTPUT_MODEL = LanguageDetectionOutput

def get_instruction_text() -> str:
    """
    Build instruction text for the LanguageDetection scanner.
    
    Returns:
        str: Instruction text for detecting language and authenticity.
    """
    return """
You are a linguistic authenticity evaluator.
Identify the **primary language** of the following text, and assess if it is authentic
(i.e., naturally written by a fluent speaker, not machine-translated or gibberish).
"""
