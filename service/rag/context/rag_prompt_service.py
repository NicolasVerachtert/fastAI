from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from schema.llm_dto import LLMQueryDTO
from config import CHROMA_PATH, CHROMA_RESET
import logging

from .google_bucket import download_files_from_gcs
from .chroma import init_chroma
from .embedding import get_embedding_function

logger = logging.getLogger("app")



PROMPT_TEMPLATE = (
    """
    You are a chatbot designed to help players understand the rules of the all popular game monopoly.
    Answer the question based only on the following context:
    
    {context}
    
    ---
    
    Answer the question based on the above context: {question}.
    """
)


class RAGPromptService:
    def __init__(self):
        """
        Initialize the RAGPromptService with an embedding function and Chroma DB.
        """
        
        # Download the necessary documents from GCS
        download_files_from_gcs()
        init_chroma(CHROMA_RESET)
    
        self.db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())


    def create_prompt(self, request: LLMQueryDTO) -> str:
        """
        Creates a prompt for querying the models by preparing the context using the RAG technique.
        """
        # Search the DB to retrieve relevant context
        results = self.db.similarity_search_with_score(request.query_text, k=5)

        sources = [doc.metadata.get("id", None) for doc, _score in results]
        logger.info(f"Query_ID: {request.query_id} - Sources: {sources}")

        # Join the relevant context pieces to form the context text
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

        # Create the prompt template
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

        # Format the prompt with the context and question
        prompt = prompt_template.format(context=context_text, question=request.query_text)

        return prompt