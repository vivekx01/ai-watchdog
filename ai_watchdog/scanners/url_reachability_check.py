from pydantic import BaseModel, Field
from typing import Optional, List
import re
import requests

class UrlReachabilityOutput(BaseModel):
    result: bool = Field(..., description='Returns true if all detected URLs are reachable, false if any are broken or unreachable')
    details: Optional[str] = Field(None, description='Single line explanation')
    unreachable_urls: Optional[List[str]] = Field(None, description='List of URLs that could not be reached')

SCANNER_NAME = "url_reachability_check"
DEFAULT_MODE = "logic"
AVAILABLE_MODES = ["logic"]
OUTPUT_MODEL = UrlReachabilityOutput


def run_logic_based_scan(
    text: str,
    timeout: int = 5,
    max_urls: int = 10
) -> UrlReachabilityOutput:
    """
    Logic-based scanner that checks whether URLs in the text are reachable.
    Sends HEAD requests to avoid downloading full pages.

    Args:
        text (str): Text to analyze for URLs.
        timeout (int): Timeout for each URL request in seconds (default: 5).
        max_urls (int): Max number of URLs to check to avoid excessive requests (default: 10).

    Returns:
        UrlReachabilityOutput: Structured output with result, details, and list of unreachable URLs.
    """
    # Extract URLs from text
    url_pattern = re.compile(r'https?://[^\s]+')
    urls = url_pattern.findall(text)
    urls_to_check = urls[:max_urls]

    if not urls_to_check:
        return UrlReachabilityOutput(
            result=True,
            details="No URLs found in the text to verify.",
            unreachable_urls=[]
        )

    unreachable = []
    for url in urls_to_check:
        try:
            response = requests.head(url, allow_redirects=True, timeout=timeout)
            if response.status_code >= 400:
                unreachable.append(url)
        except Exception:
            unreachable.append(url)

    if unreachable:
        return UrlReachabilityOutput(
            result=False,
            details=f"{len(unreachable)} of {len(urls_to_check)} URLs are unreachable.",
            unreachable_urls=unreachable
        )
    else:
        return UrlReachabilityOutput(
            result=True,
            details=f"All {len(urls_to_check)} URLs are reachable.",
            unreachable_urls=[]
        )
