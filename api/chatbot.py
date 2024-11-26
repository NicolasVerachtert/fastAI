from fastapi import APIRouter, HTTPException, status
from schema.llm_dto import LLMResponseDTO, LLMQueryDTO
from service import RAGModelQueryService
import logging

logger = logging.getLogger("app")

router = APIRouter()

rag_query_service = RAGModelQueryService()

@router.post("/chatbot/", response_model=LLMResponseDTO)
async def query_llm(query: LLMQueryDTO) -> LLMResponseDTO:
    """
    Endpoint to query the language model.

    Args:
        query (LLMQueryDTO): Input query data transfer object.

    Returns:
        LLMResponseDTO: The response from the language model.
    """
    try:
        logger.info(f"Received query with ID: {query.session_id}")

        # Call the RAGModelQueryService to handle the query
        response_content = rag_query_service.query(query)

        logger.info(f"Successfully processed query with ID: {query.session_id}")
        return response_content
        

    except ValueError as ve:
        # If the error indicates invalid or missing client input, return a 400
        logger.error(f"Validation error for query ID {query.session_id}: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(ve)}",
        )
    except Exception as e:
        # Handle unexpected server errors
        logger.error(f"Unexpected error for query ID {query.session_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request.",
        )