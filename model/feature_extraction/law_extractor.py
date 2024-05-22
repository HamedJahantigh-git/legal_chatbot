from typing import List, Tuple
import re
from hazm import *

class LawExtractor():
    
    def __init__(
        self, normalizer = Normalizer,
        tokenizer = word_tokenize, 
        pos_tagger = POSTagger(model='../../resource/hazm_model/pos_tagger.model'),
        keywords = [
        'قانون' , 'قوانین' , 'آیین نامه'  , 'آیین‌نامه' ,
        'اساس نامه' , 'اساس‌نامه']) -> None:
        
        self._normalizer = normalizer()
        self._tokenizer = tokenizer
        self._pos_tagger = pos_tagger
        self._keywords = keywords
        
    def extract(self, input: str) -> List[str]:
        normal_text = self._normalizer.normalize(input)
        normal_text = normal_text.replace("،", " ،")
        tokens = self._tokenizer(normal_text)
        pos_tag = self._pos_tagger.tag(tokens)
        first_phrases = self._pos_analysis(pos_tag)
        phrase = self._regex_analysis(normal_text, first_phrases)
        return phrase, first_phrases
    
    def _pos_analysis(self, pos_list: List) -> List:
        accept_tok = [index for index, tok in enumerate(pos_list)
                      if tok[0] in self._keywords and "EZ" in tok[1]]
        result =[]
        for i in accept_tok:
            index = i+1
            while ("EZ" in pos_list[index][1])or\
                ("EZ" in pos_list[index-1][1]):
                index += 1  
            # while (pos_list[index][0] == "،"  and (pos_list[index+2][0] in ["،", 'و']))or\
            #     (pos_list[index][0] == "و"  and (pos_list[index-2][0] == "،"))or\
            #     (pos_list[index-1][0] == "،" and (pos_list[index+1][0] in ["،", 'و'])or\
            #     (pos_list[index-1][0] == "و" )):
            #     index += 1
            result.append(" ".join([word for word,_ in pos_list[i:index]]))
        return result
    
    def _regex_analysis(self, input, phrases: List[str])-> List[Tuple[str, int, int]]:
        pattern = r"^(?:، \b\w+\b)+ و \b\w+\b"
        result = []
        start = 0
        for phrase in phrases:
            end_index = self._get_end_span(input, phrase, start)
            start = end_index
            match = re.search(pattern, input[end_index+1:])
            first_match = ""
            if match:
                first_match = match.group()
            result.append(phrase+first_match)
        return result
    
    def _get_end_span(self, input: str, phrase: str, start: int) -> int:
        index = start
        start_search_text = phrase[:phrase.find(" ")]
        start_index = input.find(start_search_text, index)
        end_search_text = phrase[phrase.rfind(" "):]
        end_index = input.find(end_search_text, start_index)
        index = end_index+len(end_search_text)
        return index
        
    
    