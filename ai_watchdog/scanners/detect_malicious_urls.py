from pydantic import BaseModel, Field
from typing import Optional

class DetectMaliciousUrlsOutput(BaseModel):
    result: bool = Field(..., description='Returns true if no malicious URLs are detected (passes scanner), false if any URL is potentially harmful or malicious')
    details: Optional[str] = Field(None, description='Single line explanation or examples of detected malicious URLs')

SCANNER_NAME = "detect_malicious_urls"
DEFAULT_MODE = "llm"
AVAILABLE_MODES = ["llm"]
SCANNER_TYPE = ["output"]
OUTPUT_MODEL = DetectMaliciousUrlsOutput

def get_instruction_text() -> str:
    """
    Build instruction text for the DetectMaliciousUrls scanner.
    
    Returns:
        str: Instruction text for detecting malicious or harmful URLs.
    """
    return """
You are a precise content safety classifier.

Determine if the following text contains any malicious, phishing, or potentially harmful URLs.
Examples include links that attempt to:
- Steal personal information (phishing)
- Distribute malware or viruses
- Redirect to unsafe or scam websites

Provide reasoning in the details if any URL is flagged.
"""
