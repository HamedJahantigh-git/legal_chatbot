
import pandas as pd
import re

from model.case_analyzer.case_retrieval import BM25Retrival
from model.feature_extraction.feature_extractor import FeatureExtractor
    
class Run():
    
    def __init__(self) -> None:
        case_df = pd.read_csv("resource/case/case.csv")
        self._case_matcher = BM25Retrival(case_df.text.tolist())
        self._feature_extractor = FeatureExtractor()
        
    def run(self, input: str):
        features = self._feature_extractor.extract(input)
        
        pattern = r'<پرونده: (\d+)>'
        match = re.search(pattern, input)
        if match:
            number = int(match.group(1))
            case = self._case_matcher.get_similar_text(input, number)
        else:
            case = None
        return features, case             

# r = Run()
# a = r.run("بنا بر اعلام گزارش پایگاه اطلاع رسانی دولت، هیئت وزیران در جلسه ۱۳۹۷/۱/۲۲ به استناد اصل یکصد و سی و هشتم قانون اساسی جمهوری اسلامی ایران و تبصره (۳) ماده (۷) قانون مبارزه با قاچاق کالا و ارز – مصوب ۱۳۹۲- و به منظور ساماندهی و مدیریت بازار ارز تصویب کرد. <پرونده:3 >")
# print(a)