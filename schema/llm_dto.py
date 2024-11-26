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
    session_id: UUID
    question: str
    language: SupportedLanguage
    game_mode: SupportedGameMode
    
    
class LLMResponseDTO(BaseModel):
    session_id: UUID
    successful: bool
    llm_response: str
