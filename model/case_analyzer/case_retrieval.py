from rank_bm25 import BM25Okapi


class BM25Retrival():
    def __init__(self, data: list, stop_words: list, tokenizer):
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
        [tok for tok in text_tok if tok not in self._stopwords] 
        return

    def get_similar(self, query: str) -> list:
        if not self._is_process:
            self.preprocess()
        score = self._model.get_scores(self._tokenizer(query)).tolist()
        score_dic = [{"corpus_id": i, "score": v} for i, v in enumerate(score)]
        sorted_score = sorted(score_dic, key=lambda x: x["score"], reverse=True)
        return sorted_score