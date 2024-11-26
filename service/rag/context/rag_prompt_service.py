from typing import Optional, List

from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma

from schema import ChatHistory
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
    
    Answer the question in {language} based on the above context: {question}.
    """
)

PROMPT_TEMPLATE_WITH_HISTORY = (
    """
    You are a chatbot designed to help players understand the rules of the all popular game monopoly.
    Previously the player already asked following question(s) and you gave the following answer(s):
    {history}
    
    Answer the question based only on the following context:
    
    {context}
    
    ---
    
    Answer the question in {language} based on the above context: {question}.
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


    def create_prompt(self, request: LLMQueryDTO, history: List[ChatHistory]) -> Optional[str] :
        """
        Creates a prompt for querying the models by preparing the context using the RAG technique.
        """
        # Search the DB to retrieve relevant context
        # Ignore the warning: unsolved type error in lanchain_chroma doesn't allow casting multiple attributes to chromadb.types.Where object
        filter_lang_mode = {"$and": [{"game_mode": request.game_mode.name}, {"language": request.language.name}]}
        results = self.db.similarity_search_with_score(request.question, filter=filter_lang_mode, k=5)
        
        # No matching documents found
        if len(results) == 0:
            logger.info(f"No results for query: {request.question} with language: {request.language.name} and game mode: {request.game_mode.name}")
            return None

        sources = [doc.metadata.get("id", None) for doc, _score in results]
        logger.info(f"Query_ID: {request.session_id} - Sources: {sources}")


        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

        # History
        if len(history) > 0:
            history_data = [{"user_question": h.user_question, "bot_answer": h.bot_answer} for h in history]
            history_prompt = "\n".join([f"Q: {h['user_question']} A: {h['bot_answer']}" for h in history_data])
            prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_WITH_HISTORY)
            prompt = prompt_template.format(context=context_text, question=request.question, language=request.language.value, history=history_prompt)
        
        else:
            prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
            prompt = prompt_template.format(context=context_text, question=request.question, language=request.language.value)
        
        return prompt