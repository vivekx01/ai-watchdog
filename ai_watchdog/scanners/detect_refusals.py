from pydantic import BaseModel, Field
from typing import Optional

class DetectRefusalsOutput(BaseModel):
    result: bool = Field(..., description='Returns true if no refusal or evasion is detected (passes scanner), false if the text contains a refusal or avoidance statement')
    details: Optional[str] = Field(None, description='Single line explanation')

SCANNER_NAME = "detect_refusals"
DEFAULT_MODE = "llm"
AVAILABLE_MODES = ["llm"]
OUTPUT_MODEL = DetectRefusalsOutput

def get_instruction_text() -> str:
    """
    Build instruction text for the DetectRefusals scanner.
    
    Returns:
        str: Instruction text for detecting refusals, evasions, or inability to answer.
    """
    return """
You are a precise text classifier.

Determine if the following text contains any form of refusal,
evasion, or inability to answer. This includes phrases like
"Sorry, I cannot help with that", "I am unable to provide",
or any statement where the assistant refuses, declines, or avoids answering.
"""
