from hazm import * 
import re


class OrgExtractor:

    def __init__(self,
        normalizer = Normalizer,
        tagger = POSTagger(model='resource/hazm_model/pos_tagger.model'),
        chunker = Chunker(model='resource/hazm_model/chunker.model')) -> None:

        self.ROLES = ['NP', 'PP', 'VP', 'ADJP', 'ADVP']
        self.normalizer = normalizer()
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
                # seq = self.find_token_sequence(txt, o)
                if o in ng and o not in result:
                    result.append(o)
        
        result = sorted(result, key=len, reverse=True)
        defined_terms = []
        for term in result:
            if not any(term in other[0] for other in defined_terms):
                for m in re.finditer(term, txt):
                    defined_terms.append([term, m.start()+bias, m.end()+bias])
        return defined_terms

# text = "عطف به نامه شماره ۹۱۹۲/۳۰۱۸۶ مورخ ۲۰/۲/۱۳۸۴ در اجرای اصل یکصد و بیست و سوم (۱۲۳) قانون اساسی جمهوری اسلامی ایران قانون مدیریت خدمات کشوری مصوب ۸/۷/۱۳۸۶ کمیسیون مشترک رسیدگی به لایحه مدیریت خدمات کشوری مجلس شورای اسلامی مطابق اصل هشتاد و پنجم ۸۵ قانون اساسی جمهوری اسلامی ایران که به مجلس شورای اسلامی تقدیم گردیده بود، پس از موافقت مجلس با اجرای آزمایشی آن به مدت پنج سال در جلسه علنی مورخ ۱۸/۱۱/۱۳۸۵ و تأیید شورای نگهبان، به پیوست ارسال می گردد."
# ext = OrgExtractor()
# print(ext.extract(text, 0))
