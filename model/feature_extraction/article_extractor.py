import re
from hazm import *

class ArticleExtractor(object):

    articleKeywords = {'ماده', 'مواد', 'اصل', 'اصول'}
    lawKeywords = ['قانون', 'قوانین', 'آیین نامه', 'آیین‌نامه', 'اساس نامه', 'اساس‌نامه']

    def __init__(self, text):
        self.result = [res for sentence in self.senTokenizer(text)
                             for res in self.find_article(self.sentence_chunking(sentence), sentence)]

    def senTokenizer(self, text):
        return sent_tokenize(text)

    def sentence_chunking(self, sentence):
        tagger = POSTagger(model='resource/hazm_model/pos_tagger.model')
        chunker = Chunker(model='resource/hazm_model/chunker.model')
        tagged_words = tagger.tag(word_tokenize(sentence))
        chunks = [tree2brackets(subtree) for subtree in chunker.parse(tagged_words).subtrees() 
                  if subtree.label() in ['NP', 'ADVP', 'ADJP']]
        return chunks

    def find_article(self, chunks, text):
        article_indices = [i for i, chunk in enumerate(chunks) if any(kw in chunk for kw in self.articleKeywords)]
        law_indices = [i for i, chunk in enumerate(chunks) if any(kw in chunk for kw in self.lawKeywords)]
        return [self.find_all_in_one(chunks[i], text) if i in law_indices 
                else self.find_it(chunks[i], self.articleKeywords, text) for i in article_indices]

    def find_all_in_one(self, chunk, text):
        words = chunk.split()
        start = next(i for i, w in enumerate(words) if any(kw in w for kw in self.articleKeywords))
        end = next(i for i, w in enumerate(words) if any(kw in w for kw in self.lawKeywords))
        article = ' '.join(words[start:end])
        return [article, *self.find_in_text(text, article)]

    def find_it(self, chunk, keyChunk, text):
        words = chunk.split()
        start = next(i for i, w in enumerate(words) if any(kw in w for kw in keyChunk))
        article = ' '.join(words[start:])
        return [article, *self.find_in_text(text, article)]

    def normalize_text(self, text):
        return Normalizer().normalize(text)

    def find_in_text(self, main_string, substring):
        normalized_substring = self.normalize_text(substring)
        start_index = main_string.find(normalized_substring)
        return (start_index, start_index + len(normalized_substring) - 1) if start_index != -1 else (-1, -1)

# text = "عطف به نامه شماره ۹۱۹۲/۳۰۱۸۶ مورخ ۲۰/۲/۱۳۸۴ در اجرای اصل یکصد و بیست و سوم (۱۲۳) قانون اساسی جمهوری اسلامی ایران قانون مدیریت خدمات کشوری مصوب ۸/۷/۱۳۸۶ کمیسیون مشترک رسیدگی به لایحه مدیریت خدمات کشوری مجلس شورای اسلامی مطابق اصل هشتاد و پنجم (۸۵) قانون اساسی جمهوری اسلامی ایران که به مجلس شورای اسلامی تقدیم گردیده بود، پس از موافقت مجلس با اجرای آزمایشی آن به مدت پنج سال در جلسه علنی مورخ ۱۸/۱۱/۱۳۸۵ و تأیید شورای محترم نگهبان، به پیوست ارسال می گردد."
# extractor = ArticleExtractor(text)
# print(extractor.result)
