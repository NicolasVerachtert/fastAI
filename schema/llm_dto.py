from pydantic import BaseModel
from uuid import UUID
from enum import Enum

class SupportedLanguage(str, Enum):
    nl = 'nederlands'
    en = 'english'


class LLMQueryDTO(BaseModel):
    query_id: UUID
    query_text: str
    query_lang: SupportedLanguage
    
    
class LLMResponseDTO(BaseModel):
    query_id: UUID
    successful: bool
    query_response: str
