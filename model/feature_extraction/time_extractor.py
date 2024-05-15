from hazm import *
import re



class time_extractor(object):

    months = {
        ' فروردین' , 'اردیبهشت', 'خرداد',
        'تیر', 'مرداد', 'شهریور',
        ' مهر ', 'آبان', 'آذر',
        ' دی ', 'بهمن', 'اسفند'
    }

    keywords = {
        'ماه' ,'سال' , 'برج' , '/' , 'تاریخ'
    }
    def __init__(self , text):
        returnList = []
        tokenized_sentences = self.senTokenizer(text)

        for sentence in tokenized_sentences:
            dates = self.find_dates(sentence)
            returnList.append(dates)

        self.result = returnList

    def senTokenizer(self , text):

        sentences = sent_tokenize(text)
        return sentences
    
    def sentence_chuncking(self , sentence):

        tagger = POSTagger(model='resource/pos_tagger.model')
        chunker = Chunker(model='resource/chunker.model')

        chunks = []
        words = word_tokenize(sentence)
        tagged_words = tagger.tag(words)


        tree = chunker.parse(tagged_words)


        for subtree in tree.subtrees():
            if subtree.label() in ['NP', 'ADVP']:
                chunk_text = tree2brackets(subtree)
                chunks.append(chunk_text)

        return chunks
    
    def find_dates(self , sentence):
        shamsi_date_regex = r'\b(1[3-4][0-9]{2})[-/](0?[1-9]|1[0-2])[-/](0?[1-9]|[12][0-9]|3[01])\b'

        dates = re.findall(shamsi_date_regex, sentence)

        if dates == []:
            if any(month in sentence for month in self.months):
                chunking = self.sentence_chuncking(sentence)
                for i in range(len(chunking)):
                    if any(m in chunking[i] for m in self.months):
                        return chunking[i]            
            elif any(keyword in sentence for keyword in self.keywords):
                chunking = self.sentence_chuncking(sentence)
                for i in range(len(chunking)):
                    if any(k in chunking[i] for k in self.keywords):
                         return chunking[i] 
            else:
                return []
        else:
            return dates
                

                
# text = "  در تاریخ  بیست و چهارم اردیبهشت ماه 1402 ،قانون مبارزه مدنی آمد"
# extractor = time_extractor(text)
# print(extractor.result)
    