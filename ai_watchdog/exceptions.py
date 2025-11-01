import datetime
import traceback

class WatchdogError(Exception):
    """
    Base exception for all aiwatchdog-related errors.
    Includes automatic timestamping and readable context for debugging.
    """

    def __init__(self, message: str = "", *, context: dict | None = None):
        self.message = message or self.__class__.__name__
        self.context = context or {}
        self.timestamp = datetime.datetime.utcnow()
        super().__init__(self.message)

    def __str__(self):
        context_str = f" | Context: {self.context}" if self.context else ""
        return f"[{self.timestamp.isoformat()}] {self.message}{context_str}"

    def detailed(self) -> str:
        """Return full error details with stack trace."""
        tb = traceback.format_exc()
        context_str = f"\nContext: {self.context}" if self.context else ""
        return f"Error: {self.message}\nTime: {self.timestamp}\n{context_str}\nTraceback:\n{tb}"

class LLMCreationError(WatchdogError):
    """Raised when the LLM could not be created due to invalid provider, model, or API key."""

    def __init__(self, provider: str, model: str | None, message: str = ""):
        super().__init__(
            message or f"Failed to create LLM for provider '{provider}' with model '{model}'",
            context={"provider": provider, "model": model},
        )


class ScannerImportError(WatchdogError):
    """Raised when a scanner module cannot be imported or is missing required attributes."""

    def __init__(self, scanner_name: str, error: Exception):
        super().__init__(
            f"Failed to load scanner module '{scanner_name}': {error}",
            context={"scanner": scanner_name, "error": str(error)},
        )


class PromptBuildError(WatchdogError):
    """Raised when building the LLM prompt fails due to misconfiguration or missing data."""

    def __init__(self, scanner_name: str, error: Exception):
        super().__init__(
            f"Error building prompt for scanner '{scanner_name}': {error}",
            context={"scanner": scanner_name, "error": str(error)},
        )


class ScanExecutionError(WatchdogError):
    """Raised when the scan fails to execute or the LLM returns an invalid response."""

    def __init__(self, text_sample: str, error: Exception):
        preview = text_sample[:100] + ("..." if len(text_sample) > 100 else "")
        super().__init__(
            f"Scan execution failed: {error}",
            context={"text_preview": preview, "error": str(error)},
        )

class LogicScanError(WatchdogError):
    """Raised when a logic-based scanner encounters an error."""
    def __init__(self, scanner_name, original_exception):
        super().__init__(
            f"Logic scan failed for scanner '{scanner_name}': {original_exception}",
            context={"scanner": scanner_name, "error": str(original_exception)}
        )
