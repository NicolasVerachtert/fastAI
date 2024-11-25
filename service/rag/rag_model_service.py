import logging
from schema.llm_dto import LLMQueryDTO, LLMResponseDTO
from .models import ModelQueryService
from .context import RAGPromptService


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
            # Use the RAG service to create the prompt
            prompt = self.rag_prompt_service.create_prompt(request)

            # Use the ModelQueryService to query the model with the prompt
            response = self.model_query_service.query(prompt)

            if response is None:
                raise RuntimeError("All models failed to respond.")

            return LLMResponseDTO(
                query_id=request.query_id,
                successful=True,
                query_response=response
            )

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return LLMResponseDTO(
                query_id=request.query_id,
                successful=False,
                query_response=("An unexpected error occurred." if request.query_lang == "en" else "Er is iets misgegaan. Contacteer de developers.")
            )