# from ..dataset.dataset_types import LegalDataset

from abc import ABC, abstractmethod
from typing import List, Tuple
from law_extractor import LawExtractor

from hazm import *
class Extractor(ABC):
    @abstractmethod
    def extract(input: str) -> list:
        pass
    

class FeatureExtrator():
    
    def __init__(
        self, normalizer = Normalizer,
        sentence_tokenizer = sent_tokenize,
        word_tokenizer = word_tokenize, 
        pos_tagger = POSTagger(model='../../resource/hazm_model/pos_tagger.model')
        ) -> None:
        self._normalizer = normalizer
        self._sent_tokenizer = sentence_tokenizer
        self._word_tokenizer = word_tokenizer
        self._pos_tagger = pos_tagger
        
        self._law_extractor = LawExtractor(normalizer, 
                                           word_tokenizer,
                                           pos_tagger)
        
    def extract(self, input: str) -> List[dict]:
        result = []
        for sentence in self._sent_tokenizer(input):
            law_phrase = self._law_extractor.extract(sentence)
            
    
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
    
