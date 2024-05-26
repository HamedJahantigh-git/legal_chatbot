from enum import Enum

import pandas as pd

from model.case_analyzer.case_retrieval import BM25Retrival
from model.feature_extraction.feature_extractor import FeatureExtrator

class Command(Enum):
    END = "پایان"
    
    
class Run():
    
    def __init__(self) -> None:
        case_df = pd.read_csv("resource/case/case.csv")
        self._case_matcher = BM25Retrival(case_df.text.tolist())
        self._feature_extractor = FeatureExtrator()
    def run(self):
        input = " "
        while input != Command.END.value:
           input = input("درخواست مورد نظر را انتخاب کنید:","\n",
                         "1- استخراج ویژگی های متن",
                         "2- ارجاع پرونده مشابه",
                         "3- راهنما"
                         "4- پایان")
                        
    
chat = Run()
chat.run()