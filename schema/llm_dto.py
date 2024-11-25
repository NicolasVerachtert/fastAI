from pydantic import BaseModel
from uuid import UUID
from enum import Enum

class SupportedLanguage(str, Enum):
    nl = 'nederlands'
    en = 'english'
    
class SupportedGameMode(str, Enum):
    classic = 'classic'
    belgium = 'belgium'


class LLMQueryDTO(BaseModel):
    query_id: UUID
    query_text: str
    query_lang: SupportedLanguage
    query_game_mode: SupportedGameMode
    
    
class LLMResponseDTO(BaseModel):
    query_id: UUID
    successful: bool
    query_response: str
