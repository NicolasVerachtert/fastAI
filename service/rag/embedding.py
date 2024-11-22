from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import GEMINI_KEY, GEMINI_EMBED_MODEL

def get_embedding_function() -> GoogleGenerativeAIEmbeddings:
    """
    Create and return an embedding function using the GoogleGenerativeAIEmbeddings model.

    This function initializes an instance of the GoogleGenerativeAIEmbeddings class
    using a provided Google API key and model, and returns the embedding function.

    Returns:
    GoogleGenerativeAIEmbeddings: An instance of the GoogleGenerativeAIEmbeddings class
                                  configured with the GEMINI_KEY and GEMINI_EMBED_MODEL.
    """
    embedding_function = GoogleGenerativeAIEmbeddings(
        google_api_key=GEMINI_KEY,
        model=GEMINI_EMBED_MODEL,
    )
    return embedding_function