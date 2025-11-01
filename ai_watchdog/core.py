from .llm_factory import create_llm
from .pydantic_model_builder import build_dynamic_super_model
from pydantic import create_model
from .prompt_builder import build_super_prompt
import importlib
from .exceptions import (
        ScanExecutionError,
        ScannerImportError,
        LogicScanError,
    )

def validate_scanner_config(scanner_config, allowed_type: str):
    """
    Validate and filter scanners based on allowed type ('input' or 'output').

    Args:
        scanner_config (list): List of scanner configurations.
        allowed_type (str): 'input' or 'output'

    Returns:
        list: Filtered and valid scanner configurations.
    """
    valid_configs = []
    skipped = []

    for config in scanner_config:
        name = config.get("name")
        if not name:
            continue

        try:
            module = importlib.import_module(f"ai_watchdog.scanners.{name}")
            scanner_types = getattr(module, "SCANNER_TYPE", ["input", "output"])

            if allowed_type.lower() in [t.lower() for t in scanner_types]:
                valid_configs.append(config)
            else:
                skipped.append(name)
        except Exception as e:
            raise ScannerImportError(name, e)

    if skipped:
        print(f"[Watchdog] Skipped scanners (not valid for {allowed_type}): {', '.join(skipped)}")

    return valid_configs

def run(llm, text, scanner_config):
    llm_scanners = []
    logic_scanners = []
    separate_llm_scanners = []  # <-- New list for special cases

    # --- Step 1: Categorize scanners ---
    for config in scanner_config:
        name = config.get("name")
        if not name:
            continue

        try:
            module = importlib.import_module(f"ai_watchdog.scanners.{name}")
            mode = getattr(module, "DEFAULT_MODE", "llm").lower()
            if mode == "logic":
                logic_scanners.append(config)
            elif mode == "llm" and name in ["relevance_detection"]:
                separate_llm_scanners.append(config)
            else:
                llm_scanners.append(config)
        except Exception as e:
            raise ScannerImportError(name, e)

    logic_results = {}

    # --- Step 2: Run logic-based scanners ---
    for config in logic_scanners:
        name = config["name"]
        try:
            module = importlib.import_module(f"ai_watchdog.scanners.{name}")
            logic_fn = getattr(module, "run_logic_based_scan", None)
            if not callable(logic_fn):
                raise AttributeError(f"Scanner '{name}' missing run_logic_based_scan function")

            params = config.get("params", {})
            logic_result_model = logic_fn(text, **params)

            if not hasattr(logic_result_model, "model_dump"):
                raise TypeError(f"Logic scanner '{name}' must return a Pydantic model")

            logic_results[name] = logic_result_model
        except Exception as e:
            raise LogicScanError(name, e)

    # --- Step 3: Run LLM-based scanners (combined ones) ---
    llm_result_model = None
    if llm_scanners:
        name_list = [item["name"] for item in llm_scanners]
        final_model = build_dynamic_super_model(name_list)
        final_prompt = build_super_prompt(text, llm_scanners)

        structured_model = llm.with_structured_output(final_model)
        try:
            llm_result_model = structured_model.invoke(final_prompt)
        except Exception as e:
            raise ScanExecutionError(text, e)

    # --- Step 4: Run separate LLM scanners (like relevance_detection) ---
    separate_results = {}
    for config in separate_llm_scanners:
        name = config["name"]
        try:
            separate_results[name] = llm_run_separately(llm, text, config)
        except Exception as e:
            raise ScanExecutionError(name, e)

    # --- Step 5: Merge all results ---
    all_fields = {}
    for name, model in logic_results.items():
        all_fields[name] = (dict, model.model_dump())

    if llm_result_model:
        for field_name, field_value in llm_result_model.model_dump().items():
            all_fields[field_name] = (type(field_value), field_value)

    for name, model in separate_results.items():
        all_fields[name] = (dict, model.model_dump())

    failed_scanners = [
        name for name, (_, data) in all_fields.items()
        if isinstance(data, dict) and data.get("result") is False
    ]
    overall_result = len(failed_scanners) == 0

    all_fields["overall_result"] = (bool, overall_result)
    all_fields["failed_scanners"] = (list[str], failed_scanners)

    if not all_fields:
        return {}

    UnifiedResult = create_model("UnifiedScanResult", **all_fields)
    return UnifiedResult(**{k: v[1] for k, v in all_fields.items()}).model_dump()

def llm_run_separately(llm, text, scanner_config):
    """
    Run scanners like 'relevance_detection' separately using their own
    instruction builder and output model instead of the combined super model.

    Args:
        llm: The LLM instance.
        text (str): The text to analyze.
        scanner_config (dict): Scanner config containing 'name' and optional 'params'.

    Returns:
        A Pydantic model instance (result of the LLM call).
    """
    name = scanner_config["name"]
    params = scanner_config.get("params", {})

    # Dynamically import the scanner module
    module = importlib.import_module(f"ai_watchdog.scanners.{name}")

    # Get the OutputModel
    model = getattr(module, "OUTPUT_MODEL", None)
    if model is None:
        raise AttributeError(f"Scanner '{name}' missing OUTPUT_MODEL class")

    # Get the instruction text builder
    get_instr = getattr(module, "get_instruction_text", None)
    if not callable(get_instr):
        raise AttributeError(f"Scanner '{name}' missing get_instruction_text() function")

    # Build instruction using text + params (if the function accepts them)
    try:
        # Attempt to call with both text and params — if it doesn’t accept them, fallback gracefully
        instruction = get_instr(text, **params)
    except TypeError:
        # For backward compatibility (if function doesn’t take arguments)
        instruction = get_instr()

    # Construct final prompt
    final_prompt = f"{instruction.strip()}\n\n{text}"

    # Run the structured LLM scan
    structured_model = llm.with_structured_output(model)
    result_model = structured_model.invoke(final_prompt)

    if not hasattr(result_model, "model_dump"):
        raise TypeError(f"Scanner '{name}' must return a Pydantic model")

    return result_model

class InputWatchdog:
    def __init__(self, provider=None, model=None, api_key=None):
        self.llm = create_llm(provider, model, api_key)

    def scan(self, text, scanner_config):
        valid_configs = validate_scanner_config(scanner_config, "input")
        return run(self.llm, text, valid_configs)
        

class OutputWatchdog:
    def __init__(self, provider=None, model=None, api_key=None):
        self.llm = create_llm(provider, model, api_key)

    def scan(self, text, scanner_config):
        valid_configs = validate_scanner_config(scanner_config, "output")
        return run(self.llm, text, valid_configs)
