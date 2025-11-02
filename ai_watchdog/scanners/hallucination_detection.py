from pydantic import BaseModel, Field
from typing import Optional

class HallucinationDetectionOutput(BaseModel):
    result: bool = Field(..., description='Returns true if no hallucinations are detected (passes scanner), false if any fabricated, unsupported, or unverifiable claims are found')
    details: Optional[str] = Field(None, description='Single line explanation')

SCANNER_NAME = "hallucination_detection"
DEFAULT_MODE = "llm"
AVAILABLE_MODES = ["llm"]
SCANNER_TYPE = ["output"]
OUTPUT_MODEL = HallucinationDetectionOutput

def get_instruction_text() -> str:
    """
    Build instruction text for the HallucinationDetection scanner.
    
    Returns:
        str: Instruction text for identifying hallucinated or fabricated content.
    """
    return """
You are a precise text classifier.

Determine if the following generated text contains any hallucinated,
fabricated, or unverifiable information — statements that are not supported
by facts, common knowledge, or plausible evidence.

Hallucinations may include:
- Invented facts, statistics, or historical events
- Fake references, URLs, or citations
- Nonexistent people, places, or organizations
- Overconfident claims without factual basis

Do NOT flag reasonable assumptions, opinions, or hypothetical examples
if they are clearly presented as such.
"""
