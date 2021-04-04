from tkinter import *
import tkinter as tk
import sys, os
import random
import numpy
from jinja2 import Template
from quiz import question
from func import *
import func
from create_quiz import Quiz
from functools import partial
from tkinter import messagebox as mb

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Генерация тестов по программированию")
        count_out = len(os.listdir(os.path.abspath('../../output')))
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

        self.title = tk.Label(self.frame1, text='Укажите количество вопросов для генерации', font=40)
        self.title.pack(fill=BOTH)
        self.count_tests = Spinbox(self.frame1, from_=2, to=10, width=5) 
        self.count_tests.pack(pady=5)
        self.btn_gen = tk.Button(self.frame1, text='Сгенерировать тест', command=self.create_quest)
        self.btn_gen.pack()

        self.num_test += 1
        self.score = 0
        self.quest = []
        self.quest2 = []
        self.answer = []
        self.correct_answer = [[]]
        self.input_answer = []
        self.input_answer1 = []
        self.input_answer2 = []
        self.input_answer3 = []
        self.input_answer4 = []
        self.answer1_check = []
        self.answer2_check = []
        self.answer3_check = []
        self.answer4_check = []
        self.question = []
        self.question2 = []
        self.frame = []
        self.button_answer = []

    def delete_elements(self):
        self.quest.clear()
        self.quest2.clear()
        self.question.clear()
        self.question2.clear()
        self.answer.clear()
        self.correct_answer.clear()
        self.input_answer.clear()
        self.button_answer.clear()
        self.input_answer1.clear()
        self.input_answer2.clear()
        self.input_answer3.clear()
        self.input_answer4.clear()
        self.answer1_check.clear()
        self.answer2_check.clear()
        self.answer3_check.clear()
        self.answer4_check.clear()
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
        list_index = list(range(1, 5))
        random.shuffle(list_index)
        for num in list_index:
            index.append(num)

        return index

    def create_input(self, i, j):
        self.answer1_check.append(IntVar())
        self.answer2_check.append(IntVar())
        self.answer3_check.append(IntVar())
        self.answer4_check.append(IntVar())
        self.input_answer1.append(tk.Checkbutton(self.frame[i], text=self.correct_answer[i][0], variable=self.answer1_check[i], offvalue=0)) #true
        self.input_answer2.append(tk.Checkbutton(self.frame[i], text=self.correct_answer[i][1], variable=self.answer2_check[i], offvalue=0))
        self.input_answer3.append(tk.Checkbutton(self.frame[i], text=self.correct_answer[i][2], variable=self.answer3_check[i], offvalue=0))
        self.input_answer4.append(tk.Checkbutton(self.frame[i], text=self.correct_answer[i][3], variable=self.answer4_check[i], offvalue=0))
        index = self.list_index()
        self.input_answer1[i].grid(row=j+1, column=index[0], padx=1, pady=1)  
        self.input_answer2[i].grid(row=j+1, column=index[1], padx=1, pady=1)  
        self.input_answer3[i].grid(row=j+1, column=index[2], padx=1, pady=1)  
        self.input_answer4[i].grid(row=j+1, column=index[3], padx=1, pady=1)
        self.input_answer.append(tk.Entry(self.frame[i], width=40, font=40)) #костыль
        self.button_answer[i].bind('<Button-1>', partial(self.check_answer_box, i))
        self.button_answer[i].grid(row=j+1, column=5, padx=1, pady=1)

        return j

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
                print(line, "<br />", end='')
        os.unlink(filename + '.bak')

        return filename

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

        self.Quiz = Quiz(os.path.abspath("../../output/quiz"+str(self.num_test)+".xml"))
        j = 0
        for i in range(self.count_number):
            quiz = question()
            self.quest.append(quiz[0])
            self.quest2.append(quiz[2])
            self.answer.append(quiz[1])
            choice = random.randint(1,2) #выборка или ответ или файл
            #choice = 1

            quest = self.quest2[i]+"<br /><br />"
            with open(self.edit_quest(os.path.abspath('quest.txt')), "r") as f:
                quest += f.read()

            self.frame.append(tk.Frame(self.frame2, borderwidth=2, relief="groove"))
            self.frame[i].pack(fill=BOTH)

            self.question.append(tk.Label(self.frame[i], text=self.quest[i], font=10, justify=LEFT))
            self.question2.append(tk.Label(self.frame[i], text=self.quest2[i], font=40, justify=LEFT))
            self.button_answer.append(tk.Button(self.frame[i], text='Отправить'))
            self.question[i].grid(row=j, column=0, padx=1, pady=1)
            self.question2[i].grid(row=j+1, column=0, padx=1, pady=1)

            if quiz[3] == 0 and choice == 1: #число ответ
                if self.is_float(self.answer[i]):
                    self.answer[i] = round(float(self.answer[i]),1)
                    number = self.answer[i]
                    list_numbers = list(numpy.arange(number-1, number+1.1, 0.1))
                    list_numbers = [round(v,1) for v in list_numbers]
                else:
                    number = int(self.answer[i])
                    list_numbers = list(range(number-10, number+11))
                random.shuffle(list_numbers)
                k = 0
                self.correct_answer[i].append(self.answer[i])
                for num in list_numbers:
                    if num != number:
                        self.correct_answer[i].append(str(num))
                        k += 1
                        if k == 3:
                            break
                self.add_correct_answer(i)
                j = self.create_input(i,j)
            elif self.answer[i] in generator['sign_for_action'] and quiz[3] == 0 and choice == 1: #знаковый ответ
                sign = generator['sign_for_action']
                random.shuffle(sign)
                k = 0
                self.correct_answer[i].append(self.answer[i])
                for num in sign:
                    if num != self.answer[i]:
                        self.correct_answer[i].append(str(num))
                        k += 1
                        if k == 3:
                            break
                self.add_correct_answer(i)
                j = self.create_input(i,j)
            elif quiz[4] and quiz[3] == 1 and choice == 1: #варианты овтетов для типа вопроса с ошибкой
                random.shuffle(quiz[4]) #list_error_answers
                self.correct_answer[i].append(self.answer[i])
                for num in quiz[4]:
                    self.correct_answer[i].append(str(num))
                self.add_correct_answer(i)
                j = self.create_input(i,j)
            elif choice == 2: #Вводный ответ
                if self.is_float(self.answer[i]):
                    self.answer[i] = round(float(self.answer[i]),1)
                self.input_answer1.append('') #заглушки
                self.input_answer2.append('')
                self.input_answer3.append('')
                self.input_answer4.append('')
                self.answer1_check.append('')
                self.answer2_check.append('')
                self.answer3_check.append('')
                self.answer4_check.append('')
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
        func.delete_file()

    def check_answer_box(self, i, event):
        self.button_answer[i].destroy()
        self.count_number -= 1

        if self.answer1_check[i].get() == True and self.answer2_check[i].get() == False and self.answer3_check[i].get() == False and self.answer4_check[i].get() == False:
            self.score += 1
            self.input_answer1[i].config(state="disabled",bg="lightgreen")
            self.input_answer2[i].config(state="disabled",bg="lightgreen")
            self.input_answer3[i].config(state="disabled",bg="lightgreen")
            self.input_answer4[i].config(state="disabled",bg="lightgreen")
            self.frame[i].config(bg="lightgreen")
            self.question[i].config(bg="lightgreen")
            self.question2[i].config(bg="lightgreen")
        else:
            self.input_answer1[i].config(state="disabled",bg="tomato")
            self.input_answer2[i].config(state="disabled",bg="tomato")
            self.input_answer3[i].config(state="disabled",bg="tomato")
            self.input_answer4[i].config(state="disabled",bg="tomato")
            self.frame[i].config(bg="tomato")
            self.question[i].config(bg="tomato")
            self.question2[i].config(bg="tomato")

        self.result()

    def check_answer(self, i, event):
        self.button_answer[i].destroy()
        self.count_number -= 1

        if self.input_answer[i].get() == str(self.answer[i]):
            self.score += 1
            self.input_answer[i].config(state="readonly",bg="lightgreen")
            self.frame[i].config(bg="lightgreen")
            self.question[i].config(bg="lightgreen")
            self.question2[i].config(bg="lightgreen")
        else:
            self.input_answer[i].config(state="readonly",bg="tomato")
            self.frame[i].config(bg="tomato")
            self.question[i].config(bg="tomato")
            self.question2[i].config(bg="tomato")
        
        self.result()
        
    def result(self):
        if self.count_number == 0:
            if mb.showinfo("Результат", "Количество правильных ответов: {score} из {number}".format(score = self.score, number = self.score_count)):
                self.Quiz.preview()
                self.Quiz.close()
                self.delete_elements()
                self.generator_test()

if __name__ == "__main__":
    app = Main()
    app.iconbitmap(os.path.abspath("../../icon.ico"))
    app.mainloop()