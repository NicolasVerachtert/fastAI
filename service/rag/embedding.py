from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import GEMINI_KEY, GEMINI_EMBED_MODEL

def get_embedding_function():
    embedding_function = GoogleGenerativeAIEmbeddings(
        google_api_key=GEMINI_KEY,
        model=GEMINI_EMBED_MODEL,
    )
    return embedding_function