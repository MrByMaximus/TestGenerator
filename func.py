import random
import subprocess
import ctypes
import os
import re
import fileinput

cmd_codepage = os.device_encoding(1) or ctypes.windll.kernel32.GetOEMCP()
os.chdir("mingw/bin")
path1 = os.path.abspath('quest.cpp')
path2 = os.path.abspath('quest.ini')

def type_code_logic(quest):
    quest = read_code(quest)
    error = ['int','return 0;','std::']
    quest = quest.replace(random.choice(error), "", 1)
    return quest

def type_code_syntax(quest):
    quest = read_code(quest)
    error = [';','<<']
    quest = quest.replace(random.choice(error), "", 1)
    return quest

def read_code(quest):
    sign = ['+','-','/','*']
    text = quest.split()
    count = 0
    action = 0
    for word in text:
        if word.find("number") != -1:
            count+=1
        if word.find("action") != -1:
            action = 1

    for i in range(count):
        quest = re.sub("number_"+str(i), str(random.randint(1,100)), quest)
        if action == 1:
            quest = re.sub("action", str(random.choice(sign)), quest)
    return quest

def write_code(quest):
    file = open(path1,'w')
    file2 = open(path2,'w')
    file.write(quest)
    file2.write(quest)
    file.close()
    file2.close()
    os_out = "g++ {path} && a.exe"
    return os_out.format(path = path1)

def delete_file():
    os.remove(os.path.join(path1))
    os.remove(os.path.join(path2))

def check_true(os_out):
    ans = subprocess.check_output(os_out, shell=True, encoding=cmd_codepage, stderr=subprocess.STDOUT)
    os.remove(os.path.join(os.path.abspath('a.exe')))
    return ans

def check_false(os_out):
    process = subprocess.Popen(os_out, shell=True, stdout=subprocess.PIPE, encoding=cmd_codepage, stderr=subprocess.STDOUT)
    tmp = process.stdout.read()
    tmp = tmp.replace(path1+":","")
    tmp = tmp.replace(" In function 'int main()':\n","")
    tmp = tmp.replace(" In function 'int func(int, int)':\n","")
    #print(tmp)
    index = tmp.find(":")
    ans = ''
    for i in range(index):
        ans += ''.join(tmp[i])
    #print(ans)
    return ans

def number_lines(filename, start=1):
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
        for n, line in enumerate(file, start=start):
            print(n, line, end='')
    os.unlink(filename + '.bak')
    return filename

def addCompleteCodeQuestions(self, title, questionPattern, sourceCode, tokens, distractors = [], numQuestions=-1):
    pairs = []
    for token in tokens:
        code = sourceCode.replace(token, "__________")
        pairs.append((code, token))
    self.addMultipleChoiceQuestionsFromPairs(title, questionPattern, pairs, distractors, numQuestions)

def addMultipleChoiceQuestionsFromPairs(self, title, questionPattern, solutionPairs, moreDistractors=[], numQuestions=-1):

    L = len(solutionPairs)
    if numQuestions == -1: # auto
        numQuestions = L
    if numQuestions <= L: # prevent questions sharing question text
        pairs = sample(solutionPairs, numQuestions)
    else:
        pairs = [ sample(solutionPairs, 1)[0] for _ in range(numQuestions) ]

    for pair in pairs:
        question, answer = pair[0], pair[1]

        if isinstance(question, Basic): # sympy expr
            question = f"\({latex(question)}\)"

        q = questionPattern.replace("%s", question)

        bads = [ pair[1] for pair in solutionPairs] + moreDistractors
        bads = list(set(bads))
        while answer in bads:
            bads.remove(answer)

        shuffle(bads)
        self.addMultipleChoiceQuestion(title, q, [answer] + bads[0:3])