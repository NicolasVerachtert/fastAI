import json
import os
from pathlib import Path
from typing import Dict, Any

import joblib
import pandas as pd

from schema import BoardGameDTO, Mechanic


class FeatureTransfomer:
    """
    A class responsible for applying data transformations to board game features. This includes:
    - Binning features like decade and play time.
    - Mapping mechanics to relevant clusters.
    - MultiLabelBinarizer transformations for domains and clusters.
    - Feature scaling using a pre-trained scaler.
    """

    def __init__(self, artifacts_path: str):
        try:
            transfs = self._load_json(artifacts_path, "data_transformation.json")
            # Bins
            self.decade_bins = transfs.get("decade_bins")
            self.decade_labels = transfs.get("decade_labels")
        
            self.play_time_bins = transfs.get("play_time_bins")
            self.play_time_labels = transfs.get("play_time_labels")
        
            # Mechanic Clusters
            self.mechanic_cluster_mapping = transfs.get("mechanic_cluster_mapping")
        
            # MultiLabelBinarizers
            self.domains_mlb = joblib.load(f'{artifacts_path}{os.sep}Domains_MLB.pkl')
            self.clusters_mlb = joblib.load(f'{artifacts_path}{os.sep}Clusters_MLB.pkl')
        
            # Normalisation Scaler
            self.scaler = joblib.load(f'{artifacts_path}{os.sep}Scaler.pkl')
            
        except FileNotFoundError as e:
            raise FileNotFoundError(f"One or more transformation or model files could not be found at the path: {artifacts_path}. Error: {str(e)}")


    @staticmethod
    def _load_json(folder_path: str, file_name: str) -> Dict[str, Any]:
        path = Path(folder_path + os.sep + file_name)
        if not path.is_file():
            raise FileNotFoundError(f"JSON file not found at: {folder_path + os.sep + file_name}")
    
        try:
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON file at {folder_path + os.sep + file_name}: {e}")
    
    
    @staticmethod
    def _bin(value: int, bins: list[int], labels: list[str]) -> int:
        return pd.cut([value], bins=bins, labels=labels).astype('category').codes[0]
    
    
    @staticmethod
    def _map_to_cluster(mechanics: list[Mechanic], clusters: Dict[str, int]) -> list[list[int]]:
        return [[clusters.get(mechanic) for mechanic in mechanics]]
    
    
    def transform(self, dto: BoardGameDTO) -> pd.DataFrame:
        """
        Transforms the provided BoardGameDTO object into a pandas DataFrame suitable for prediction by applying various 
        preprocessing steps, such as binning, scaling, encoding of domains, and mapping of mechanics to clusters.
    
        This method performs the following transformations on the input `dto` (BoardGameDTO):
        - **Binning**: The `year_published` and `play_time` features are binned into predefined categories.
        - **Scaling**: The `min_players`, `max_players`, and `min_age` features are normalized using a pre-trained scaler.
        - **Domain Encoding**: The domains of the board game are transformed using MultiLabelBinarizer (MLB) into binary format.
        - **Cluster Mapping**: The mechanics of the board game are mapped to clusters using a predefined mapping, then encoded using MLB.
    
        Args:
            dto (BoardGameDTO): A data transfer object containing the attributes of the board game. 
    
        Returns:
            pd.DataFrame: A DataFrame containing the transformed features, ready for use in making predictions. 
            This DataFrame includes:
                - Binned values for `year_published` and `play_time`.
                - Scaled values for `min_players`, `max_players`, and `min_age`.
                - One-hot encoded columns for the domains and clusters.
        
        Raises:
            ValueError: If the input DTO is missing required attributes or contains invalid data types.
        """
        # Binning
        year_bin = self._bin(dto.year_published, self.decade_bins, self.decade_labels)
        play_time_bin = self._bin(dto.play_time, self.play_time_bins, self.play_time_labels)

        # Creating Dict
        prediction_df = pd.DataFrame([{
            "Year Published Bins": year_bin,
            "Min Players": dto.min_players,
            "Max Players": dto.max_players,
            "Play Time Bins": play_time_bin,
            "Min Age": dto.min_age,
            "Amount_of_Mechanics": len(dto.mechanics)
        }])

        # Scaling
        to_scale_columns = ["Min Players", "Max Players", "Min Age", "Amount_of_Mechanics"]
        prediction_df[to_scale_columns] = self.scaler.transform(prediction_df[to_scale_columns])
    
        # Domains
        domains_enc = self.domains_mlb.transform([dto.domains])
        for i, class_name in enumerate(self.domains_mlb.classes_):
            prediction_df[f"Domains_{class_name}"] = domains_enc[:, i].tolist()
    
        # Clusters
        clusters = self._map_to_cluster(dto.mechanics, self.mechanic_cluster_mapping)
        clusters_enc = self.clusters_mlb.transform(clusters)
        for i, class_name in enumerate(self.clusters_mlb.classes_):
            prediction_df[f"Clusters_{class_name}"] = clusters_enc[:, i].tolist()
    
        return prediction_df
