from pydantic import BaseModel, Field
from typing import Optional

class GibberishDetectionOutput(BaseModel):
    result: bool = Field(..., description='Returns true if the text is meaningful English (passes scanner), false if it is gibberish or nonsensical')
    details: Optional[str] = Field(None, description='Single line explanation')

SCANNER_NAME = "gibberish_detection"
DEFAULT_MODE = "llm"
AVAILABLE_MODES = ["llm"]
OUTPUT_MODEL = GibberishDetectionOutput

def get_instruction_text() -> str:
    """
    Build instruction text for the GibberishDetection scanner.
    
    Returns:
        str: Instruction text for detecting gibberish or nonsensical text.
    """
    return """
You are a linguistic sanity checker.
Determine if the following text is **meaningful English** or **gibberish/non-sense**.
"""
