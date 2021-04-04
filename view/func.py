import sys
import random
import subprocess
import ctypes
import os
import re
import ast
import fileinput

cmd_codepage = os.device_encoding(1) or ctypes.windll.kernel32.GetOEMCP()
os.chdir("mingw/bin")
path1 = os.path.abspath('quest.cpp')
path2 = os.path.abspath('quest.txt')
generator = open(os.path.abspath('../../generator.ini'),'r')
generator = ast.literal_eval(generator.read())

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
    count = count_num(quest)
    choice = random.randint(1,2)
    check_division = 0
    out = ''

    quest = noise(quest)
    quest2 = noise(quest)

    if choice == 1:
        if count[0] != 0:
            j = 0
            number = []
            num = random.randint(0,count[0]-1)
            for i in range(count[0]):
                number.append(str(random.randint(generator['from_number'],generator['to_number'])))
                quest = re.sub("{number_"+str(i)+"}", number[j], quest)
                if i != num:
                    quest2 = re.sub("{number_"+str(i)+"}", number[j], quest2)
                else:
                    quest2 = re.sub("{number_"+str(i)+"}", "{number}", quest2)
                    out = number[num]
                j += 1
        if count[1] != 0:
            action = []
            for i in range(count[1]):
                action.append(str(random.choice(generator['sign_for_action'])))
                quest = re.sub("{action_"+str(i)+"}", action[i], quest)
                quest2 = re.sub("{action_"+str(i)+"}", action[i], quest2)
                if action[i] == '/':
                    check_division = 1
        out2 = "{number}"
    else:
        if count[1] != 0:
            j = 0
            action = []
            num = random.randint(0,count[1]-1)
            for i in range(count[1]):
                action.append(str(random.choice(generator['sign_for_action'])))
                quest = re.sub("{action_"+str(i)+"}", action[j], quest)
                if action[i] == '/':
                    check_division = 1
                if i != num:
                    quest2 = re.sub("{action_"+str(i)+"}", action[j], quest2)
                else:
                    quest2 = re.sub("{action_"+str(i)+"}", "{action}", quest2)
                    out = action[num]
                j += 1
        if count[0] != 0:
            number = []
            for i in range(count[0]):
                number.append(str(random.randint(generator['from_number'],generator['to_number'])))
                quest = re.sub("{number_"+str(i)+"}", number[i], quest)
                quest2 = re.sub("{number_"+str(i)+"}", number[i], quest2)
        out2 = "{action}"

    if check_division == 1:
        quest = re.sub("int","double",quest)
        quest = re.sub("double main","int main",quest)
        quest2 = re.sub("int","double",quest2)
        quest2 = re.sub("double main","int main",quest2)

    return [quest,quest2,out,out2] #Сделать проверку на единественный верный овтет, если при вычислениях будут 1 и больше вариантов

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
        num_error = random.randint(0,count_error-1)
        for i in range(count_error):

            index2 = quest2.find(error_choice)+len(error_choice)
            index += index2
            quest2 = quest2[index2:]
            if i == num_error:
                quest = quest[:index-len(error_choice)] + quest[index:]
                break
 
    return quest

def type_code_logic(quest):
    quest2 = quest
    chance = random.randint(2)
    #chance = 1
    error = ['int','std::'] #,'=='
    error_replace = ['','','','=']
    out = ''

    
    quest = type_code_error(quest,error)

    return [quest,quest2,out]

def type_code_syntax(quest):
    quest2 = quest
    #choice = random.randint(1,4)
    choice = 1
    error = [';','<<','{','}','"','(',')']
    error_replace = ['','','','=']
    text = quest.split()
    out = ''
    out_error = []

    if quest.find("func(a") and choice == 1: #не работает
        index1 = quest.find("func(a")
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
    elif quest.find("return result;") != -1 and choice == 2:
        error_choice = ['char','bool','string']
        quest = re.sub("return result;", "", quest) #с делением идут неправильные результаты
        out_error.append("return result")
        out_error.append(random.choice(error_choice)+" result;")
        out_error.append("return")
        out = "return result;"
    elif quest.find("==") and choice == 3:
        with open(path1, 'r') as fp:
            for n, line in enumerate(fp, 1):
                if line.find("==") != -1:
                    quest2 = re.sub("==","=",quest2)
                    out = n - 1
    else:
        quest = type_code_error(quest, error)

    return [quest,quest2,out,out_error]

def read_code(quest):
    count = count_num(quest)
    quest = noise(quest)
    check_division = 0

    if count[0] != 0:
        for i in range(count[0]):
            quest = re.sub("{number_"+str(i)+"}", str(random.randint(generator['from_number'],generator['to_number'])), quest)
    
    if count[1] != 0:
        action = []
        for i in range(count[1]):
            action.append(str(random.choice(generator['sign_for_action'])))
            if action[i] == '/':
                check_division = 1
            quest = re.sub("{action_"+str(i)+"}", action[i], quest)

    if check_division == 1:
        quest = re.sub("int","double",quest)
        quest = re.sub("double main","int main",quest)

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
    os.remove(os.path.join("quest.exe")) #Надо еще для linux

def check_os(os_out):
    if sys.platform == "linux" or sys.platform == "linux2":
        os_out += " && ./quest" #Проверить в linux
    else:
        os_out += " && quest.exe"

    return os_out

def check_true(os_out):
    ans = subprocess.check_output(os_out, shell=True, encoding=cmd_codepage, stderr=subprocess.STDOUT)
    index = ans.find(":")

    return ans[index+2:]

def check_false(os_out):
    process = subprocess.Popen(os_out, shell=True, stdout=subprocess.PIPE, encoding=cmd_codepage, stderr=subprocess.STDOUT)
    tmp = process.stdout.read()
    print(tmp)
    tmp = tmp.replace("quest.cpp:","")
    tmp = tmp.replace(" In function 'int main()':\n","")
    tmp = tmp.replace(" In function 'int func(int, int)':\n","") #это не нормально
    #print(tmp)
    index = tmp.find(":")
    ans = ''
    for i in range(index):
        ans += ''.join(tmp[i])

    return ans

def number_lines(filename, start=1):
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
        for n, line in enumerate(file, start=start):
            print(n, '\t', line, end='')
    os.unlink(filename + '.bak')

    return filename