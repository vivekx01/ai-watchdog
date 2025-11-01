from pydantic import BaseModel, Field
from typing import Optional

class ReadingTimeOutput(BaseModel):
    result: bool = Field(..., description='Returns true if estimated reading time is within the allowed limit (passes scanner), false if limit exceeded')
    details: Optional[str] = Field(None, description='Single line explanation')

SCANNER_NAME = "reading_time"
DEFAULT_MODE = "logic"
SCANNER_TYPE = ["output"]
AVAILABLE_MODES = ["logic"]
OUTPUT_MODEL = ReadingTimeOutput


def run_logic_based_scan(
    text: str,
    max_minutes: float = 5.0,
    words_per_minute: int = 200
) -> ReadingTimeOutput:
    """
    Generic logic-based scanner that checks if the estimated reading time exceeds a given limit.
    
    Args:
        text (str): The text to analyze.
        max_minutes (float): Maximum allowed reading time in minutes (default: 5.0).
        words_per_minute (int): Average reading speed in words per minute (default: 200).
    
    Returns:
        ReadingTimeOutput: Structured output with result and explanation.
    """
    # Count words
    word_count = len(text.split())

    # Calculate estimated reading time in minutes
    estimated_time = word_count / words_per_minute

    if estimated_time <= max_minutes:
        return ReadingTimeOutput(
            result=True,
            details=f"Estimated reading time ({estimated_time:.2f} min) is within the allowed limit ({max_minutes} min)."
        )
    else:
        return ReadingTimeOutput(
            result=False,
            details=f"Estimated reading time ({estimated_time:.2f} min) exceeds the allowed limit ({max_minutes} min)."
        )

print(run_logic_based_scan("Enter your input here ...", max_minutes=1) )