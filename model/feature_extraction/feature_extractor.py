import sys
ROOT_DIR = "/home/miirzamiir/codes/nlp/legal_chatbot/model/feature_extraction"
sys.path.append(ROOT_DIR)
import article_extractor, law_extractor, org_extractor, time_extractor

class FeatureExtractorAmir:
    def __init__(self, text) -> None:
        self.text = text
        
        artext = article_extractor.article_extractor(self.text)
        self.arts = artext.result

        datext = time_extractor.time_extractor(self.text)
        self.dates = datext.result
        
        orgext = org_extractor.org_extractor(self.text)
        self.orgs = orgext.find_org()

        lawext = law_extractor.LawExtractor()
        self.laws = lawext.extract(self.text)
    
    def extract(self):
        self.result = "متن وارد شده پردازش و اطلاعات کلیدی زیر از آن استخراج شد؛\n\n"

        self.result += 'مواد اشاره شده در متن:\n'
        if self.arts == []:
            self.result += 'هیچ عنوان ماده ای پیدا نشد.\n'
        else:
            for art in self.arts:
                self.result += f'{art[0]}\n(از کاراکتر {art[1]} تا کاراکتر {art[2]})\n\n'
        
        self.result += '\nقوانین اشاره شده در متن:\n'
        if self.laws == []:
            self.result += 'هیچ عنوان قانونی پیدا نشد.\n'
        else:
            for law in self.laws:
                self.result += f'{law[0]}\n(از کاراکتر {law[1]} تا کاراکتر {law[2]})\n\n'

        self.result += '\nنام نهادهای اشاره شده در متن:\n'
        if self.orgs == []:
            self.result += 'هیچ نام نهادی پیدا نشد.\n'
        else:
            for org in self.orgs:
                self.result += f'{org[0]}\n(از کاراکتر {org[1]} تا کاراکتر {org[2]})\n\n'

        self.result += '\nتاریخ های اشاره شده در متن:\n'
        if self.dates == []:
            self.result += 'هیچ تاریخی پیدا نشد.\n'
        else:
            for date in self.dates:
                self.result += f'{date[0]}\n(از کاراکتر {date[1]} تا کاراکتر {date[2]})\n\n'

        
        return self.result


# from ..dataset.dataset_types import LegalDataset

from abc import ABC, abstractmethod
from typing import List, Tuple
from law_extractor import LawExtractor
from org_extractor import org_extractor

from hazm import *
class Extractor(ABC):
    @abstractmethod
    def extract(input: str) -> list:
        pass
    

class FeatureExtrator:
    
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
        # self._org_extractor = org_extractor()
        # artext = article_extractor.article_extractor(self.text)
        # self.arts = artext.result

        # datext = time_extractor.time_extractor(self.text)
        # self.dates = datext.result
        
        # orgext = org_extractor.org_extractor(self.text)
        # self.orgs = orgext.find_org()
        
    def extract(self, input: str) -> List[dict]:
        result = []
        span_bias = 0
        for sentence in self._sent_tokenizer(input):
            law_phrase = self._law_extractor.extract(sentence)
            artext = article_extractor.article_extractor(sentence)
            article_phrase = artext.result[0]

            datext = time_extractor.time_extractor(sentence)
            dates_phrase = datext.result
            
            orgext = org_extractor(sentence)
            orgs_phrase = orgext.find_org()
            result.append({
                "Article": self._get_span(sentence, article_phrase, span_bias),
                "Law": self._get_span(sentence, law_phrase, span_bias),
                "Organization": self._get_span(sentence, orgs_phrase, span_bias),
                "Date": self._get_span(sentence, dates_phrase, span_bias)
            })
            span_bias += len(sentence)
        return result
    
    def doce_type_detection():
        pass
    
    def _get_span(self, input: str, phrases: List[str], bias: int) -> List[Tuple[str, int, int]]:
        index = 0
        result = []
        for phrase in phrases:
            start_search_text = phrase[:phrase.find(" ")]
            start_index = input.find(start_search_text, index)
            end_search_text = phrase[phrase.rfind(" "):]
            end_index = input.find(end_search_text, start_index)
            index = end_index+len(end_search_text)
            result.append((phrase, "Span: "+f'[{start_index+bias}, {index+bias}]'))
        return result
    


# text =  "هیئت وزیزان در جلسه ۱۸/۴/۹۹ به پیشنهاد ۳۸۶۵۴ مورخ ۱/۳/۹۷ وزارت تعاون، کار و رفاه اجتماعی به اتسناد اصل یک و سی وهشتم قانون اساسی جمهوری اسلامی ایران آیین نامه اجرایی بند خ ماده ۸۷ قانون برنامه ششم توسعه اقتصادی و اجتماعی و فرهنگی جمهوری اسلامی ایران -مصوب۱۳۹۵- را به شرح زیر تصویب کرد" 
# ext = FeatureExtractor(text)
# print(ext.extract())
