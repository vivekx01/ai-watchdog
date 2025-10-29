from pydantic import BaseModel, Field
from typing import Optional

class FactualConsistencyCheckOutput(BaseModel):
    result: bool = Field(..., description='Returns true if the text is factually consistent (passes scanner), false if any factual inconsistency or contradiction is detected')
    details: Optional[str] = Field(None, description='Single line explanation')

SCANNER_NAME = "factual_consistency_check"
DEFAULT_MODE = "llm"
AVAILABLE_MODES = ["llm"]
OUTPUT_MODEL = FactualConsistencyCheckOutput

def get_instruction_text() -> str:
    """
    Build instruction text for the FactualConsistencyCheck scanner.
    
    Returns:
        str: Instruction text for factual consistency analysis.
    """
    return """
You are a precise text classifier.

Determine if the following text contains any factual inconsistencies,
logical contradictions, or statements that are clearly false
based on common knowledge and logical reasoning.
"""
