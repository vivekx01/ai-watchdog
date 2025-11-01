from pydantic import BaseModel, Field
from typing import List


# --- Scanner metadata ---
SCANNER_NAME = "ban_substrings"
DEFAULT_MODE = "logic"  # can be switched to "llm" if you want LLM-based scanning
AVAILABLE_MODES = ["logic", "llm"]
SCANNER_TYPE = ["input", "output"]

class BanSubstringsOutput(BaseModel):
    result: bool = Field(..., description="True if text passes the check, False if it violates the rule.")
    banned_phrases_found: List[str] = Field(default_factory=list, description="List of banned substrings found in text.")


def run_logic_based_scan(text: str, banned_substrings: List[str]) -> BanSubstringsOutput:
    """
    Detects whether the input text contains any banned substrings.
    Returns a BanSubstringsOutput Pydantic model.
    """
    found = [s for s in banned_substrings if s.lower() in text.lower()]
    passed = len(found) == 0
    return BanSubstringsOutput(result=passed, banned_phrases_found=found)

def get_instruction_text(banned_substrings: List[str]) -> str:
    """
    Builds the LLM instruction text for substring banning.
    This is used only when DEFAULT_MODE = 'llm'.
    """
    substr_list = ", ".join(f"'{s}'" for s in banned_substrings)
    return (
        f"You must check if the provided text contains any of the following banned substrings: {substr_list}.\n"
        "If the text contains any of them, respond with result=False. "
        "Otherwise, respond with result=True. "
        "Also return a list of all banned substrings that were found."
    )


# --- Attach to package model registry ---
OUTPUT_MODEL = BanSubstringsOutput
