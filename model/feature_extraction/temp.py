import sys
ROOT_DIR = "/home/miirzamiir/codes/nlp/legal_chatbot/model/feature_extraction"
sys.path.append(ROOT_DIR)
import article_extractor, law_extractor, org_extractor, time_extractor

# class FeatureExtractorAmir:
#     def __init__(self, text) -> None:
#         self.text = text
        
#         artext = article_extractor.article_extractor(self.text)
#         self.arts = artext.result

#         datext = time_extractor.time_extractor(self.text)
#         self.dates = datext.result
        
#         orgext = org_extractor.org_extractor(self.text)
#         self.orgs = orgext.find_org()

#         lawext = law_extractor.LawExtractor()
#         self.laws = lawext.extract(self.text)
    
#     def extract(self):
#         self.result = "متن وارد شده پردازش و اطلاعات کلیدی زیر از آن استخراج شد؛\n\n"

        
        
#         return self.result


# from ..dataset.dataset_types import LegalDataset

import re
from abc import ABC, abstractmethod
from typing import List, Tuple
from law_extractor import LawExtractor
from org_extractor import OrgExtractor
from article_extractor import ArticleExtractor
from time_extractor import TimeExtractor

from hazm import *


class FeatureExtractor:
    
    def __init__(
        self, normalizer = Normalizer,
        sentence_tokenizer = sent_tokenize,
        word_tokenizer = word_tokenize, 
        pos_tagger = POSTagger(model='resource/hazm_model/pos_tagger.model'),
        chunker = Chunker(model='resource/hazm_model/chunker.model')
        ) -> None:
      
        self._normalizer = normalizer
        self._sent_tokenizer = sentence_tokenizer
        self._word_tokenizer = word_tokenizer
        self._pos_tagger = pos_tagger
        self._chunker = chunker
        
        self._law_extractor = LawExtractor(normalizer, word_tokenizer, pos_tagger)
        self._org_extractor = OrgExtractor(normalizer, pos_tagger, chunker)
        self._art_extractor = ArticleExtractor()
        self._time_extractor = TimeExtractor(normalizer, word_tokenizer, pos_tagger)

        
    def extract(self, input: str) -> List[dict]:
        result = []
        span_bias = 0
        pattern = r"^.(\s*)"
        for sentence in self._sent_tokenizer(input):
            law_phrase = self._law_extractor.extract(sentence, span_bias)
            art_phrase = self._art_extractor.extract(sentence, span_bias)
            org_phrase = self._org_extractor.extract(sentence, span_bias)
            time_phrase = self._time_extractor.extract(sentence, span_bias)


            result.append(
                {
                    "Sentence": sentence,
                    "Article": art_phrase,
                    "Law": law_phrase,
                    "Organization": org_phrase,
                    "Date": time_phrase
                }
            )

            
            match = re.search(pattern, input[span_bias+len(sentence)-1:])
            span_bias += len(sentence)+len(match.group(1))
        return result
    
# text =  "هیئت وزیزان در جلسه ۱۸/۴/۹۹ به پیشنهاد ۳۸۶۵۴ مورخ ۱/۳/۹۷ وزارت تعاون، کار و رفاه اجتماعی به اتسناد اصل یک و سی وهشتم قانون اساسی جمهوری اسلامی ایران آیین نامه اجرایی بند خ ماده ۸۷ قانون برنامه ششم توسعه اقتصادی و اجتماعی و فرهنگی جمهوری اسلامی ایران -مصوب۱۳۹۵- را به شرح زیر تصویب کرد" 
# ext = FeatureExtractor()
# print(ext.extract(text))
