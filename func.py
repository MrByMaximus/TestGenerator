import sys
import random
import subprocess
import ctypes
import os
import re
import fileinput

cmd_codepage = os.device_encoding(1) or ctypes.windll.kernel32.GetOEMCP()
os.chdir("mingw/bin")
path1 = os.path.abspath('quest.cpp')
path2 = os.path.abspath('quest.txt')

def count_num(quest):
    text = quest.split()
    count_number = 0
    count_action = 0

    for word in text:
        if word.find("{number_"+str(count_number)+"}") != -1:
            count_number+=1
        if word.find("{action_"+str(count_action)+"}") != -1:
            count_action += 1

    return [count_number, count_action]

def noise(quest):
    count_noise = 0
    text = quest.split()
    noise = []

    for word in text:
        if word.find("{^"+str(count_noise)+"^}") != -1:
            noise.append("{^"+str(count_noise)+"^}")
            count_noise+=1

    if count_noise != 0:
        noise.append("{^-^}")
        num = random.randint(0,count_noise-1)
        noise_num1 = quest.find(noise[num])
        first = quest.find(noise[0])
        end = quest.find(noise[count_noise])
        noise_num2 = quest.find(noise[num+1])
        quest2 = quest[noise_num1+5:noise_num2]
        quest = quest[:first] + quest[end:]
        quest = quest.replace("{^-^}", quest2)

    return quest

def type_code_output(quest):
    quest2 = quest
    sign = ['+','-','/','*']
    count = count_num(quest)
    choice = random.randint(1,2)
    out = ''

    quest = noise(quest)
    quest2 = noise(quest)

    if choice == 1:
        if count[0] != 0:
            j = 0
            if count[0] == 3:
                first = 1
            else:
                first = 0
            number = []
            num = random.randint(first,count[0])
            for i in range(first,count[0]):
                number.append(str(random.randint(1,99)))
                quest = re.sub("{number_"+str(i)+"}", number[j], quest)
                if i != num:
                    quest2 = re.sub("{number_"+str(i)+"}", number[j], quest2)
                else:
                    out = number[num]
                j += 1
        if count[1] != 0:
            action = []
            for i in range(count[1]):
                action.append(str(random.choice(sign)))
                quest = re.sub("{action_"+str(i)+"}", action[i], quest)
                quest2 = re.sub("{action_"+str(i)+"}", action[i], quest2)
    else:
        if count[1] != 0:
            num = random.randint(0,count[1])
            quest = re.sub("{action_"+str(num)+"}", str(random.choice(sign)), quest)
        if count[0] != 0:
            number = []
            for i in range(count[0]):
                number.append(str(random.randint(1,99)))
                quest = re.sub("{number_"+str(i)+"}", number[i], quest)
                quest2 = re.sub("{number_"+str(i)+"}", number[i], quest2)

    return [quest,quest2,out]

def type_code_error(quest,error):
    text = quest.split()
    error_choice = random.choice(error)
    count_error = 0

    for word in text:
        if word.find(error_choice) != -1:
            count_error += 1

    if count_error != 0:
        index = 0
        quest2 = quest
        num_error = random.randint(1,count_error)
        for i in range(1,count_error):
            index2 = quest2.find(error_choice)+len(error_choice)
            index += index2
            quest2 = quest2[index2:]
            if i == num_error:
                quest = quest[:index-len(error_choice)] + quest[index:]
                break

    return quest

def type_code_logic(quest):
    quest = read_code(quest)
    error = ['int','return 0;','std::','==']
    error_replace = ['','','','=']
    return type_code_error(quest,error)

def type_code_syntax(quest):
    quest = read_code(quest)
    #chance = random.randint(1,3)
    chance = 2
    error = [';','<<','{','}','"','(',')']
    error_replace = ['','','','=']
    text = quest.split()

    if chance == 1:
        index1 = quest.find("func(a")
        if index1 != -1:
            index = []
            index.append(quest.find("(",index1)-1)
            index2 = quest.find(")",index1)
            i = index1+4
            while i != index2:
                index1 = quest.find(",",index1+2,index2)
                if index1 != -1:
                    index.append(index1)
                i += 2
            index.append(index[len(index)-1])
            num = random.randint(1,len(index)-1)
            quest = quest[:index[num]] + quest[index[len(index)-1]:] #в конце добавить скобку
    elif chance == 2:
        type_choice = ['bool','string','char']
        quest = re.sub("int result", random.choice(type_choice)+" result", quest)

    return quest

def read_code(quest):
    sign = ['+','-','/','*']
    count = count_num(quest)

    quest = noise(quest)

    if count[0] != 0:
        for i in range(count[0]):
            quest = re.sub("{number_"+str(i)+"}", str(random.randint(1,99)), quest)
    
    if count[1] != 0:
        for i in range(count[1]):
            quest = re.sub("{action_"+str(i)+"}", str(random.choice(sign)), quest) 

    return quest

def write_code_output(quest):
    file = open(path2,'w')
    file.write(quest)
    file.close()

def write_code(quest):
    file = open(path1,'w')
    file.write(quest)
    file.close()
    return "g++ -o quest.exe quest.cpp"

def delete_file():
    os.remove(os.path.join(path1))
    os.remove(os.path.join(path2))

def check_os():
    if sys.platform == "linux" or sys.platform == "linux2":
        ans = check_true("./quest") #Проверить в linux
    else:
        ans = check_true("quest.exe")
    return ans

def check_true(os_out):
    ans = subprocess.check_output(os_out, shell=True, encoding=cmd_codepage, stderr=subprocess.STDOUT)
    os.remove(os.path.join(os_out))
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