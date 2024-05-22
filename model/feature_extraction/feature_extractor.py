# from ..dataset.dataset_types import LegalDataset

from abc import ABC, abstractmethod
from typing import List, Tuple

class Extractor(ABC):
    @abstractmethod
    def extract(input: str) -> list:
        pass
    

class FeatureExtrator():
    
    def extract(input: str) -> dict:
        pass
    
    def doce_type_detection():
        pass
    
    def _get_span(self, input: str, phrases: List[str]) -> List[Tuple[str, int, int]]:
        index = 0
        result = []
        for phrase in phrases:
            start_search_text = phrase[:phrase.find(" ")]
            start_index = input.find(start_search_text, index)
            end_search_text = phrase[phrase.rfind(" "):]
            end_index = input.find(end_search_text, start_index)
            index = end_index+len(end_search_text)
            result.append((phrase, start_index,index))
        return result
    
