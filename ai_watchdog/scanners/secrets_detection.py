from detect_secrets.core.secrets_collection import SecretsCollection
from detect_secrets.settings import transient_settings
import tempfile
import os
from pydantic import BaseModel


class DetectSecretsResult(BaseModel):
    result: bool
    details: str
    secrets_found: list[str]


SCANNER_NAME = "secrets_detection"
SCANNER_TYPE = ["input"]
DEFAULT_MODE = "logic"
AVAILABLE_MODES = ["logic"]
OUTPUT_MODEL = DetectSecretsResult


def run_logic_based_scan(text: str) -> DetectSecretsResult:
    """
    Scans the given text for potential secrets using detect-secrets.

    Args:
        text (str): The text content to scan.

    Returns:
        DetectSecretsResult: Pydantic model with scan result and details.
    """
    if not text.strip():
        return DetectSecretsResult(
            result=True,
            details="No secrets detected in the provided text.",
            secrets_found=[],
        )

    # Default plugin config can be customized here if needed
    default_detect_secrets_config = {
        "plugins_used": [
            {"name": "AWSKeyDetector"},
            {"name": "SlackDetector"},
            {"name": "PrivateKeyDetector"},
            {"name": "BasicAuthDetector"},
            {"name": "JwtTokenDetector"},
            {"name": "StripeDetector"},
            {"name": "NpmDetector"},
            {"name": "ArtifactoryDetector"},
            {"name": "GitHubTokenDetector"},
            {"name": "GitLabTokenDetector"},
            {"name": "Base64HighEntropyString", "limit": 4.5},
            {"name": "HexHighEntropyString", "limit": 3.0},
            {"name": "DiscordBotTokenDetector"},
            {"name": "CloudantDetector"},
            {"name": "IbmCloudIamDetector"},
            {"name": "IbmCosHmacDetector"},
            {"name": "MailchimpDetector"},
            {"name": "SquareOAuthDetector"},
            {"name": "SoftlayerDetector"},
            {"name": "TelegramBotTokenDetector"},
            {"name": "TwilioKeyDetector"},
        ]
    }

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        temp_file.write(text.encode("utf-8"))
        temp_file.close()

        secrets = SecretsCollection()
        with transient_settings(default_detect_secrets_config):
            secrets.scan_file(temp_file.name)

        all_secrets = []
        for file in secrets.files:
            for secret in secrets[file]:
                if secret.secret_value:
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

    finally:
        os.remove(temp_file.name)
