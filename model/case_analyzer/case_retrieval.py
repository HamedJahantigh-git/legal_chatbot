from rank_bm25 import BM25Okapi
from nltk.translate.bleu_score import corpus_bleu
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np
from tqdm import tqdm

from hazm import word_tokenize
from operator import itemgetter
import warnings

class BM25Retrival():
    def __init__(self, data: list, stop_words = [], tokenizer = word_tokenize):
        self._data = data
        self._stopwords = stop_words
        self._tokenizer = tokenizer
        self._text_tok = []
        self._is_process = False 
    
    def preprocess(self):
        self._text_tok = [
            self.remove_stopwords(self._tokenizer(text)) 
            for text in self._data
            ]
        self._model = BM25Okapi(self._text_tok)
        self._is_process = True
        
    def remove_stopwords(self, text_tok: str):
        return [tok for tok in text_tok if tok not in self._stopwords] 
        

    def get_similar_score(self, query: str) -> list:
        if not self._is_process:
            self.preprocess()
        score = self._model.get_scores(self._tokenizer(query)).tolist()
        score_dic = [{"corpus_id": i, "score": v} for i, v in enumerate(score)]
        sorted_score = sorted(score_dic, key=lambda x: x["score"], reverse=True)
        return sorted_score
    
    def get_similar_text(self, query: str, num: int) -> list:
        result = []
        if not self._is_process:
            self.preprocess()
        sorted_score = self.get_similar_score(query)[:num+1]
        top_score = sorted_score[0]["score"]
        for i in range(1,num+1):
            text_id = sorted_score[i]["corpus_id"]
            score = sorted_score[i]["score"]
            result.append((self._data[text_id],f"{100*score/top_score:.2f}" ))
        return result
    
    def create_similarity_matrix(self, save_path: str) -> None:
        if not self._is_process:
            self.preprocess()
        size = len(self._data)
        result_matrix = np.ones((size, size))
        for i in tqdm(range(size)):
            result_matrix[i,:] = self._model.get_scores(self._text_tok[i])
        np.save(save_path, result_matrix)
    
    
class BleuRetrieval():
    def __init__(self, data: list, stop_words =[], tokenizer = word_tokenize):
        self._data = data
        self._tokenizer = tokenizer
        self._stopwords = stop_words
        self._score_matrix= np.zeros((len(data),len(data)))
        self._text_tok = []
        self._is_process = False 
    
    def create_similarity_matrix(self, save_path = str) -> None:
        warnings.filterwarnings("ignore")
        for i in tqdm(range(len(self._data))):
            for j in range(len(self._data)):
                candidate = self._tokenizer(self._data[i])
                reference = [self._tokenizer(self._data[j])]
                self._score_matrix[i,j] = corpus_bleu([reference],[candidate],weights=[1,1,0,0])
        np.save(save_path,  self._score_matrix)
    
class WordEmbedingRetrieval():
    
    def __init__(self, data:list, **word2vec_parameter) -> None:
        self._documents = data
        self._tokenized_docs = [word_tokenize(doc) for doc in data]
        self._model = Word2Vec(self._tokenized_docs, word2vec_parameter)
        self._doc_embeddings = None

    # Function to get document embeddings
    def get_doc_embedding(self, doc, model):
        word_embeddings = [model.wv[word] for word in doc if word in model.wv]
        if len(word_embeddings) > 0:
            return np.mean(word_embeddings, axis=0)
        else:
            return np.zeros(model.vector_size)  # Return zero vector if no words found in vocab

    def _set_all_doc_embeding(self):
        # Get embeddings for all documents
        self._doc_embeddings = [self.get_doc_embedding(word_tokenize(doc), self._model) for doc in self._documents]

    # Function to calculate cosine similarity between two vectors
    def calculate_cosine_similarity(self, vector1, vector2):
        return cosine_similarity([vector1], [vector2])[0][0]

    def get_similarty(self, query:str):
        self._doc_embeddings()
        similarities = [self.calculate_cosine_similarity(
            self.get_doc_embedding(word_tokenize(query), self._model),
            doc_emb) for doc_emb in self._doc_embeddings]
        most_similar_index = np.argmax(similarities) 
        indices = list(sorted(enumerate(similarities), key = itemgetter(1)))[-5:]
        return indices, most_similar_index