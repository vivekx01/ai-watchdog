from pydantic import BaseModel, Field
from typing import Optional

class BanCodeOutput(BaseModel):
    result: bool = Field(..., description='False if code is detected, True if no code is present')
    details: Optional[str] = Field(None, description='Single line explanation')

SCANNER_NAME = "ban_code"
SCANNER_TYPE = ["input"]
DEFAULT_MODE = "llm"
AVAILABLE_MODES = ["llm"]
OUTPUT_MODEL = BanCodeOutput

def get_instruction_text() -> str:
    """
    Build instruction text for the BanCode scanner.
    """
    return """
You are a precise text classifier. Determine whether the following text contains *any* computer code (in any language: Python, JavaScript, SQL, HTML, etc.).
Code includes function definitions, imports, variable assignments, or code snippets in markdown code blocks.
Single words such as "function" or "import" alone are NOT considered code.
"""
