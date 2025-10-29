from pydantic import BaseModel, Field
from typing import Optional

class RelevanceDetectionOutput(BaseModel):
    result: bool = Field(..., description='Returns true if the generated text is relevant and aligned with the original prompt (passes scanner), false if it is off-topic or misaligned')
    details: Optional[str] = Field(None, description='Single line explanation')

SCANNER_NAME = "relevance_detection"
DEFAULT_MODE = "llm"
AVAILABLE_MODES = ["llm"]
OUTPUT_MODEL = RelevanceDetectionOutput

def get_instruction_text(prompt_text: str, generated_text: str) -> str:
    """
    Build instruction text for the RelevanceDetection scanner dynamically.
    
    Args:
        prompt_text (str): The original user prompt.
        generated_text (str): The generated text to evaluate.
    
    Returns:
        str: Instruction text embedding both prompt and generated text.
    """
    return f"""
You are a precise text classifier.

Determine if the following generated text is irrelevant, off-topic,
or misaligned with the original prompt.

Original prompt:
```
{prompt_text}
```

Generated text:
```
{generated_text}
```
"""