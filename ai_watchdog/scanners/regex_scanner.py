from pydantic import BaseModel, Field
from typing import Optional
import re

class RegexScannerOutput(BaseModel):
    result: bool = Field(..., description='True if regex pattern matched')
    details: Optional[str] = Field(None, description='Explanation of result')
    sanitized_text: Optional[str] = Field(None, description='Text with redacted patterns if applicable')

SCANNER_NAME = "regex_scanner"
SCANNER_TYPE = ["input", "output"]
DEFAULT_MODE = "logic"
AVAILABLE_MODES = ["logic"]
OUTPUT_MODEL = RegexScannerOutput

def run_logic_based_scan(
    text: str,
    patterns: list[str],
    is_blocked: bool = True,
    redact: bool = False
):
    sanitized_text = text
    for pattern in patterns:
        if re.search(pattern, text):
            if redact:
                sanitized_text = re.sub(pattern, "[REDACTED]", sanitized_text)
            return RegexScannerOutput(
                result=True,
                details=f"Pattern matched: {pattern}",
                sanitized_text=sanitized_text if redact else None
            )
    # no match
    return RegexScannerOutput(
        result=False,
        details="No patterns matched",
        sanitized_text=sanitized_text if redact else None
    )

print(run_logic_based_scan(
    "This is a test text with a badword.",
    ["badword", "anotherbadword"],
    is_blocked=True
))
