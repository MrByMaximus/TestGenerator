import func
import subprocess
import random
import os

DEVNULL = os.open(os.devnull, os.O_WRONLY) 
path1 = os.path.abspath('../../cods')

count_code = len(os.listdir(path1))
code = random.randint(1,count_code)
type_quiz = random.randint(1,3)

file = open(path1+"/"+str(code)+".ini",'r')
quest = file.read()

if type_quiz == 1: #логический
    quest = func.type_code_logic(quest)
elif type_quiz == 2: #синтаксический
    quest = func.type_code_syntax(quest)
else: #без ошибок
    quest = func.read_code(quest)

os_out = func.write_code(quest)
file.close()

with open(func.number_lines(os.path.abspath('quest.ini')), "r") as f:
    text = f.read()
    print(text)

check = subprocess.call(os_out, shell=True, stdout=DEVNULL, stderr=subprocess.STDOUT)
if check == 0:
    print("Введите ответ программы:")
    ans = func.check_true(os_out)
elif check == 1:
    print("Введите строчку кода, где допущена ошибка:")
    ans = func.check_false(os_out)
else:
    print ("Ошибка!")

func.delete_file()

answer = input()
if answer == ans:
    print("Ответ правильный!")
else:
    print("Ответ неправильный!")