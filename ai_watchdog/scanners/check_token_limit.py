from pydantic import BaseModel, Field
from typing import Optional
import tiktoken

class TokenLimitOutput(BaseModel):
    result: bool = Field(..., description='Returns true if token count is within the allowed limit (passes scanner), false if limit exceeded')
    details: Optional[str] = Field(None, description='Single line explanation')

SCANNER_NAME = "check_token_limit"
DEFAULT_MODE = "logic"
AVAILABLE_MODES = ["logic"]
OUTPUT_MODEL = TokenLimitOutput


def run_logic_based_scan(
    text: str,
    max_tokens: int = 4096,
    encoding: Optional[tiktoken.Encoding] = "cl100k_base",
    model_name: Optional[str] = None
) -> TokenLimitOutput:
    """
    Generic logic-based scanner that checks if the given text exceeds the token limit.
    Uses tiktoken for accurate tokenization. Encoding can be passed directly for efficiency.
    
    Args:
        text (str): The text to analyze.
        max_tokens (int): The maximum allowed token count (default: 4096).
        encoding (tiktoken.Encoding, optional): Pre-initialized encoding instance. If not provided, one will be created.
        model_name (str, optional): Model name for selecting tokenizer. Only used if encoding is not provided.
    
    Returns:
        TokenLimitOutput: Structured output with result and explanation.
    """
    # Determine encoding (priority: provided > model_name > default)
 
    if model_name:
        encoding = tiktoken.encoding_for_model(model_name)
    else:
        encoding = tiktoken.get_encoding("cl100k_base")

    # Tokenize and count
    token_count = len(encoding.encode(text))

    if token_count <= max_tokens:
        return TokenLimitOutput(
            result=True,
            details=f"Token count ({token_count}) is within the allowed limit ({max_tokens})."
        )
    else:
        return TokenLimitOutput(
            result=False,
            details=f"Token count ({token_count}) exceeds the allowed limit ({max_tokens})."
        )

print(run_logic_based_scan("Enter your input here ...", max_tokens=4) )