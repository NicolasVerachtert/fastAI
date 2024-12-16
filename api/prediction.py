import logging

from fastapi import APIRouter, HTTPException, status

from schema import PredictionDTO, BoardGameDTO
from service import PredictionModelService

logger = logging.getLogger("app")

router = APIRouter()

prediction_model_service = PredictionModelService()

@router.post("/predict", response_model=PredictionDTO)
async def predict(board_game_dto: BoardGameDTO) -> PredictionDTO:
    """
    Endpoint to query the prediction model.

    Args:
        board_game_dto (BoardGameDTO): Input data transfer object.

    Returns:
        PredictionDTO: The response from the prediction model.
    """
    try:
        logger.info(f"Received request for prediction: {board_game_dto}")
        
        response = prediction_model_service.predict_board_game(board_game_dto)
        
        logger.info(f"Board game successfully predicted: {response}")
        return response
    
    except Exception as e:
        logger.error(f"Exception raised while prediction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request.",
        )
