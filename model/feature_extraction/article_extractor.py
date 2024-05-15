import re
from hazm import *
from model.feature_extraction.law_extractor import law_extractor

class article_extractor(object):

    keywords = {
    'ماده' , 'مواد'
    }

    def __init__(self , text):

        returnList = []
        tokenized_sentences = self.senTokenizer(text)

        for sentence in tokenized_sentences:
            chunking = self.sentence_chuncking(sentence)
            findArticles = self.find_article(chunking)
            extractor = law_extractor(text)
            returnList.append(findArticles)
            returnList.append(extractor.result)

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

    def find_article(self , chunks):
        listOfNumber = []
        i=0

        while i < len(chunks):

            if any(key in chunks[i] for key in self.keywords):
                listOfNumber = re.findall(r'\d+', chunks[i])
                while chunks[i].find("قانون") == -1:
                    i +=1
                    if i < len(chunks):
                        number = re.findall(r'\d+', chunks[i])
                        if not number:
                            break
                        else:
                            listOfNumber.append(number)
                    else:
                        break
            i +=1
        return listOfNumber


# text = "بر اساس ماده 1 و (10) قانون مجازات اسلامی"
# extractor = article_extractor(text)
# print(extractor.result)

