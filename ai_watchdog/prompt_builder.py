import importlib
from typing import List, Dict
from .exceptions import ScannerImportError, PromptBuildError


def build_super_prompt(text_to_check: str, scanner_configs: List[Dict], scanner_package="ai_watchdog.scanners") -> str:
    """
    Build a single prompt for the LLM using scanner configs.
    
    Each scanner config is a dict, e.g.:
        {
            "name": "ban_code",           # required
            "params": {"some_param": ...} # optional
        }
    """
    scanners = []
    for config in scanner_configs:
        name = config.get("name")
        if not name:
            raise ScannerImportError("<unknown>", ValueError("Missing 'name' in scanner config"))
        
        try:
            module = importlib.import_module(f"{scanner_package}.{name}")
        except Exception as e:
            # If the scanner module itself cannot be imported
            raise ScannerImportError(name, e)
        
        scanners.append({
            "module": module,
            "params": config.get("params", {}) 
        })

    intro = (
        "You are an AI Policy Checker. You will receive multiple sets of scanning instructions below.\n"
        "For each instruction, analyze the provided text and respond according to the defined schema.\n"
    )

    scanner_instructions = (
        "For instructions which require a result boolean value, respond with False only if the text "
        "violates the instruction, otherwise respond with True.\n"
    )

    for scanner in scanners:
        try:
            instr_fn = getattr(scanner["module"], "get_instruction_text", None)
            if not callable(instr_fn):
                raise AttributeError(
                    f"Scanner '{scanner['module'].__name__}' must define a callable 'get_instruction_text()'"
                )

            instr = instr_fn(**scanner["params"]).strip()
            scanner_instructions += (
                f"\n### Instruction for scanner '{scanner['module'].SCANNER_NAME}' ###\n{instr}\n"
            )

        except Exception as e:
            # Covers missing SCANNER_NAME, or get_instruction_text failure
            raise PromptBuildError(scanner["module"].__name__, e)

    text_section = f"\nText to analyze: \n\"\"\"\n{text_to_check}\n\"\"\"\n"

    return intro + scanner_instructions + text_section
