import sys
ROOT_DIR = "/home/miirzamiir/codes/nlp/legal_chatbot/model/feature_extraction"
sys.path.append(ROOT_DIR)
import article_extractor, law_extractor, org_extractor, time_extractor

class FeatureExtractor:
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
    

# text =  "هیئت وزیزان در جلسه ۱۸/۴/۹۹ به پیشنهاد ۳۸۶۵۴ مورخ ۱/۳/۹۷ وزارت تعاون، کار و رفاه اجتماعی به اتسناد اصل یک و سی وهشتم قانون اساسی جمهوری اسلامی ایران آیین نامه اجرایی بند خ ماده ۸۷ قانون برنامه ششم توسعه اقتصادی و اجتماعی و فرهنگی جمهوری اسلامی ایران -مصوب۱۳۹۵- را به شرح زیر تصویب کرد" 
# ext = FeatureExtractor(text)
# print(ext.extract())
