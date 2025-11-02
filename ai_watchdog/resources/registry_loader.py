import pkgutil
import importlib
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry, PatternRecognizer


def load_all_recognizers_from_resources(analyzer: AnalyzerEngine) -> AnalyzerEngine:
    """
    Loads:
    1. Custom recognizers from ai_watchdog.resources.pii_recognizers
    2. All predefined recognizers (including country_specific) from Presidio
    """
    # --- Load custom recognizers from your own package ---
    package = "ai_watchdog.resources.pii_recognizers"
    try:
        package_loader = pkgutil.iter_modules(importlib.import_module(package).__path__)
        for module_info in package_loader:
            module = importlib.import_module(f"{package}.{module_info.name}")
            if hasattr(module, "recognizers"):
                for recognizer in getattr(module, "recognizers"):
                    analyzer.registry.add_recognizer(recognizer)
    except ModuleNotFoundError:
        print(f"Custom recognizer package '{package}' not found. Skipping...")

    # --- Load all predefined recognizers from Presidio (recursively) ---
    try:
        base_pkg = "presidio_analyzer.predefined_recognizers"

        def import_all_recognizers(package_name):
            pkg = importlib.import_module(package_name)
            for _, mod_name, is_pkg in pkgutil.iter_modules(pkg.__path__):
                full_name = f"{package_name}.{mod_name}"
                if is_pkg:
                    import_all_recognizers(full_name)
                else:
                    module = importlib.import_module(full_name)
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (
                            isinstance(attr, type)
                            and issubclass(attr, PatternRecognizer)
                            and attr.__name__ != "PatternRecognizer"
                        ):
                            analyzer.registry.add_recognizer(attr())

        import_all_recognizers(base_pkg)

    except Exception as e:
        print(f"Error loading predefined recognizers: {e}")

    return analyzer
