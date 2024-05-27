
import pandas as pd
import re

from model.case_analyzer.case_retrieval import BM25Retrival
from model.feature_extraction.feature_extractor import FeatureExtractor
    
class Run():
    
    def __init__(self) -> None:
        case_df = pd.read_csv("resource/case/case.csv")
        self._case_matcher = BM25Retrival(case_df.text.tolist())
        # self._feature_extractor = FeatureExtractor()
        
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