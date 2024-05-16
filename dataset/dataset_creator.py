
# Dataset Factory Interface
from abc import ABC, abstractmethod

import gzip
import json
import pandas as pd

from hazm import *

import os, re

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
    
    def __init__(self) -> None:
        self._normalizer = Normalizer()
     
    def gz_to_df(self, path: str) -> pd.DataFrame:
        with gzip.open(path, 'rb') as f:
            json_data = []
            for line in f:
                decoded_line = line.decode('utf-8')
                parsed_json = json.loads(decoded_line)
                json_data.append(parsed_json)
        df = pd.json_normalize(json_data)
        return(df)
    
    def merge_txt_files(self, folder_path:str, output_file:str, separator:str):
        content = ''
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = content + infile.read()
                    content = content + separator
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(content)
            
    def case_to_df(self, data: list) -> pd.DataFrame:
        title, number, date, type, text = [], [], [], [], []
        data = [self._normalizer.normalize(text) for text in data]
        for case in data:
            index = [match.start() for match in re.finditer(r'\n', case)]
            title.append(case[7:index[0]])
            number.append(case[index[0]+21:index[1]])
            date.append(case[index[1]+21:index[2]])
            type.append(case[index[2]+11:index[3]])
            text.append(case[index[3]+1:])
        df = pd.DataFrame({
            "title": title,
            "number": number,
            "date": date,
            "type": type,
            "text": text
        })
        return df
    
    def ekhtebar_news(self, data: pd.DataFrame) -> pd.DataFrame:
        ek_news = data[data["category.major"] == "News"]\
            [["title", "content", "date", "url", "tags", "category.original"]]
        ek_news = ek_news.rename(columns={'content': 'content_html'})
        content = [self._normalizer.normalize(''.join([item['text'] for item in data])) for data in ek_news.content_html]

        # for data in ek_news.content_html:
        #     content = [''.join([item['text'] for item in data])) ]
        ek_news["content"] = content
        return ek_news

        
            
      