import logging

from repository import save_chat_history
from schema.llm_dto import LLMQueryDTO, LLMResponseDTO, SupportedLanguage
from .models import ModelQueryService
from .context import RAGPromptService
from repository import save_chat_history, get_chat_history


logger = logging.getLogger("app")

class RAGModelQueryService:
    def __init__(self):
        """
        Initialize the RAGModelQueryService with model names and the necessary services.
        """       

        # Initialize the RAGPromptService and ModelQueryService
        self.rag_prompt_service = RAGPromptService()
        self.model_query_service = ModelQueryService()


    def query(self, request: LLMQueryDTO) -> LLMResponseDTO:
        """
        Perform the entire query process: create a prompt and query the models.

        :param request: The query request containing the question and other metadata.
        :return: LLMResponseDTO with the model's response or error.
        """
        try:
            
            history = get_chat_history(request.session_id)
            
            
            # Use the RAG service to create the prompt
            prompt = self.rag_prompt_service.create_prompt(request, history)
            
            if prompt is None:
                return LLMResponseDTO(
                    session_id=request.session_id,
                    successful=False,
                    llm_response=( 
                        "Helaas beschik ik niet over de nodige informatie om op je vraag te antwoorden. Contacteer de developers van de game."
                        if request.language == SupportedLanguage.nl else
                        "Unfortunately I don't posses the necessary information to answer your question. Please contact the devs."
                    )
                )
            
            # Use the ModelQueryService to query the model with the prompt
            response = self.model_query_service.query(prompt)

            if response is None:
                raise RuntimeError("All models failed to respond.")

            save_chat_history(request.session_id, request.question, response)

            return LLMResponseDTO(
                session_id=request.session_id,
                successful=True,
                llm_response=response
            )

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return LLMResponseDTO(
                session_id=request.session_id,
                successful=False,
                llm_response=("An unexpected error occurred." if request.language == "en" else "Er is iets misgegaan. Contacteer de developers.")
            )