import re
from hazm import *
from typing import List, Tuple
from law_extractor import LawExtractor


class TimeExtractor(object):

    def __init__(
            self, normalizer = Normalizer,
            tokenizer = word_tokenize, 
            pos_tagger = POSTagger(model='resource/hazm_model/pos_tagger.model'),
            months = [
                "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
                "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
            ],
            days = [
                "یک", "یکم", "دو", "دوم", "سه", "سوم", "چهار", "چهارم", "پنج", "پنجم",
                "شش", "ششم", "هفت", "هفتم", "هشت", "هشتم", "نه", "نهم", "ده", "دهم",
                "یازده", "یازدهم", "دوازده", "دوازدهم", "سیزده", "سیزدهم",
                "چهارده", "چهاردهم", "پانزده", "پانزدهم", "شانزده", "شانزدهم",
                "هفده", "هفدهم", "هجده", "هجدهم", "نوزده", "نوزدهم", "بیست", "بیستم",
                "بیست و یک", "بیست و یکم", "بیست و دو", "بیست و دوم", "بیست و سه", "بیست و سوم",
                "بیست و چهار", "بیست و چهارم", "بیست و پنج", "بیست و پنجم",
                "بیست و شش", "بیست و ششم", "بیست و هفت", "بیست و هفتم",
                "بیست و هشت", "بیست و هشتم", "بیست و نه", "بیست و نهم",
                "سی", "سیم", "سی و یک", "سی و یکم"
            ],
            numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
                        '14', '15', '16', '17', '18', '19', '20', '21', '22', '23',
                        '24', '25', '26', '27', '28', '29', '30', '31','۱', '۲', 
                        '۳', '۴', '۵', '۶', '۷', '۸', '۹', '۱۰', '۱۱', '۱۲', '۱۳', '۱۴', '۱۵',
                        '۱۶', '۱۷', '۱۸', '۱۹', '۲۰', '۲۱', '۲۲', '۲۳', '۲۴', '۲۵', '۲۶', '۲۷', '۲۸', '۲۹', '۳۰', '۳۱',
                        '01', '02', '03', '04', '05', '06', '07', '08', '09',
                        '۰۱', '۰۲', '۰۳', '۰۴', '۰۵', '۰۶', '۰۷', '۰۸', '۰۹'
            ]) -> None:
            
            self._normalizer = normalizer()
            self._tokenizer = tokenizer
            self._pos_tagger = pos_tagger
            self._month_keyword = months
            self._days_keyword = days
            self._number_keyword = numbers
        
    def extract(self, sentence):
        
        shamsi_date_regex_list = [
            r'\b\d{2,4}\s*/\s*\d{1,2}\s*/\s*\d{1,2}\b',
            r'\b\d{1,2}\s*/\s*\d{1,2}\s*/\s*\d{2,4}\b'
        ]
        
        day_pattern = '|'.join(self._days_keyword)
        month_pattern = '|'.join(self._month_keyword)
        number_pattern =  '|'.join(self._number_keyword)
        written_date_pattern = rf'({day_pattern})\s*({month_pattern})\s*(هر)?\s*(ماه|سال)?\b'
        written_date_pattern_2 = rf'({number_pattern})\s*({month_pattern})\s*(هر)?\s*(ماه|سال)?\b'        
        listOfDates = []
        for shamsi in shamsi_date_regex_list:
            dates = re.findall(shamsi, sentence)
            listOfDates.extend(dates)
        
        written_dates = re.findall(written_date_pattern, sentence)
        formatted_written_dates = [' '.join(date).strip() for date in written_dates]
        listOfDates.extend(formatted_written_dates)

        written_dates_2 = re.findall(written_date_pattern_2, sentence)
        formatted_written_dates_2 = [' '.join(date).strip() for date in written_dates_2]
        listOfDates.extend(formatted_written_dates_2)

        return listOfDates

# Example usage
# text = "عطف به نامه شماره ۹۱۹۲/۳۰۱۸۶ مورخ ۲۰/۲/۱۳۸۴ در اجرای اصل یکصد و بیست و سوم (۱۲۳) قانون اساسی جمهوری اسلامی ایران قانون مدیریت خدمات کشوری مصوب ۸/۷/۱۳۸۶ کمیسیون مشترک رسیدگی به لایحه مدیریت خدمات کشوری مجلس شورای اسلامی مطابق اصل هشتاد و پنجم (۸۵) قانون اساسی جمهوری اسلامی ایران که به مجلس شورای اسلامی تقدیم گردیده بود، پس از موافقت مجلس با اجرای آزمایشی آن به مدت پنج سال در جلسه علنی مورخ 18/7/1385 و تأیید شورای محترم نگهبان در تاریخ بیست و چهارم مهر ماه، به پیوست ارسال می گردد و در ۲۰ اردیبهشت هر ماه."
# extractor = Time()
# result = extractor.extract(text)
# print(result)
