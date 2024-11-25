from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import GEMINI_KEY, GEMINI_EMBED_MODEL
import logging

logger = logging.getLogger("app")

def get_embedding_function() -> GoogleGenerativeAIEmbeddings:
    """
    Create and return an embedding function using the GoogleGenerativeAIEmbeddings model.

    This function initializes an instance of the GoogleGenerativeAIEmbeddings class
    using a provided Google API key and model, and returns the embedding function.

    Returns:
    GoogleGenerativeAIEmbeddings: An instance of the GoogleGenerativeAIEmbeddings class
                                  configured with the GEMINI_KEY and GEMINI_EMBED_MODEL.
    """
    try:
        if not GEMINI_KEY:
            raise ValueError("GEMINI_KEY is not set. Please configure the Google API key.")
        if not GEMINI_EMBED_MODEL:
            raise ValueError("GEMINI_EMBED_MODEL is not set. Please configure the embedding model.")
    
    
        embedding_function = GoogleGenerativeAIEmbeddings(
            google_api_key=GEMINI_KEY,
            model=GEMINI_EMBED_MODEL,
        )
        return embedding_function
    
    except ValueError as ve:
        logger.error(f"Configuration error: {ve}")
        raise

    except Exception as e:
        logger.error(f"Unexpected error while initializing embedding function: {e}")
        raise