from hazm import *
import sacrebleu

class law_extractor(object):

    listOfLaw = []

    with open('resource/law/law_clean_list.txt', 'r', encoding='utf-8') as file:
        laws = file.readlines()

    for law in laws:
        listOfLaw.append(law)

    keywords = [
        'قانون' , 'قوانین' , 'آیین نامه'  , 'آیین‌نامه' , 'اساس نامه' , 'اساس‌نامه'
    ]

    def senTokenizer(self, text):

        tagger = POSTagger(model='resource/pos_tagger.model')
        chunker = Chunker(model='resource/chunker.model')

        chunks = []

        sentences = sent_tokenize(text)

        for sentence in sentences:

            words = word_tokenize(sentence)
            tagged_words = tagger.tag(words)

            tree = chunker.parse(tagged_words)

            for subtree in tree.subtrees():
                if subtree.label() in ['NP', 'ADVP']:
                    chunk_text = tree2brackets(subtree)

                    chunks.append(chunk_text)

        return chunks

    def find_law(self, tokens):
        dates = []
        i = 0
        while i < len(tokens):
            chunk = tokens[i]

            if any(key in chunk for key in self.keywords):
                dates.append(chunk)

            i += 1  
        return dates

    def check_law(self, law):
        splitedLaw = law.split()
        if splitedLaw[-1] in self.keywords:
            return False
        else:
            return True

    def selected_law(self, law):
        splitedLaw = law.split()
        for splited in splitedLaw:
            if splited in self.keywords:
                index = splitedLaw.index(splited)
        
        return ' '.join(splitedLaw[index:])

    def bleu_score(self, candidate, references):

        scores = []
        
        for ref in references:
            bleu = sacrebleu.corpus_bleu([candidate], [[ref]])
            scores.append(bleu.score)
        

        max_index = scores.index(max(scores))
        return max_index, scores[max_index] , scores

    def find_in_text(self, text , law):

        for key in self.keywords:
            if key in law:
                findKey = key
                break
        
        start_index = text.find(findKey)
        if start_index == -1:
            return -1, -1 
        
        end_index = start_index + len(law) - 1

        return start_index, end_index

    def __init__(self, text):
        returnList = []
        tokenized_sentences = self.senTokenizer(text)
        laws = self.find_law(tokenized_sentences)

        for law in laws:
            if self.check_law(law):
                law = self.selected_law(law)
                myList = []
                start , end = self.find_in_text(text , law)
                myList.append((law, start, end))
                returnList.append(myList)
                # ind, score , scores = self.bleu_score(law , self.listOfLaw)
                # l = self.listOfLaw[ind]
                # print(l)
                # print(ind , score)
        self.result = returnList

# text = "این یک قانون جدید است که به تصویب رسیده است. این قوانین باید رعایت شوند."
# extractor = law_extractor(text)
# print(extractor.result)
