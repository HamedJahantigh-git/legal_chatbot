from hazm import * 
import re


class OrgExtractor:

    def __init__(self,
        normalizer = Normalizer(),
        tagger = POSTagger(model='resource/hazm_model/pos_tagger.model'),
        chunker = Chunker(model='resource/hazm_model/chunker.model')) -> None:

        self.ROLES = ['NP', 'PP', 'VP', 'ADJP', 'ADVP']
        self.normalizer = normalizer
        self.tagger = tagger
        self.content = open('resource/org/orgs.txt', 'r+').readlines() 
        self.chunker = chunker

    def ngrams(self, text, n):
        words = text.split()
        ngrams = zip(*[words[i:] for i in range(n)])
        return [' '.join(ngram) for ngram in ngrams]

    def chunk_text(self, text):
        
        tagged = self.tagger.tag(word_tokenize(text))
        chunks = tree2brackets(self.chunker.parse(tagged))

        chunked = [[c.strip(), c.split()[-1]] for c in\
                    [re.sub(r'\.|،|]*|,|;|/|[۰-۹]+|\)|\(|-|«|»', '', chunk).strip() for chunk in chunks.split('[')] if len(c.split()) >= 2]

        for c in chunked:
            c[0] = c[0].replace('\u200c', ' ')

        roles_set = set(self.ROLES)

        for chunk in chunked:
            words = chunk[0].split()
            filtered_words = [word for word in words if word not in roles_set]

            chunk[0] = ' '.join(filtered_words)

            if chunk[1] not in roles_set:
                for word in words:
                    if word in roles_set:
                        chunk[1] = word 
                        break  

        return chunked

    def merge_np_chunks(self, chunked):
        nps, temp, id = [], '', 0

        while id < len(chunked):
            chunk = chunked[id]
            if chunk[1]=='NP':
                temp = chunk[0]
                while id<len(chunked)-1 and chunked[id+1][1]=='NP':
                    temp = temp + ' ' + chunked[id+1][0]
                    id = id + 1
                    
                else:
                    nps.append(temp)
                    temp = ''
            id= id+1

        return nps

    def make_ngrams(self, nps):
        ngs = []
        for np in nps:
            npg = []
            count = len(np.split())
            for i in range(count, 0, -1):
                npg.extend(self.ngrams(np, i))
            ngs.append(npg)

        return ngs

    def normalize_text(self, text):
        return re.sub(r'\W+', '', text)

    def find_token_sequence(self, text, phrase):
        """Find the substring in the text that matches the normalized version of the phrase without taking tokens as input."""
        # Tokenize the text and normalize the tokens
        tokens = word_tokenize(text)
        normalized_tokens = [(self.normalize_text(token), index) for index, token in enumerate(tokens) if self.normalize_text(token)]
        
        # Normalize the phrase
        normalized_phrase = self.normalize_text(phrase)
        
        # Concatenate the normalized tokens into one string for comparison
        concatenated_tokens = ''.join(token for token, _ in normalized_tokens)
        
        # Find the normalized phrase within the concatenated normalized tokens
        start_pos = concatenated_tokens.find(normalized_phrase)
        if start_pos == -1:
            return None  # No match found
        
        # Determine the bounds of the matching sequence
        end_pos = start_pos + len(normalized_phrase)
        current_pos = 0
        start_token_index = None
        end_token_index = None
        
        for token, original_index in normalized_tokens:
            prev_pos = current_pos
            current_pos += len(token)
            if current_pos > start_pos and start_token_index is None:
                start_token_index = original_index
            if current_pos >= end_pos:
                end_token_index = original_index
                break

        # Extract the exact substring from the original text
        if start_token_index is not None and end_token_index is not None:
            # Construct the substring based on token indices
            start_char_pos = text.find(tokens[start_token_index])
            if end_token_index + 1 < len(tokens):
                end_char_pos = text.find(tokens[end_token_index + 1])
            else:
                end_char_pos = len(text)
            return text[start_char_pos:end_char_pos]

        return None

    def extract(self, text, bias):

        txt = text
        text = self.normalizer.normalize(text=text)
        chunked = self.chunk_text(text)
        nps = self.merge_np_chunks(chunked=chunked)
        ngs = self.make_ngrams(nps=nps)
        
        output = []
        for row in ngs:
            t = []
            for ng in row: 
                if len(ng) < 4:
                    continue
                for org in self.content:
                    otp = re.match(f'^{ng}.*', org)

                    if isinstance(otp, re.Match):
                        t.append((ng))
            
            output.append(t)

        result = []
        for ng, otp in zip(ngs, output):
            for o in otp:
                seq = self.find_token_sequence(txt, o)
                if o in ng and o not in result and seq:
                    result.append(seq)
        
        result = sorted(result, key=len, reverse=True)
        defined_terms = []
        for term in result:
            if not any(term in other[0] for other in defined_terms):
                for m in re.finditer(term, txt):
                    defined_terms.append((term, m.start()+bias, m.end()+bias))
        return defined_terms

# text = "عطف به نامه شماره ۱۳۹۵۷۴ مورخ ۲۶/۱۰/۱۳۹۴ در اجرای اصل یکصد و بیست و سوم(۱۲۳) قانون اساسی جمهوری‌ اسلامی‌ ایران قانون برنامه پنجساله ششم توسعه اقتصادی، اجتماعی و فرهنگی جمهوری اسلامی ایران (۱۴۰۰- ۱۳۹۶) مصوب جلسه علنی روز شنبه مورخ ۱۴/۱۲/۱۳۹۵ مجلس که با عنوان «لایحه احکام مورد نیاز اجرای بـرنـامـه شـشـم تـوسـعـه اقتصادی، اجتماعی و فرهنگی جمهوری اسلامی ایران (۱۳۹۹-۱۳۹۵)» به مجلس شورای اسلامی تقدیم و مطابق اصل یکصد و دوازدهم (۱۱۲) قانون اساسی جمهوری‌اسلامی ایران از سوی مجمع تشخیص مصلحت نظام موافق با مصلحت نظام تشخیص داده شده است، به پیوست ابلاغ می‌گردد."  
# ext = OrgExtractor()
# print(ext.extract(text, 10))
