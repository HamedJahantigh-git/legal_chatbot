import re
from hazm import *
from typing import List, Tuple

class ArticleExtractor(object):

    def __init__(
        self, normalizer=Normalizer,
        tokenizer=word_tokenize, 
        pos_tagger=POSTagger(model='resource/hazm_model/pos_tagger.model'),
        articleKeywords={'ماده', 'مواد', 'اصل', 'اصول'},
        lawKeywords=['قانون', 'قوانین', 'آیین نامه', 'آیین‌نامه', 'اساس نامه', 'اساس‌نامه']) -> None:
        
        self._normalizer = normalizer()
        self._tokenizer = tokenizer
        self._pos_tagger = pos_tagger
        self._article_keyword = articleKeywords
        self._law_keyword = lawKeywords

    def extract(self, input: str, bias) -> List[Tuple[str, int, int]]:
        sentences = self.senTokenizer(input)
        result = [res for sentence in sentences
                  for res in self.find_article(self.sentence_chunking(sentence), sentence, bias)]
        return result

    def senTokenizer(self, text):
        return sent_tokenize(text)

    def sentence_chunking(self, sentence):
        tagger = self._pos_tagger
        chunker = Chunker(model='resource/hazm_model/chunker.model')
        tagged_words = tagger.tag(word_tokenize(sentence))
        chunks = [tree2brackets(subtree) for subtree in chunker.parse(tagged_words).subtrees() 
                  if subtree.label() in ['NP', 'ADVP', 'ADJP']]
        return chunks

    def find_article(self, chunks, text, bias):
        article_pattern = re.compile('|'.join(map(re.escape, self._article_keyword)))
        law_pattern = re.compile('|'.join(map(re.escape, self._law_keyword)))
        article_indices = [i for i, chunk in enumerate(chunks) if article_pattern.search(chunk)]        
        law_indices = [i for i, chunk in enumerate(chunks) if law_pattern.search(chunk)] 
        lists =  [self.find_all_in_one(chunks[i], text, bias) if i in law_indices 
                else self.find_it(chunks[i], self._article_keyword, text, bias) for i in article_indices]
        
        returnList = []
        for i in lists:
            if i:
                x = i[0].split()
                if len(x)>1:
                    returnList.append(i)
        return returnList

    def find_all_in_one(self, chunk, text, bias):
        words = chunk.split()
        start = next(i for i, w in enumerate(words) if any(kw in w for kw in self._article_keyword))
        end = next(i for i, w in enumerate(words) if any(kw in w for kw in self._law_keyword))
        article = ' '.join(words[start:end])
        return self.find_in_text(text, article, bias)

    def find_it(self, chunk, keyChunk, text, bias):
        words = chunk.split()
        start = next(i for i, w in enumerate(words) if any(kw in w for kw in keyChunk))
        article = ' '.join(words[start:])
        return self.find_in_text(text, article, bias)

    def normalize_text(self, text):
        return Normalizer().normalize(text)

    def find_in_text(self, main_string, substring, bias):
        normalized_substring = self.normalize_text(substring)
        start_index = main_string.find(normalized_substring)
        # return (start_index, start_index + len(normalized_substring) - 1) if start_index != -1 else (-1, -1)

        for m in re.finditer(re.escape(normalized_substring), main_string):
            return([normalized_substring, m.start()+bias, m.end()+bias])

# text = "عطف به نامه شماره ۹۱۹۲/۳۰۱۸۶ مورخ ۲۰/۲/۱۳۸۴ در اجرای اصل یکصد و بیست و سوم (۱۲۳) قانون اساسی جمهوری اسلامی ایران قانون مدیریت خدمات کشوری مصوب ۸/۷/۱۳۸۶ کمیسیون مشترک رسیدگی به لایحه مدیریت خدمات کشوری مجلس شورای اسلامی مطابق اصل هشتاد و پنجم (۸۵) قانون اساسی جمهوری اسلامی ایران که به مجلس شورای اسلامی تقدیم گردیده بود، پس از موافقت مجلس با اجرای آزمایشی آن به مدت پنج سال در جلسه علنی مورخ ۱۸/۱۱/۱۳۸۵ و تأیید شورای محترم نگهبان،  به پیوست ارسال می گردد."
# extractor = ArticleExtractor()
# print(extractor.extract(text, 0))
