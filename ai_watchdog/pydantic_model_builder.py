import importlib
from pydantic import create_model
from .exceptions import ScannerImportError

def build_dynamic_super_model(scanner_names: list, scanner_package="ai_watchdog.scanners"):
    """
    Build a dynamic Pydantic super model from a list of scanner names.

    Parameters:
        scanner_names: list of scanner module names as strings, e.g. ["ban_code", "toxicity_detection"]
        scanner_package: the Python package where the scanner modules are located (default: "scanners")
    """
    fields = {}

    for name in scanner_names:
        try:
            # dynamically import the scanner module
            module = importlib.import_module(f"{scanner_package}.{name}")

            # read SCANNER_NAME and OUTPUT_MODEL from the module
            scanner_field_name = getattr(module, "SCANNER_NAME")
            scanner_output_model = getattr(module, "OUTPUT_MODEL")
        except (ImportError, AttributeError) as e:
            raise ScannerImportError(name, e)
        # add to fields dict
        fields[scanner_field_name] = (scanner_output_model, ...)
    return create_model("ExpectedLLMOutput", **fields)
