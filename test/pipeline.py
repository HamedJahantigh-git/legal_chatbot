import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.feature_extraction import org_extractor, law_extractor, time_extractor, article_extractor

def testpipe():

    f = open('test/zahra.json', 'r+', encoding='utf-8')
    res = open('test/result.txt', 'w+', encoding='utf-8')
    res.flush()
    testcases = json.load(f)

    passed, o, l, d, s = 0, 0, 0, 0, 0
    total = len(testcases)

    for i, testcase in enumerate(testcases):
        
        # artext = article_extractor.article_extractor(testcase['input'])
        # art = artext.result

        # datext = time_extractor.time_extractor(testcase['input'])
        # date = datext.result
        
        orgext = org_extractor.org_extractor(testcase['input'])
        org = orgext.find_org()

        # lawext = law_extractor.law_extractor(testcase['input'])
        # law = lawext.result

        res.write(f'======== TEST {i+1:02d} ========\n')
        res.write(f'input_text: {testcase["input"]}\n')

        # # statute reference / article
        # if art == testcase['output']['Statute reference']:
        #     res.write(f'PASSED ===> article: {art}')
        #     s += 1
        
        # else:
        #     res.write(f'FAILED ===> expected {testcase["output"]["Statute reference"]}, returned {art} \n')


        # # date / time
        # if date == testcase['output']['date']:
        #     res.write(f'PASSED ===> date: {date}')
        #     s += 1
        
        # else:
        #     res.write(f'FAILED ===> expected {testcase["output"]["date"]}, returned {date} \n')


        # defined terms / orgaization
        if sorted(org) == sorted(testcase['output']['Defined terms']):
            res.write(f'PASSED ===> org: {org}')
            o += 1
        
        else:
            res.write(f'FAILED ===> expected {testcase["output"]["Defined terms"]}, returned {org} \n')


        # # law
        # if law == testcase['output']['law']:
        #     res.write(f'PASSED ===> law: {law}')
        #     l += 1
        
        # else:
        #     res.write(f'FAILED ===> expected {testcase["output"]["law"]}, returned {law} \n')




        res.write('\n')

    res.write('\n================================\nSTATS:\n')
    res.write(f'TOTAL PASSED: {passed}/{total}\nSTATUTE REFERENCE: {s}/{total}\nDATE: {d}/{total}\nDEFINED TERMS: {o}/{total}\nLAW: {l}/{total}')

testpipe()