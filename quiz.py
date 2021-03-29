import func
import subprocess
import random
import os

def question():
    DEVNULL = os.open(os.devnull, os.O_WRONLY)
    path3 = os.path.abspath('../../cods')
    #code = random.randint(1,len(os.listdir(path3)))
    #type_quiz = random.randint(1,4)
    type_quiz = 4
    code = 2
    out_error = [] #заглушка
    type_error = 0

    code_error_for_type_quiz = [1]
    if type_quiz == 3 and code in code_error_for_type_quiz:
        type_quiz = 4

    file = open(path3+"/"+str(code)+".txt",'r')
    quest = file.read()

    if type_quiz == 1 or type_quiz == 2:
        quest = func.read_code(quest)
        func.write_code(quest)

    if type_quiz == 1: #логический     
        quest2 = func.type_code_logic(quest)
    elif type_quiz == 2: #синтаксический       
        quest2 = func.type_code_syntax(quest) #0-quest,1-quest_output,2-answer,answer,3-answer_error
    elif type_quiz == 3: #выходной ответ
        quest2 = func.type_code_output(quest) #0-quest,1-quest_output,2-answer,3-additional_out
        
    if type_quiz == 4: #входной ответ
        quest = func.read_code(quest)
        func.write_code_output(quest)
        os_out = func.write_code(quest)
    else:
        func.write_code_output(quest2[1])
        os_out = func.write_code(quest2[0])
    
    file.close()
    with open(func.number_lines(os.path.abspath('quest.txt')), "r") as f:
        text = f.read()

    #check = subprocess.call(os_out, shell=True, stdout=DEVNULL, stderr=subprocess.STDOUT)
    if type_quiz == 3:
        ans2 = func.check_true(func.check_os(os_out))
        quiz = "При каком значении "+quest2[3]+" программа выдаст результат: "+ans2
        ans = quest2[2]
    elif type_quiz == 4:
        quiz = "Введите ответ программы:"
        ans = func.check_true(func.check_os(os_out))
    else:
        quiz = "Введите строчку кода, где допущена ошибка:"
        if quest2[3]:
            out_error = list(quest2[3])
            type_error = 1 #определиться посылать ли единчные варианты или просто тип вопроса - разницы по сути нет
        if quest2[2] != '':
            ans = quest2[2]
        else:
            ans = func.check_false(os_out)

    return [text,str(ans),quiz,type_error,out_error]