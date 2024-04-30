
# Dataset Factory Interface
from abc import ABC, abstractmethod

import gzip
import json
import pandas as pd


class LegalDatasetCreator(ABC):
    @abstractmethod
    def method1(self):
        pass

    @abstractmethod
    def method2(self):
        pass
    
    def gz_to_df(path: str) -> pd.DataFrame:
        with gzip.open(path, 'rb') as f:
            json_data = []
            for line in f:
                decoded_line = line.decode('utf-8')
                parsed_json = json.loads(decoded_line)
                json_data.append(parsed_json)
        df = pd.json_normalize(json_data)
        return(df)
    