# # from ..dataset.dataset_types import LegalDataset

# from abc import ABC, abstractmethod

# class Extractor(ABC):
#     @abstractmethod
#     def extract(input: str) -> list:
#         pass
    

# class FeatureExtrator():
    
#     def extract(input: str) -> dict:
#         pass
    
#     def doce_type_detection():
#         pass
    

import article_extractor, law_extractor, org_extractor, time_extractor

class FeatureExtractor:
    def __init__(self, text) -> None:
        self.text = text
        
        artext = article_extractor.article_extractor(self.text)
        self.art = artext.result

        datext = time_extractor.time_extractor(self.text)
        self.date = datext.result
        
        orgext = org_extractor.org_extractor(self.text)
        self.org = orgext.find_org()

        lawext = law_extractor.LawExtractor()
        self.law = lawext.extract(self.text)
    
    def extract(self):
        self.result = "متن وارد شده پردازش و اطلاعات کلیدی زیر از آن استخراج شد؛\n"

        self.result += 'مواد اشاره شده در متن: '
        if self.art == []:
            self.result += 'هیچ عنوان ماده ای پیدا نشد.\n'
        else:
            self.result += f'{self.art}\n\n'
        
        self.result += 'قوانین اشاره شده در متن: '
        if self.law == []:
            self.result += 'هیچ عنوان قانونی پیدا نشد.\n'
        else:
            self.result += f'{self.law}\n\n'

        self.result += 'نام نهادهای اشاره شده در متن: '
        if self.org == []:
            self.result += 'هیچ نام نهادی پیدا نشد.\n'
        else:
            self.result += f'{self.org}\n\n'

        self.result += 'تاریخ های اشاره شده در متن: '
        if self.date == []:
            self.result += 'هیچ تاریخی پیدا نشد.\n'
        else:
            self.result += f'{self.date}\n\n'

        
        return self.result
    

text =  "هیت وزیزان در جلسه ۱۸/۴/۹۹ به پیشنهاد ۳۸۶۵۴ مورخ ۱/۳/۹۷ وزارت تعاون، کار و رفاه اجتماعی به اتسناد اصل یک و سی وهشتم قانون اساسی جمهوری اسلامی ایران آیین نامه اجرایی بند خ ماده ۸۷ قانون برنامه ششم توسعه اقتصادی و اجتماعی و فرهنگی جمهوری اسلامی ایران -مصوب۱۳۹۵- را به شرح زیر تصویب کرد" 
ext = FeatureExtractor(text)
print(ext.extract())
