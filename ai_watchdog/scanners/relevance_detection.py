from pydantic import BaseModel, Field
from typing import Optional

class RelevanceDetectionOutput(BaseModel):
    result: bool = Field(..., description='Returns true if the generated text is relevant and aligned with the original prompt (passes scanner), false if it is off-topic or misaligned')
    details: Optional[str] = Field(None, description='Single line explanation')

SCANNER_NAME = "relevance_detection"
SCANNER_TYPE = ["output"]
DEFAULT_MODE = "llm"
AVAILABLE_MODES = ["llm"]
OUTPUT_MODEL = RelevanceDetectionOutput

def get_instruction_text(generated_text: str, prompt_text: str) -> str:
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

Determine whether the generated text is relevant to the original prompt —
that is, whether it stays on topic, refers to the same subject, and is not off-topic.

Do not penalize for brevity or partial answers. 
Only flag as irrelevant if the generated text discusses a different topic or meaning.

Original prompt:
```
{prompt_text}
```

Generated text:
```
{generated_text}
```
"""