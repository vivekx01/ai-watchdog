from .llm_factory import create_llm
from .pydantic_model_builder import build_dynamic_super_model
from .prompt_builder import build_super_prompt
from .exceptions import ScanExecutionError

def run(llm, text, scanner_config):
    name_list = [item["name"] for item in scanner_config]
    final_model = build_dynamic_super_model(name_list)
    final_prompt = build_super_prompt(text, scanner_config)

    structured_model = llm.with_structured_output(final_model)
    try:
        result = structured_model.invoke(final_prompt)
        return result.model_dump()
    except Exception as e:
        raise ScanExecutionError(text, e)

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
