from pydantic import BaseModel, Field
from typing import Optional

class BiasDetectionOutput(BaseModel):
    result: bool = Field(..., description='Returns true if no bias is detected (passes scanner), false if any form of bias is found')
    details: Optional[str] = Field(None, description='Single line explanation')

SCANNER_NAME = "bias_detection"
DEFAULT_MODE = "llm"
AVAILABLE_MODES = ["llm"]
OUTPUT_MODEL = BiasDetectionOutput

def get_instruction_text() -> str:
    """
    Build instruction text for the BiasDetection scanner.
    
    Returns:
        str: Instruction text for detecting bias.
    """
    return """
You are a fairness and bias detection model.
Analyze the following text and determine if it contains **any form of bias** —
including gender, racial, political, cultural, or other prejudiced framing.
"""
