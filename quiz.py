#from main import score
import func
import subprocess
import random
import os

def question():
    DEVNULL = os.open(os.devnull, os.O_WRONLY) 
    path1 = os.path.abspath('../../cods')

    code = random.randint(1,len(os.listdir(path1)))
    #type_quiz = random.randint(1,4)
    type_quiz = 4

    file = open(path1+"/"+str(2)+".txt",'r')
    quest = file.read()

    if type_quiz == 1: #логический
        quest = func.type_code_logic(quest)
    elif type_quiz == 2: #синтаксический
        quest = func.type_code_syntax(quest)
    elif type_quiz == 3: #выходной ответ
        quest2 = func.type_code_output(quest)
    else:
        quest = func.read_code(quest)

    if type_quiz == 3:
        func.write_code_output(quest2[1])
        os_out = func.write_code(quest2[0])
    else:
        func.write_code_output(quest)
        os_out = func.write_code(quest)
    file.close()

    with open(func.number_lines(os.path.abspath('quest.txt')), "r") as f:
        text = f.read()
        #print(text)

    check = subprocess.call(os_out, shell=True, stdout=DEVNULL, stderr=subprocess.STDOUT)
    if check == 0:
        if type_quiz == 3:
            ans2 = func.check_os()
            quiz = "При каком значении программа выдаст результат: "+ans2
            ans = quest2[2]
        else:
            quiz = "Введите ответ программы:"
            ans = func.check_os()
    elif check == 1:
        quiz = "Введите строчку кода, где допущена ошибка:"
        ans = func.check_false(os_out)

    func.delete_file()

    return [text,ans,quiz]