from pydantic import BaseModel, Field
from typing import Optional

class ToxicityDetectionOutput(BaseModel):
    result: bool = Field(..., description='Returns true if the text is non-toxic (passes scanner), false if it contains toxic, offensive, or harmful content')
    details: Optional[str] = Field(None, description='Single line explanation')

SCANNER_NAME = "toxicity_detection"
DEFAULT_MODE = "llm"
AVAILABLE_MODES = ["llm"]
OUTPUT_MODEL = ToxicityDetectionOutput

def get_instruction_text() -> str:
    """
    Build instruction text for the ToxicityDetection scanner.
    
    Returns:
        str: Instruction text for detecting toxic, offensive, or harmful content.
    """
    return """
You are a precise text classifier.

Determine if the following text contains toxic, offensive, or harmful content.
Examples include hate speech, insults, harassment, or abusive language.
"""
