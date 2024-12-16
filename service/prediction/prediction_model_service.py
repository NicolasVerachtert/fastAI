import logging
from config import PREDICTION_ARTIFACTS_PATH

from schema import BoardGameDTO, PredictionDTO
from service.prediction.board_game_predictor import BoardGamePredictor
from service.prediction.feature_transformer import FeatureTransfomer

logger = logging.getLogger("app")

class PredictionModelService:
    def __init__(self):
        self.transformer = FeatureTransfomer(PREDICTION_ARTIFACTS_PATH)
        self.predictor = BoardGamePredictor(PREDICTION_ARTIFACTS_PATH)
        
    def predict_board_game(self, board_game_dto: BoardGameDTO) -> PredictionDTO:
        encoded = self.transformer.transform(board_game_dto)
        return self.predictor.predict(encoded)