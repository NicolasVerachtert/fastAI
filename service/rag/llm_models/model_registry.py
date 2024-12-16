from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI

from config import GEMINI_KEY, GEMINI_LLM_MODEL, MISTRAL_KEY, MISTRAL_LLM_MODEL
from typing import List, Tuple, Optional
import logging


logger = logging.getLogger("app")


MODEL_REGISTRY: List[Tuple[int, BaseChatModel]] = []


def register_model(priority: int, model: Optional[BaseChatModel]) -> None:
    """Register models with a priority."""
    if model is not None:
        MODEL_REGISTRY.append((priority, model))
        MODEL_REGISTRY.sort(key=lambda x: x[0])  # Sort by priority
    else:
        logger.warning(f"Attempted to register a None model with priority {priority}.")


def get_models_by_priority() -> List[BaseChatModel]:
    """Retrieve all models sorted by priority."""
    return [model for _, model in MODEL_REGISTRY]


def get_gemini_model() -> Optional[BaseChatModel]:
    """Initialize the Gemini model."""
    try:
        return ChatGoogleGenerativeAI(
            google_api_key=GEMINI_KEY,
            model=GEMINI_LLM_MODEL,
            temperature=0,
            timeout=None,
            max_retries=2,
        )
    except Exception as e:
        logger.error(f"Failed to initialize Gemini model: {e}")
        return None


def get_mistral_model() -> Optional[BaseChatModel]:
    """Initialize the Mistral model."""
    try:
        return ChatMistralAI(
            mistral_api_key=MISTRAL_KEY,
            model=MISTRAL_LLM_MODEL,
            temperature=0,
            timeout=10,
            max_retries=2,
        )
    except Exception as e:
        logger.error(f"Failed to initialize Gemini model: {e}")
        return None


register_model(0, get_gemini_model())
register_model(1, get_mistral_model())
