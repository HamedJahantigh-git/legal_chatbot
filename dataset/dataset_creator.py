
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
  
class LawTxetPreProcessor():
    
    def __init__(self, law_texts: list) -> None:
        self._law_texets = law_texts
        self._law_name_df = pd.DataFrame(columns=["law_index", "law_name"])
        self._madeh_df = pd.DataFrame(columns=["law_index", "madeh_index", "madeh_text"])
        self._is_df = False
        
    def build_df(self):
        title_list = []
        madeh_list = []
        madeh_index = []
        law_index = []
        counter = 0
        for text in self._law_texets:
            title_list.append(self.title_extractor(text))
            temp_madeh_list = self.madeh_extractor(text)
            law_index.extend([counter for i in temp_madeh_list])
            madeh_index.extend([i+1  for i in range(len(temp_madeh_list))])
            madeh_list.extend(temp_madeh_list)
            counter += 1
        law_index_list = [i for i in range(counter)]
        self._madeh_df = pd.DataFrame({"law_index": law_index,
                                    "madeh_index": madeh_index,
                                    "madeh_text": madeh_list})
        self._law_name_df = pd.DataFrame({"law_index": law_index_list,
                                          "law_name": title_list})
        
    def title_extractor(self, law_text: str) -> str:
        first_newline_index = law_text.find('\n')
        return law_text[:first_newline_index]
    
    def madeh_extractor(self, law_text: str)-> list:
        result = []
        
        pattern = r"(^.{0,1}ماده)"
        removed_regex = r"❯.*\n"
        notvalid_pattern = r"(^.{0,1}ماده.*مکرر\n)"
        
        cleaned_text = re.sub(removed_regex, "", law_text)
        matches = re.finditer(pattern, cleaned_text, flags=re.MULTILINE)
        not_valid_matches = re.finditer(notvalid_pattern, cleaned_text, flags=re.MULTILINE)
        indices = [match.start() for match in matches]
        not_valid_indices = [match.start() for match in not_valid_matches]
        valid_indices = [item for item in indices if item not in not_valid_indices]
        for i in range(len(valid_indices)):
            start = valid_indices[i]
            if i != len(valid_indices)-1:
                end = valid_indices[i+1]
                result.append(cleaned_text[start:end])
            else:
                result.append(cleaned_text[start:])
        return result
        
    def get_df(self) -> pd.DataFrame:
        if not self._is_df:
            self.build_df()
        return self._law_name_df, self._madeh_df 

        
             