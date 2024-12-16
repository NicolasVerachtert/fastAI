import logging
from typing import Optional

from .model_registry import get_models_by_priority

logger = logging.getLogger("app")


class ModelQueryService:
    def __init__(self):
        """
        Initialize the service. Fetch models from the registry in priority order.
        """
        self.models = get_models_by_priority()

    def query(self, prompt: str) -> Optional[str]:
        """
        Query the models in order of priority. 
        Returns the first successful response or None if all models fail.
        """
        for model in self.models:
            try:
                logger.info(f"Querying model: {model}")
                response = model.invoke(prompt)  # Use LangChain's `invoke` method
                if response and hasattr(response, "content"):
                    logger.info("Model responded successfully.")
                    return response.content
                else:
                    logger.warning("Model returned an invalid or empty response.")
            except Exception as e:
                logger.error(f"Model failed with error: {e}")
                continue  # Proceed to the next model if one fails

        logger.error("All models failed to respond.")
        return None