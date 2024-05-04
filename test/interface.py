# import re
# import json
# import os
# from tqdm import tqdm



# def find_status_refrence(testCase):
#     return re.finditer(r"ماده\s*(\d{1,3})(\s*\(\d+\))?" , testCase[0]['input'])

# testCase = []


# with open("./test/test_case.json" , 'r' , encoding='utf-8' ) as jsonFile:
#     cases = json.load(jsonFile)
# testCase.append(cases)


# for i, m in enumerate(find_status_refrence(testCase)):
#     if testCase[i]['output']['Statute reference'] == m[0]:
#         print(True)
#     else:
#         print(testCase[i]['output']['Statute reference'] + "       " + m[0])


import json
from main import result
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def check(testCase):
  result = result(testCase['input'])
  if (result['Statute reference'] == testCase['output']['Statute reference'] and 
      result['Date'] == testCase['output']['Date'] and 
      result['Defined terms'] == testCase['output']['Defined terms'] and
      result['Punishment'] == testCase['output']['Punishment']):
    return True
  else:
    return False


def blueScore(testCase):
    candidate = result(testCase['input'])
    reference = testCase['output']
    listOfInput = ['Statute reference' , 'Date' , 'Defined terms' , 'Punishment' ]
    results=[]


    for case in listOfInput:
        candidate[case] = candidate[case].split()
        reference[case] = reference[case].split()
        smoothie = SmoothingFunction().method1
        score = sentence_bleu(reference[case], candidate[case], smoothing_function=smoothie)
        results.append(score)
    return results




testCase = []


with open("./test_case.json" , 'r' , encoding='utf-8' ) as jsonFile:
    cases = json.load(jsonFile)
testCase.append(cases)


for i, test in testCase:
  if(check(test)):
    print("test " + str(i+1) + "success")

for i, test in testCase:
  blue = blueScore(test)
  print("Average BluScore for test " + str(i+1) +" : "+ (sum(blue)/len(blue)) )