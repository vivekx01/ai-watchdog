from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from .exceptions import LLMCreationError

def create_llm(provider=None, model=None, api_key=None):
    try:
        if provider is None or model is None:
            return None
        provider = provider.lower()
        if provider == "openai":
            return ChatOpenAI(model_name=model, openai_api_key=api_key, temperature=0)
        elif provider == "anthropic":
            return ChatAnthropic(model=model, anthropic_api_key=api_key, temperature=0)
        elif provider == "google":
            return ChatGoogleGenerativeAI(model=model, google_api_key=api_key, temperature=0)
        elif provider == "huggingface":
            llm = HuggingFaceEndpoint(
                repo_id=model,
                task="text-generation",
                huggingfacehub_api_token=api_key,
                temperature=0
            )        
            return ChatHuggingFace(llm=llm)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    except Exception as e:
        raise LLMCreationError(provider, model, str(e))
