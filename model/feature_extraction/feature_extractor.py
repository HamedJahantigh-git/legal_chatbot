# from ..dataset.dataset_types import LegalDataset

from abc import ABC, abstractmethod

class Extractor(ABC):
    @abstractmethod
    def extract(input: str) -> list:
        pass
    

class FeatureExtrator():
    
    def extract(input: str) -> dict:
        pass
    
    def doce_type_detection():
        pass
    
