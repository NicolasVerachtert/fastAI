import os

import joblib
import pandas as pd

from schema import PredictionDTO


class BoardGamePredictor:

    def __init__(self, artifacts_path: str):
        # Prediction Models
        self.rating_average_mdl = joblib.load(f'{artifacts_path}{os.sep}Rating_Average_Model.pkl')
        self.complexity_average_mdl = joblib.load(f'{artifacts_path}{os.sep}Complexity_Average_Model.pkl')
        self.popularity_score_mdl = joblib.load(f'{artifacts_path}{os.sep}Popularity_Score_Model.pkl')


    def predict(self, features_df: pd.DataFrame) -> PredictionDTO:
        """
        Predicts the average complexity, average rating, and popularity score of a board game using the provided features.

        Args:
            features_df (pd.DataFrame): A DataFrame containing the features of the board game for prediction.
        
        Returns:
            PredictionDTO: An object that contains the predicted values for the board game's average complexity, average rating,
            and popularity score.
        """
        return PredictionDTO(
            average_complexity=self.complexity_average_mdl.predict(features_df),
            average_rating=self.rating_average_mdl.predict(features_df),
            popularity_score=self.popularity_score_mdl.predict(features_df),
        )