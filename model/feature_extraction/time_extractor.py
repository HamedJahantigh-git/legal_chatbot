from hazm import *
import re

class time_extractor(object):

    months = {
        'فروردین', 'اردیبهشت', 'خرداد',
        'تیر', 'مرداد', 'شهریور',
        ' مهر ', 'آبان', 'آذر',
        ' دی ', 'بهمن', 'اسفند'
    }

    def __init__(self, text):
        returnList = []
        tokenized_sentences = self.senTokenizer(text)

        for sentence in tokenized_sentences:
            dates = self.find_dates(sentence)
            for date in dates:
                if date:
                    start, end = self.find_subtext_span(sentence, date)
                    returnList.append((date, start, end))

        self.result = returnList

    def senTokenizer(self, text):
        sentences = sent_tokenize(text)
        return sentences

    def sentence_chunking(self, sentence):
        tagger = POSTagger(model='resource/hazm_model/pos_tagger.model')
        chunker = Chunker(model='resource/hazm_model/chunker.model')

        chunks = []
        words = word_tokenize(sentence)
        tagged_words = tagger.tag(words)
        tree = chunker.parse(tagged_words)

        for subtree in tree.subtrees():
            # if subtree.label() in ['NP', 'ADVP']:
            chunk_text = ' '.join(word for word, tag in subtree.leaves())
            chunks.append(chunk_text)

        return chunks

    def find_dates(self, sentence):
        
        shamsi_date_regex_list ={
            r'\b\d{2,4}\s*/\s*\d{1,2}\s*/\s*\d{1,2}\b',
            r'\b\d{1,2}\s*/\s*\d{1,2}\s*/\s*\d{2,4}\b'
        }
        
        listOfDates = []
        for shamsi in shamsi_date_regex_list:
            dates = re.findall(shamsi, sentence)
            listOfDates.extend(dates)

        if any(month in sentence for month in self.months):
            chunks = self.sentence_chunking(sentence)
            if len(chunks)>1:
                for i in range(1,len(chunks)):
                    
                    if any(month in chunks[i] for month in self.months):
                            # print(chunks[i])
                            listOfDates.append(chunks[i])
        return listOfDates

    def find_subtext_span(self, text, subtext):
        current_index = 0
        subtext_parts = subtext.split()
        part_start = text.find(subtext_parts[0], current_index)
        part_end = text.find(subtext_parts[-1], part_start) + len(subtext_parts[-1])
        return part_start, part_end

# Example usage
# text =  "عطف به نامه شماره ۹۱۹۲/۳۰۱۸۶ مورخ ۲۰/۲/۱۳۸۴ در اجرای اصل یکصد و بیست و سوم (۱۲۳) قانون اساسی جمهوری اسلامی ایران قانون مدیریت خدمات کشوری مصوب ۸/۷/۱۳۸۶ کمیسیون مشترک رسیدگی به لایحه مدیریت خدمات کشوری مجلس شورای اسلامی مطابق اصل هشتاد و پنجم (۸۵) قانون اساسی جمهوری اسلامی ایران که به مجلس شورای اسلامی تقدیم گردیده بود، پس از موافقت مجلس با اجرای آزمایشی آن به مدت پنج سال در جلسه علنی مورخ 18/7/1385 و تأیید شورای محترم نگهبان در تاریخ بیست و چهارم مهر ماه، به پیوست ارسال می گردد." 
# extractor = time_extractor(text)
# print(extractor.result)
