from tkinter import *
import tkinter as tk
import sys, os
import random
import numpy
import subprocess
import ctypes
import re
import ast
import fileinput
from functools import partial
from tkinter import messagebox as mb
import webbrowser, sys, os
from sympy.core.basic import Basic
from sympy import *
from contextlib import redirect_stdout
from jinja2 import Template

path = os.getcwd()
path1 = path+'/quest.cpp'
path2 = path+'/quest.txt'
path3 = path+'/quest_xml.txt'
generator = open(path+'/generator.conf','r')
generator = ast.literal_eval(generator.read())
cmd_codepage = os.device_encoding(1) or ctypes.windll.kernel32.GetOEMCP()

class Generation():
    def __init__(self):
        super().__init__()

    def question_gen(self):
        DEVNULL = os.open(os.devnull, os.O_WRONLY)
        path4 = path+'/cods'
        #code = random.randint(1,len(os.listdir(path3)))
        #type_quiz = random.randint(1,4)
        type_quiz = 4
        code = 2
        out_error = [] #заглушка
        type_error = 0

        code_error_for_type_quiz = [1]
        if type_quiz == 3 and code in code_error_for_type_quiz:
            type_quiz = 4

        file = open(path4+"/"+str(code)+".txt",'r')
        quest = file.read()

        if type_quiz == 1 or type_quiz == 2:
            quest = self.read_code(quest)
            self.write_code(quest)

        if type_quiz == 1: #логический     
            quest2 = self.type_code_logic(quest)
        elif type_quiz == 2: #синтаксический       
            quest2 = self.type_code_syntax(quest) #0-quest,1-quest_output,2-answer,answer,3-answer_error
        elif type_quiz == 3: #выходной ответ
            quest2 = self.type_code_output(quest) #0-quest,1-quest_output,2-answer,3-additional_out
            
        if type_quiz == 4: #входной ответ
            quest = self.read_code(quest)
            self.write_code_output(quest)
            os_out = self.write_code(quest)
        else:
            self.write_code_output(quest2[1])
            os_out = self.write_code(quest2[0])
        
        file.close()
        with open(self.number_lines(path2), "r") as f:
            text = f.read()

        #check = subprocess.call(os_out, shell=True, stdout=DEVNULL, stderr=subprocess.STDOUT)
        if type_quiz == 3:
            ans2 = self.check_true(self.check_os(os_out))
            quiz = "При каком значении "+quest2[3]+" программа выдаст результат: "+ans2
            ans = quest2[2]
        elif type_quiz == 4:
            quiz = "Введите ответ программы:"
            ans = self.check_true(self.check_os(os_out))
        else:
            quiz = "Введите строчку кода, где допущена ошибка:"
            if quest2[3]:
                out_error = list(quest2[3])
                type_error = 1 #определиться посылать ли единчные варианты или просто тип вопроса - разницы по сути нет
            if quest2[2] != '':
                ans = quest2[2]
            else:
                ans = self.check_false(os_out)

        return [text,str(ans),quiz,type_error,out_error]

    def count_num(self, quest):
        text = quest.split()
        count_number = 0
        count_action = 0

        for word in text:
            if word.find("{number_"+str(count_number)+"}") != -1:
                count_number+=1
            if word.find("{action_"+str(count_action)+"}") != -1:
                count_action += 1

        return [count_number, count_action]

    def noise(self, quest):
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

    def type_code_output(self, quest):
        quest2 = quest
        count = self.count_num(quest)
        choice = random.randint(1,2)
        check_division = 0
        out = ''
        generated_number = list(generator['generated_number'])

        quest = self.noise(quest)
        quest2 = self.noise(quest)

        if choice == 1:
            if count[0] != 0:
                j = 0
                number = []
                num = random.randint(0,count[0]-1)
                for i in range(count[0]):
                    number.append(str(random.randint(generated_number[0],generated_number[1])))
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
                    number.append(str(random.randint(generated_number[0],generated_number[1])))
                    quest = re.sub("{number_"+str(i)+"}", number[i], quest)
                    quest2 = re.sub("{number_"+str(i)+"}", number[i], quest2)
            out2 = "{action}"

        if check_division == 1:
            quest = re.sub("int","double",quest)
            quest = re.sub("double main","int main",quest)
            quest2 = re.sub("int","double",quest2)
            quest2 = re.sub("double main","int main",quest2)

        return [quest,quest2,out,out2] #Сделать проверку на единественный верный овтет, если при вычислениях будут 1 и больше вариантов

    def type_code_error(self, quest,error):
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

    def type_code_logic(self, quest):
        quest2 = quest
        chance = random.randint(2)
        #chance = 1
        #error_replace = ['','','','=']
        out = ''

        
        quest = type_code_error(quest,generator['error_logic'])

        return [quest,quest2,out]
 #необъявленный идентификатор
 #числа в идентификатор нельзя ставить
 #изменение константы
 #сопастовление пунктов списка
    def type_code_syntax(self, quest):
        quest2 = quest #добавить ошибку из конфигуратора
        #choice = random.randint(1,4)
        choice = 1
        #error_replace = ['','','','=']
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
            quest = type_code_error(quest, generator['error_syntax'])

        return [quest,quest2,out,out_error]

    def read_code(self, quest):
        import re
        count = self.count_num(quest)
        quest = self.noise(quest)
        check_division = 0
        generated_number = list(generator['generated_number'])

        if count[0] != 0:
            for i in range(count[0]):
                quest = re.sub("{number_"+str(i)+"}", str(random.randint(generated_number[0],generated_number[1])), quest)
        
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

    def write_code_output(self, quest):
        file1 = open(path2,'w')
        file1.write(quest)
        file1.close()
        file2 = open(path3,'w')
        file2.write(quest)
        file2.close()

    def write_code(self, quest):
        file = open(path1,'w')
        file.write(quest)
        file.close()
        return "g++ " + path + "\quest.cpp -o " + path + "\quest"

    def delete_file(self):
        os.remove(os.path.join(path1))
        os.remove(os.path.join(path2))
        os.remove(os.path.join(path3))
        if os.path.exists(path+"/quest.exe"):
            os.remove(os.path.join("quest.exe")) #Надо еще для linux
        if os.path.exists(path+"/quest"):
            os.remove(os.path.join("quest")) #Надо еще для linux

    def check_os(self, os_out):
        if sys.platform == "linux" or sys.platform == "linux2":
            os_out += " && " + path + "./quest" #Проверить в linux
        else:
            os_out += " && " + path + "\quest"

        return os_out

    def check_true(self, os_out):
        ans = subprocess.check_output(os_out, shell=True, encoding=cmd_codepage, stderr=subprocess.STDOUT)
        index = ans.find(":")

        return ans[index+2:]

    def check_false(self, os_out):
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

    def number_lines(self, filename, start=1):
        with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
            for n, line in enumerate(file, start=start):
                print(n, '\t', line, end='')
        os.unlink(filename + '.bak')

        return filename

