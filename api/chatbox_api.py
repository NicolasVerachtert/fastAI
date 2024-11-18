from fastapi import APIRouter
from schema.llm_dto import LLMResponseDTO, LLMQueryDTO
from service.rag import query_rag

router = APIRouter()

@router.post("/chatbox/")
async def query_llm(query: LLMQueryDTO) -> LLMResponseDTO:
    return query_rag(query)