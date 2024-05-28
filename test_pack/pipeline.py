import os
import sys
import json
from hazm import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.feature_extraction import  org_extractor, time_extractor, article_extractor, law_extractor


def testpipe():

    f = open('test_pack/testcases.json', 'r+', encoding='utf-8')
    res = open('test_pack/result.txt', 'w+', encoding='utf-8')
    res.flush()
    testcases = json.load(f)

    passed, o, l, d, s = 0, 0, 0, 0, 0
    total = len(testcases)
    
    ae = article_extractor.ArticleExtractor()
    le = law_extractor.LawExtractor()
    oe = org_extractor.OrgExtractor()
    te = time_extractor.TimeExtractor()



    for i, testcase in enumerate(testcases):
        ot, lt, dt, st = False, False, False, False
        text = testcase['input']

        art = ae.extract(text, 0)
        law = le.extract(text, 0)
        org = oe.extract(text, 0)
        date = te.extract(text, 0)

        res.write(f'======== TEST {i+1:02d} ========\n')
        res.write(f'INPUT_TEXT: {text}\n')

        # statute reference / article
        res.write('\nARTICLE:\n')

        if art == testcase['output']['Statute reference']:
            res.write(f'PASSED ===> article: {art}\n')
            s += 1
            st = True
        
        else:
            res.write(f'FAILED ===> expected {testcase["output"]["Statute reference"]}, returned {art} \n')


        # date / time
        res.write('\nDATE:\n')
        if date == testcase['output']['Date']:
            res.write(f'PASSED ===> date: {date}\n')
            d += 1
            dt = True
        
        else:
            res.write(f'FAILED ===> expected {testcase["output"]["Date"]}, returned {date} \n')


        # defined terms / orgaization
        res.write('\nDEFINED TERMS:\n')
        if sorted(org) == sorted(testcase['output']['Defined terms']):
            res.write(f'PASSED ===> org: {org}\n')
            o += 1
            ot = True
        
        else:
            res.write(f'FAILED ===> expected {testcase["output"]["Defined terms"]}, returned {org} \n')


        # law
        res.write('\nLAW:\n')
        if law == testcase['output']['law']:
            res.write(f'PASSED ===> law: {law}')
            l += 1
            lt = True
        
        else:
            res.write(f'FAILED ===> expected {testcase["output"]["law"]}, returned {law} \n')
        
        if st and lt and ot and dt:
            passed += 1
        res.write('\n\n')


    res.write('\n================================\nSTATS:\n')
    res.write(f'TOTAL PASSED: {passed}/{total}\nSTATUTE REFERENCE: {s}/{total}\ndate: {d}/{total}\nDEFINED TERMS: {o}/{total}\nLAW: {l}/{total}')

testpipe()
