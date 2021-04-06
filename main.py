from tkinter import messagebox as mb
from tkinter import *
import tkinter as tk
import sys, os
import random
import numpy
import ctypes
import fileinput
from functools import partial
from quiz import Quiz
from generation import Generation
from generation import generator, path, path_xml

class Main(tk.Tk): #Оконное приложение
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

    def is_number(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    def edit_quest(self, filename, start=1):
        with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
            for n, line in enumerate(file, start=start):
                print(n, "&nbsp;&nbsp;&nbsp;&nbsp;", line, "<br />")             
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
        self.geometry('880x660')
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
            output = 1
            quest = self.quest_title[i]+"<br /><br />"
            with open(self.edit_quest(path_xml), "r") as f:
                quest += f.read()

            self.frame.append(tk.Frame(self.frame2, borderwidth=2, relief="groove"))
            self.frame[i].pack(fill=BOTH)

            self.question.append(tk.Label(self.frame[i], text=self.quest[i], font=10, justify=LEFT))
            self.question_title.append(tk.Label(self.frame[i], text=self.quest_title[i], font=40, justify=LEFT))
            self.button_answer.append(tk.Button(self.frame[i], text='Отправить'))
            self.question[i].grid(row=j, column=0, padx=1, pady=1)
            self.question_title[i].grid(row=j+1, column=0, padx=1, pady=1)

            if self.is_number(self.answer[i]) == False:
                choice = 1 # вводный ответ по умолчанию
            else:
                choice = random.randint(2,3) #множественная выборка или вводный ответ
            print(choice)
            if self.is_number(self.answer[i]) and quiz[3] == 0 and choice == 3: #число ответ
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
                output = 2
            elif self.answer[i] in generator['sign_for_action'] and quiz[3] == 0 and choice == 3: #знаковый ответ
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
                output = 2
            elif len(quiz[4]) != 0 and quiz[3] == 1 and choice != 1: #варианты ответов для типа вопроса с ошибкой
                random.shuffle(quiz[4]) #list_error_answers
                self.correct_answer[i].append(self.answer[i]) #херово работает куда попало
                for num in quiz[4]:
                    self.correct_answer[i].append(str(num))
                self.add_correct_answer(i)
                self.create_input(i,j)
                output = 2
            elif choice == 1 or (self.is_number(self.answer[i]) and choice == 2) or (self.answer[i] in generator['sign_for_action'] and choice == 2) and quiz[3] == 0: #Вводный ответ
                if self.is_float(self.answer[i]):
                    self.answer[i] = round(float(self.answer[i]),generator['fractional_number'])
                self.input_answer_error.append([]) #заглушки
                self.answer_check.append([])
                self.add_correct_answer(i)
                #print(self.input_answer)
                self.input_answer.append(tk.Entry(self.frame[i], width=30, font=40))
                self.input_answer[i].grid(row=j+1, column=1, padx=1, pady=1)
                self.button_answer[i].bind('<Button-1>', partial(self.check_answer, i))
                self.button_answer[i].grid(row=j+1, column=2, padx=1, pady=1)
                output = 1
            print("Ответ: "+str(self.answer[i]))
            j += 2

            if output == 1:
                self.Quiz.addShortAnswerQuestion("Вопрос №"+str(i+1), quest, str(self.answer[i]))
            elif output == 2:
                self.Quiz.addMultipleChoiceQuestion("Вопрос №"+str(i+1), quest, self.correct_answer[i])
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
    if sys.platform == "win32" or sys.platform == "win64":
        app.iconbitmap(path+'/icon.ico')
    app.mainloop()