class Quiz:
    def __init__(self, filename, htmlFilename=""):
        self.filename = filename
        if not htmlFilename:
            htmlFilename = os.path.splitext(filename)[0]+".html"
        self.htmlFilename = str(htmlFilename)
        self.f = open(filename, 'w', encoding="utf-8")
        with redirect_stdout(self.f):
            print('<?xml version="1.0" ?> <quiz>')
        file = open(htmlFilename, 'w', encoding="utf-8")
        file.close()

    def addShortAnswerQuestion(self, name, question, answer):
        if isinstance(question, Basic):
            question = f"\({latex(question)}\)"

        with redirect_stdout(self.f):
            self.questionHeader("shortanswer", name, question)
            xml = Template('<usecase>0</usecase>\n<answer fraction="100" format="moodle_auto_format"><text> {{answer}} </text></answer>\n</question>\n')
            print(xml.render(answer=answer))

        self.addHtmlHeader()
        self.addHtmlQuestionBlock(name, question, 'shortanswer')
        self.addHtmlAnswerBlockShortAnswer(answer)

    def addMultipleChoiceQuestion(self, name, question, choiceList):
        if isinstance(question, Basic):
            question = f"\({latex(question)}\)"
        if len(choiceList) > generator['count_multichoice']:
            tmp = choiceList[1:]
            shuffle(tmp)
            choiceList = [choiceList[0]] + tmp[:generator['count_multichoice']-1]
        choiceList = [ f"\({latex(item)}\)" if isinstance(item, Basic) else item for item in choiceList]

        if len(choiceList) != generator['count_multichoice']:
            print("Ошибка: добавление вопроса с множественным выбором требует ровно" + generator['count_multichoice'] + " варианта ответов. Дано:\n", choiceList)
            sys.exit(-1)
        if len(set(choiceList)) != generator['count_multichoice']:
            print("Предупреждение: добавление вопроса с несколькими вариантами выбора с неуникальными опциями было проигнорировано:\n ", choiceList)
            return

        choiceList = [str(i) for i in choiceList]

        with redirect_stdout(self.f):
            self.questionHeader("multichoice", name, question)
            xml = Template(' <answer fraction="100" format="html"><text><![CDATA[ {{correct_answer}} ]]></text></answer>')
            print(xml.render(correct_answer=choiceList[0]))
            for item in choiceList[1:]:
                xml = Template(' <answer fraction="-33.33333" format="html"> <text><![CDATA[ {{incorrect_answer}} ]]></text></answer>')
                print(xml.render(incorrect_answer=item))
            print('<answernumbering>none</answernumbering>\n<shuffleanswers>1</shuffleanswers>\n<single>true</single>\n</question>\n')

        self.addHtmlHeader()
        self.addHtmlQuestionBlock(name, question, 'multichoice')
        self.addHtmlAnswerBlockMultichoice(choiceList)

    def questionHeader(self, type, name, question):
        with redirect_stdout(self.f):
            xml = Template('<question type=" {{type}} ">\n <name>\n  <text> {{name}} </text>\n </name>\n <questiontext format="html">\n  <text><![CDATA[\n {{question}} ]]> \n  </text>\n </questiontext>')
            print(xml.render(name=name,type=type,question=question))

    def addHtmlHeader(self):
        if os.path.getsize(self.htmlFilename):
            return
        html = """<!DOCTYPE html>
        <html>
        <head>
        <title>Тест по программированию на C++</title>
        <style>
        body
        {
        margin-top: 20px;
        margin-right: 20px;
        margin-bottom: 20px;
        margin-left: 20px;
        }
        h2
        {
        margin-left: 120px;
        }
        </style>
        </head>
        """
        f = self.edit_open()
        f.write(html)
        f.close()

    def addHtmlQuestionBlock(self, name, question, questionType):
        html = f'<body><h2> {name} </h2><div class="que {questionType} deferredfeedback "><div class="content"><div class="formulation clearfix"><div class="qtext">\n {question} </div>'
        f = self.edit_open()
        f.write(html)
        f.close()

    def addHtmlAnswerBlockMultichoice(self, choiceList):
        html = '<br /><div class="ablock"><div class="answer">'
        for item in choiceList:
            html += f'<div class="r0"><input type="radio" {"checked" if item==choiceList[0] else ""}/><label> {item} </label></div>'
        html += '</div></div></div></div></div></body></html>'
        f = self.edit_open()
        f.write(html)
        f.close()

    def addHtmlAnswerBlockShortAnswer(self, answer):
        html = f'<br /><div class="ablock"><span class="answer"><input type="text" size="80" class="form-control d-inline" /><p>Правильный ответ: {answer} </span></div></div></div></div></body></html>'
        f = self.edit_open()
        f.write(html)
        f.close()

    def preview(self):
        webbrowser.open_new_tab(self.htmlFilename)

    def edit_open(self):
        f = open(self.htmlFilename, 'a', encoding="utf-8")
        return f

    def close(self):
        with redirect_stdout(self.f):
            print('</quiz>')
        self.f.close()

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Генерация тестов по программированию")
        count_out = len(os.listdir(path+'/output'))
        if count_out == 0:
            self.num_test = 0
        else:
            self.num_test = int(count_out / 2)
        self.generator_test()

    def generator_test(self):
        self.geometry('400x100')
        self.resizable(width=False, height=False)

        self.frame1 = tk.Frame(self)
        self.frame1.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

        count_question = list(generator['count_question'])
        self.title = tk.Label(self.frame1, text='Укажите количество вопросов для генерации', font=40)
        self.title.pack(fill=BOTH)
        self.count_tests = Spinbox(self.frame1, from_=count_question[0], to=count_question[1], width=5) 
        self.count_tests.pack(pady=5)
        self.btn_gen = tk.Button(self.frame1, text='Сгенерировать тест', command=self.create_quest)
        self.btn_gen.pack()

        self.num_test += 1
        self.score = 0
        self.quest = []
        self.quest_title = []
        self.answer = []
        self.correct_answer = [[]]
        self.input_answer = []
        self.input_answer_error = [[]]
        self.answer_check = [[]]
        self.question = []
        self.question_title = []
        self.frame = []
        self.button_answer = []

    def delete_elements(self):
        self.quest.clear()
        self.quest_title.clear()
        self.question.clear()
        self.question_title.clear()
        self.answer.clear()
        self.correct_answer.clear()
        self.input_answer.clear()
        self.button_answer.clear()
        self.input_answer_error.clear()
        self.answer_check.clear()
        self.frame.clear()
        self.canvas.destroy()
        self.frame2.destroy()
        self.scrolly.destroy()

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def list_index(self):
        index = []
        list_index = list(range(1, generator['count_multichoice']+1))
        random.shuffle(list_index)
        for num in list_index:
            index.append(num)
        return index

    def add_correct_answer(self, i):
        if i != self.score_count-1:
            self.correct_answer.append([]) 

    def is_float(self, str):
        try:
            float(str)
            if str.find('.') != -1 and str.count('.') == 1:
                return True
            else:
                raise ValueError
        except ValueError:
            return False

    def edit_quest(self, filename, start=1):
        with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
            for n, line in enumerate(file, start=start):
                print(n, "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;", line, "<br />", end='') #отступы
        os.unlink(filename + '.bak')

        return filename

    def create_input(self, i, j):
        index = self.list_index()
        for k in range(generator['count_multichoice']):
            self.answer_check[i].append(IntVar())
            self.input_answer_error[i].append(tk.Checkbutton(self.frame[i], text=self.correct_answer[i][k], variable=self.answer_check[i][k], offvalue=0))
            self.input_answer_error[i][k].grid(row=j+1, column=index[k], padx=1, pady=1)
        self.answer_check.append([])
        self.input_answer_error.append([])
        self.input_answer.append(tk.Entry(self.frame[i], width=40, font=40))
        self.button_answer[i].bind('<Button-1>', partial(self.check_answer_box, i))
        self.button_answer[i].grid(row=j+1, column=generator['count_multichoice']+1, padx=1, pady=1)

    def create_quest(self):
        self.count_number = int(self.count_tests.get())
        self.score_count = int(self.count_tests.get())
        self.frame1.destroy()
        self.geometry('800x600')
        self.resizable(width=True, height=True)

        self.canvas = tk.Canvas(self)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.frame2 = tk.Frame(self.canvas)
        self.frame2.bind('<Configure>', self.on_configure)
        self.canvas.create_window(0, 0, window=self.frame2)

        self.scrolly = tk.Scrollbar(self, command=self.canvas.yview)
        self.scrolly.place(relx=1, rely=0, relheight=1, anchor='ne')
        self.canvas.configure(yscrollcommand=self.scrolly.set)

        self.Quiz = Quiz(path+'/output/quiz'+str(self.num_test)+'.xml')
        q = Generation()
        j = 0
        for i in range(self.count_number):
            quiz = q.question_gen()
            self.quest.append(quiz[0])
            self.quest_title.append(quiz[2])
            self.answer.append(quiz[1])
            choice = random.randint(1,2) #множественная выборка или ответ

            quest = self.quest_title[i]+"<br /><br />"
            with open(self.edit_quest(path3), "r") as f:
                quest += f.read()

            self.frame.append(tk.Frame(self.frame2, borderwidth=2, relief="groove"))
            self.frame[i].pack(fill=BOTH)

            self.question.append(tk.Label(self.frame[i], text=self.quest[i], font=10, justify=LEFT))
            self.question_title.append(tk.Label(self.frame[i], text=self.quest_title[i], font=40, justify=LEFT))
            self.button_answer.append(tk.Button(self.frame[i], text='Отправить'))
            self.question[i].grid(row=j, column=0, padx=1, pady=1)
            self.question_title[i].grid(row=j+1, column=0, padx=1, pady=1)

            if quiz[3] == 0 and choice == 1: #число ответ
                if self.is_float(self.answer[i]):
                    fractional_number_answer = list(generator['fractional_number_answer'])
                    self.answer[i] = round(float(self.answer[i]),generator['fractional_number'])
                    number = self.answer[i]
                    fractional_step_number = 1 / (10 ** generator['fractional_number'])
                    list_numbers = list(numpy.arange(number-fractional_number_answer[0], number+fractional_number_answer[1], fractional_step_number))
                    list_numbers = [round(v,generator['fractional_number']) for v in list_numbers]
                else:
                    number_answer = list(generator['number_answer'])
                    number = int(self.answer[i])
                    list_numbers = list(range(number-number_answer[0], number+number_answer[1]))
                random.shuffle(list_numbers)
                k = 0
                self.correct_answer[i].append(self.answer[i])
                for num in list_numbers:
                    if num != number:
                        self.correct_answer[i].append(str(num))
                        k += 1
                        if k == generator['count_multichoice']-1:
                            break
                self.add_correct_answer(i)
                self.create_input(i,j)
            elif self.answer[i] in generator['sign_for_action'] and quiz[3] == 0 and choice == 1: #знаковый ответ
                sign = generator['sign_for_action']
                random.shuffle(sign)
                k = 0
                self.correct_answer[i].append(self.answer[i])
                for num in sign:
                    if num != self.answer[i]:
                        self.correct_answer[i].append(str(num))
                        k += 1
                        if k == generator['count_multichoice']-1:
                            break
                self.add_correct_answer(i)
                self.create_input(i,j)
            elif quiz[4] and quiz[3] == 1 and choice == 1: #варианты овтетов для типа вопроса с ошибкой
                random.shuffle(quiz[4]) #list_error_answers
                self.correct_answer[i].append(self.answer[i])
                for num in quiz[4]:
                    self.correct_answer[i].append(str(num))
                self.add_correct_answer(i)
                self.create_input(i,j)
            elif choice == 2: #Вводный ответ
                if self.is_float(self.answer[i]):
                    self.answer[i] = round(float(self.answer[i]),generator['fractional_number'])
                self.input_answer_error.append([]) #заглушки
                self.answer_check.append([])
                self.add_correct_answer(i)
                self.input_answer.append(tk.Entry(self.frame[i], width=30, font=40))
                self.input_answer[i].grid(row=j+1, column=1, padx=1, pady=1)
                self.button_answer[i].bind('<Button-1>', partial(self.check_answer, i))
                self.button_answer[i].grid(row=j+1, column=2, padx=1, pady=1)
            print("Ответ: "+str(self.answer[i]))
            j += 2

            if choice == 1:
                self.Quiz.addMultipleChoiceQuestion("Вопрос №"+str(i+1), quest, self.correct_answer[i])
            elif choice == 2:
                self.Quiz.addShortAnswerQuestion("Вопрос №"+str(i+1), quest, str(self.answer[i]))
        q.delete_file()
        self.Quiz.close()

    def check_answer_box(self, i, event):
        self.button_answer[i].destroy()
        self.count_number -= 1
        k = 0
        if self.answer_check[i][0].get() == True: #может быть несколько правильных ответов - сделать
            self.score += 1
            for k in range(generator['count_multichoice']):
                self.input_answer_error[i][k].config(state="disabled",bg="lightgreen")
            self.frame[i].config(bg="lightgreen")
            self.question[i].config(bg="lightgreen")
            self.question_title[i].config(bg="lightgreen")
        else:
            for k in range(generator['count_multichoice']):
                self.input_answer_error[i][k].config(state="disabled",bg="tomato")
            self.frame[i].config(bg="tomato")
            self.question[i].config(bg="tomato")
            self.question_title[i].config(bg="tomato")

        self.result()

    def check_answer(self, i, event):
        self.button_answer[i].destroy()
        self.count_number -= 1

        if self.input_answer[i].get() == str(self.answer[i]):
            self.score += 1
            self.input_answer[i].config(state="readonly",bg="lightgreen")
            self.frame[i].config(bg="lightgreen")
            self.question[i].config(bg="lightgreen")
            self.question_title[i].config(bg="lightgreen")
        else:
            self.input_answer[i].config(state="readonly",bg="tomato")
            self.frame[i].config(bg="tomato")
            self.question[i].config(bg="tomato")
            self.question_title[i].config(bg="tomato")
        
        self.result()
        
    def result(self):
        if self.count_number == 0:
            if mb.showinfo("Результат", "Количество правильных ответов: {score} из {number}".format(score = self.score, number = self.score_count)):
                self.Quiz.preview()
                self.delete_elements()
                self.generator_test()

if __name__ == "__main__":
    app = Main()
    app.iconbitmap(path+'/icon.ico')
    app.mainloop()