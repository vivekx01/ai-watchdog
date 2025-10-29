from pydantic import BaseModel, Field
from typing import Optional

class CodeDetectionOutput(BaseModel):
    result: bool = Field(..., description='Returns true if the text is pure code (passes scanner), false if it contains natural language or explanations')
    details: Optional[str] = Field(None, description='Single line explanation')

SCANNER_NAME = "code_detection"
DEFAULT_MODE = "llm"
AVAILABLE_MODES = ["llm"]
OUTPUT_MODEL = CodeDetectionOutput

def get_instruction_text() -> str:
    """
    Build instruction text for the CodeDetection scanner.
    
    Returns:
        str: Instruction text for detecting pure code content.
    """
    return """
You are a code classifier.
Determine whether the following text is *pure code* — meaning it mostly contains programming syntax,
not natural language, explanations, or instructions.
"""
