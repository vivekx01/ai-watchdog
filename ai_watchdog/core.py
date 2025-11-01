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

def run(llm, text, scanner_config):
    llm_scanners = []
    logic_scanners = []

    # --- Step 1: Categorize scanners based on DEFAULT_MODE ---
    for config in scanner_config:
        name = config.get("name")
        if not name:
            continue

        try:
            module = importlib.import_module(f"ai_watchdog.scanners.{name}")
            mode = getattr(module, "DEFAULT_MODE", "llm").lower()
            if mode == "llm":
                llm_scanners.append(config)
            elif mode == "logic":
                logic_scanners.append(config)
        except Exception as e:
            raise ScannerImportError(name, e)

    logic_results = {}

    # --- Step 2: Run logic-based scanners locally ---
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

    # --- Step 3: Run LLM-based scanners ---
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

    # --- Step 4: Merge both result models into one unified Pydantic model ---
    all_fields = {}
    for name, model in logic_results.items():
        all_fields[name] = (dict, model.model_dump())

    if llm_result_model:
        for field_name, field_value in llm_result_model.model_dump().items():
            all_fields[field_name] = (type(field_value), field_value)

    if not all_fields:
        return {}

    UnifiedResult = create_model("UnifiedScanResult", **all_fields)
    return UnifiedResult(**{k: v[1] for k, v in all_fields.items()}).model_dump()

class InputWatchdog:
    def __init__(self, provider=None, model=None, api_key=None):
        self.llm = create_llm(provider, model, api_key)

    def scan(self, text, scanner_config):
        return run(self.llm, text, scanner_config)
        

class OutputWatchdog:
    def __init__(self, provider=None, model=None, api_key=None):
        self.llm = create_llm(provider, model, api_key)

    def scan(self, text, scanner_config):
        return run(self.llm, text, scanner_config)
