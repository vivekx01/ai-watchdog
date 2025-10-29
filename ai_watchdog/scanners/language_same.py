from pydantic import BaseModel, Field
from typing import Optional

class LanguageSameOutput(BaseModel):
    result: bool = Field(..., description='Returns true if the text is written in the specified target language (passes scanner), false otherwise')
    details: Optional[str] = Field(None, description='Single line explanation')

SCANNER_NAME = "language_same"
DEFAULT_MODE = "llm"
AVAILABLE_MODES = ["llm"]
OUTPUT_MODEL = LanguageSameOutput

def get_instruction_text(target_language: str) -> str:
    """
    Build instruction text for the LanguageSame scanner dynamically.

    Args:
        target_language (str): The target language to validate against.

    Returns:
        str: Instruction text with the target language inserted.
    """
    return f"""
You are a language validator.
Determine if the following text is written in the specified target language: {target_language}.
"""
