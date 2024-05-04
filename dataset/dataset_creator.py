
# Dataset Factory Interface
from abc import ABC, abstractmethod

import gzip
import json
import pandas as pd

import os

class LegalDatasetCreator(ABC):
    @abstractmethod
    def create(self):
        pass
    
    def create_case_dataset(df: pd.DataFrame) :
        pass
    
    def create_blog_dataset(df: pd.DataFrame) :
        pass
    
    def create_law_dataset(df: pd.DataFrame) :
        pass
    
    def create_news_dataset(df: pd.DataFrame) :
        pass
    
    
class LawDatasetCreator():
    
    def __init__(self, data_paths: list) -> None:
        super().__init__()
        self._data_paths = data_paths
    
    def create(self):
        pass
    
    def _load_data(self):
        for i in self._data_paths:
            pass
    
    def _txt_to_df (self, data_str_list):
        pass
 
 
 # Dataset PreProcessor for notbook
 
class LegalDatasetPreProcessor():
     
    def gz_to_df(self, path: str) -> pd.DataFrame:
        with gzip.open(path, 'rb') as f:
            json_data = []
            for line in f:
                decoded_line = line.decode('utf-8')
                parsed_json = json.loads(decoded_line)
                json_data.append(parsed_json)
        df = pd.json_normalize(json_data)
        return(df)
    
    def merge_txt_files(folder_path:str, output_file:str, separator:str):
        content = ''
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = content + infile.read()
                    content = content + separator
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(content)
      