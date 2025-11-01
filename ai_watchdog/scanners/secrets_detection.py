from detect_secrets import SecretsCollection, plugins
from pydantic import BaseModel


class DetectSecretsResult(BaseModel):
    result: bool
    details: str
    secrets_found: list[str]

SCANNER_NAME = "secrets_detection"
DEFAULT_MODE = "logic"
AVAILABLE_MODES = ["logic"]
OUTPUT_MODEL = DetectSecretsResult

def run_logic_based_scan(text: str) -> DetectSecretsResult:
    """
    Scans the given text for potential secrets using detect-secrets.

    Args:
        text (str): The text content to scan.
        **kwargs: Additional configuration options (currently unused).

    Returns:
        DetectSecretsResult: Pydantic model with scan result and details.
    """
    # Initialize all default plugins (AWS, Slack, Generic, etc.)
    plugins_used = plugins.initialize.from_plugin_classname(None)
    secrets = SecretsCollection(plugins=plugins_used)

    lines = text.splitlines()
    for i, line in enumerate(lines, start=1):
        secrets.scan_line(line=line, filename=f"<memory-line-{i}>")

    all_secrets = []
    for _, secret_list in secrets.data.items():
        for secret in secret_list:
            all_secrets.append(secret.secret_value)

    if all_secrets:
        return DetectSecretsResult(
            result=False,
            details="Potential secrets detected in the provided text.",
            secrets_found=all_secrets,
        )

    return DetectSecretsResult(
        result=True,
        details="No secrets detected in the provided text.",
        secrets_found=[],
    )
