import pkgutil
import importlib
from presidio_analyzer import AnalyzerEngine


def load_all_recognizers_from_resources(analyzer) -> AnalyzerEngine:
    """
    Loads all custom recognizers from resources/pii_recognizers/
    and merges them with Presidio's built-in ones.
    """
    package = "ai_watchdog.resources.pii_recognizers"
    package_loader = pkgutil.iter_modules(importlib.import_module(package).__path__)

    for module_info in package_loader:
        module = importlib.import_module(f"{package}.{module_info.name}")
        if hasattr(module, "recognizers"):
            for recognizer in getattr(module, "recognizers"):
                analyzer.registry.add_recognizer(recognizer)

    return analyzer
