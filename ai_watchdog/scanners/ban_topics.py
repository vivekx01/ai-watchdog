from pydantic import BaseModel, Field
from typing import Optional, List

class BanTopicsOutput(BaseModel):
    result: bool = Field(..., description='Returns true if no banned topic is mentioned (passes scanner), false if any banned topic is detected')
    details: Optional[str] = Field(None, description='Single line explanation')

SCANNER_NAME = "ban_topics"
DEFAULT_MODE = "llm"
AVAILABLE_MODES = ["llm"]
OUTPUT_MODEL = BanTopicsOutput

def get_instruction_text(topic_list: List[str]) -> str:
    """
    Build instruction text for the BanTopics scanner dynamically.
    
    Args:
        topic_list (List[str]): List of banned topics to check for.
    
    Returns:
        str: Instruction text with the topic list injected.
    """
    topic_str = ", ".join(topic_list)
    return f"""
You are a content moderation model.
Determine if the following text mentions or relates to any of these banned topics:
{topic_str}
"""
