from pydantic import BaseModel, Field
from typing import Optional, List

class BanCompetitorsOutput(BaseModel):
    result: bool = Field(..., description='Returns true if no competitor is mentioned (passes scanner), false if any competitor is detected')
    details: Optional[str] = Field(None, description='Single line explanation')

SCANNER_NAME = "ban_competitors"
SCANNER_TYPE = ["input", "output"]
DEFAULT_MODE = "llm"
AVAILABLE_MODES = ["llm"]
OUTPUT_MODEL = BanCompetitorsOutput

def get_instruction_text(competitor_list: List[str]) -> str:
    """
    Build instruction text for the BanCompetitors scanner dynamically.
    
    Args:
        competitor_list (List[str]): List of competitor names to check for.
    
    Returns:
        str: Instruction text with competitors injected.
    """
    formatted_list = ", ".join(competitor_list)
    return f"""
You are a content filter. Determine if the following text
mentions or refers directly or indirectly to any competitor
from the list: {formatted_list}
"""
