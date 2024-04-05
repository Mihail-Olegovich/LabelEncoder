import pandas as pd
from typing import List
import json

class LabelEncoder:
    def __init__(self, df, datetime_features: List[str] = None, map_name=None):
        self.df = df.copy()
        self.map_name = map_name if map_name else "Untitled map"
        if datetime_features is not None:
            self.datetime_features = datetime_features 
        else:
            self.datetime_features = ['']
        for col in self.df.columns:
            if pd.api.types.is_datetime64_any_dtype(self.df[col]):
                self.df[col] = self.df[col].astype(str)
    

    def create_map(self):
        self.map = {}
        self.categorical_features = self.df.select_dtypes(include=['object']).columns 
        for col in self.categorical_features:
            self.map[col] = {}
            if col not in self.datetime_features:
                for index, sorted_feature_value in enumerate(self.df[col].sort_values().unique()):
                    self.map[col][sorted_feature_value] = index
            else:
                for index, feature_value in enumerate(self.df[col].unique()):
                    self.map[col][feature_value] = index

    def save_map(self, folder: str = None):
        with open(f"{folder}/{self.map_name}", 'w') as f:
            json.dump(self.map, f)

    def mapped_df(self, from_file: bool = False, folder: str = None, test_data = None):
        if test_data is None:
            mapped_df = self.df.copy()
        else:
            mapped_df = test_data.copy()

        if from_file:
            with open(f"{folder}/{self.map_name}", 'r') as f:
                mapper = json.load(f)            
        else:
            mapper = self.map

        for col in mapper.keys():
            mapped_df[col] = mapped_df[col].map(mapper[col])
        
        mapped_df.fillna(-1, inplace=True)

        return mapped_df
    
    def recovered_df(self, mapped_data, from_file: bool = False, folder: str = None):
        recovered_df = mapped_data.copy()
        if from_file:
            with open(f"{folder}/{self.map_name}", 'r') as f:
                mapper = json.load(f)            
        else:
            mapper = self.map

        for col in mapper.keys():
            reverse_mapper = {v: k for k, v in mapper[col].items()}
            recovered_df[col] = recovered_df[col].map(reverse_mapper)
        
        recovered_df.fillna(-1, inplace=True)

        return recovered_df