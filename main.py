# Copyright 2021 Gildenberg Maksim

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from tkinter import messagebox as mb
from tkinter import filedialog
from tkinter import *
import tkinter as tk
import sys, os
import random
import ast
from numpy import arange
from functools import partial
from quiz import Quiz
from generation import Generation

class Main(tk.Tk): #Оконное приложение
    def __init__(self):
        super().__init__()
        self.path = StringVar()
        self.title("Генерация тестов по программированию")
        self.generator_test()

    def generator_test(self):
        self.resizable(width=False, height=False)
        self.geometry("400x170")
        self.frame_out = tk.Frame(self)
        self.frame_out.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98) 
        self.btn_license = tk.Button(self.frame_out, text="Лицензия", command=self.open_license)
        self.btn_license.pack()  
        self.entry_path = tk.Entry(self.frame_out, width=30, textvariable=self.path)     
        self.entry_path.pack(fill=BOTH,pady=5)
        self.button_path = tk.Button(self.frame_out, text='Выбрать рабочую папку', command=self.choose_path)       
        self.button_path.pack()

        self.score = 0
        self.quest = []
        self.quest_title = []
        self.answer = []
        self.correct_answer = []
        self.input_answer = []
        self.input_answer_checkbox = []
        self.input_first_answer_matching = []
        self.answer_first_matching_check = []
        self.input_second_answer_matching = []
        self.answer_second_matching_check = []
        self.answer_check = []
        self.question = []
        self.question_title = []
        self.frame = []
        self.button_answer = []

    def open_license(self):
        mb.showinfo("Лицензия","""Copyright 2021 Gildenberg Maksim

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program. If not, see <https://www.gnu.org/licenses/>.""")

    def choose_path(self):
        filename = filedialog.askdirectory()
        self.path.set(filename)
        if os.path.isfile(filename+'/generator.conf'):
            self.generator = open(self.path.get()+'/generator.conf','r', encoding="utf-8")
            self.generator = ast.literal_eval(self.generator.read())
            if self.check_generator(self.generator):
                self.sign_for_action = self.generator['sign_for_action']
                self.fractional_number = self.generator['fractional_number']
                self.count_multichoice = self.generator['count_multichoice']
                self.count_question = list(self.generator['count_question'])
                count_out = len(os.listdir(self.path.get()+'/'+self.generator['path_output']))
                if count_out == 0:
                    self.num_test = 0
                else:
                    self.num_test = int(count_out / 2)
                self.num_test += 1
                self.title = tk.Label(self.frame_out, text='Укажите количество вопросов для генерации', font=40)
                self.title.pack(fill=BOTH)
                self.count_tests = Spinbox(self.frame_out, from_=self.count_question[0], to=self.count_question[1], width=5) 
                self.count_tests.pack(pady=5)
                self.btn_gen = tk.Button(self.frame_out, text='Сгенерировать тест', command=self.create_quest)
                self.btn_gen.pack()
            else:
                mb.showerror("Ошибка", "Конфигурационный файл имеет ошибки в параметрах!")
        else:
            mb.showerror("Ошибка", "Конфигурационный файл в папке не найден!")

    def check_generator(self, generator): #вообще все проверить!
        if os.path.exists(self.path.get()+'/'+generator['path_output']) and os.path.exists(self.path.get()+'/'+generator['path_cods']) and os.path.exists(self.path.get()+'/'+generator['files']):
            return True
        else:
            return False

    def delete_elements(self):
        self.quest.clear()
        self.quest_title.clear()
        self.question.clear()
        self.question_title.clear()
        self.answer.clear()
        self.correct_answer.clear()
        self.input_answer.clear()
        self.button_answer.clear()
        self.input_answer_checkbox.clear()
        self.answer_check.clear()
        self.input_first_answer_matching.clear()
        self.answer_first_matching_check.clear()
        self.input_second_answer_matching.clear()
        self.answer_second_matching_check.clear()
        self.frame.clear()
        self.canvas.destroy()
        self.frame_in.destroy()
        self.scrolly.destroy()

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def list_index(self, count):
        index = []
        list_index = list(range(1, count+1))
        random.shuffle(list_index)
        for num in list_index:
            index.append(num)
        return index

    def create_input(self, i, j, count, count_true):
        index = self.list_index(count)
        self.answer_check.append([])
        self.input_answer_checkbox.append([])
        for k in range(count):
            self.answer_check[i].append(IntVar())
            self.input_answer_checkbox[i].append(tk.Checkbutton(self.frame[i], text=self.correct_answer[i][k], variable=self.answer_check[i][k], offvalue=0))
            self.input_answer_checkbox[i][k].grid(row=j+1, column=index[k], padx=1, pady=1)
        self.input_answer.append(tk.Entry(self.frame[i]))
        self.answer_first_matching_check.append([]) #заглушки
        self.input_first_answer_matching.append([])
        self.answer_second_matching_check.append([])
        self.input_second_answer_matching.append([])
        self.button_answer[i].bind('<Button-1>', partial(self.check_answer_box, i, count, count_true))
        self.button_answer[i].grid(row=j+1, column=count+1, padx=1, pady=1)

    def create_quest(self):
        self.count_number = int(self.count_tests.get())
        self.score_count = int(self.count_tests.get())
        self.frame_out.destroy()
        self.geometry('880x660')
        self.resizable(width=True, height=True)
        self.canvas = tk.Canvas(self)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.frame_in = tk.Frame(self.canvas)
        self.frame_in.bind('<Configure>', self.on_configure)
        self.canvas.create_window(0, 0, window=self.frame_in)
        self.scrolly = tk.Scrollbar(self, command=self.canvas.yview)
        self.scrolly.place(relx=1, rely=0, relheight=1, anchor='ne')
        self.canvas.configure(yscrollcommand=self.scrolly.set)
        self.Quiz = Quiz(self.path.get()+'/'+self.generator['path_output']+'/quiz'+str(self.num_test)+'.xml')
        generate = Generation(self.path.get())
        j = 0

        for i in range(self.count_number):
            quiz = generate.question_gen()
            while quiz[2] == "[ERROR]":
                mb.showerror("Ошибка", "Скомпилированный код из файла: {code} содержит ошибки".format(code = quiz[1]))
                generate.delete_file()
                i += 1
                quiz = generate.question_gen()

            self.quest.append(quiz[0])
            self.answer.append(quiz[1])
            self.quest_title.append(quiz[2])
            self.frame.append(tk.Frame(self.frame_in, borderwidth=2, relief="groove"))
            self.frame[i].pack(fill=BOTH)
            self.question.append(tk.Label(self.frame[i], text=self.quest[i], font=10, justify=LEFT))
            self.question[i].grid(row=j, column=0, padx=1, pady=1)
            self.question_title.append(tk.Label(self.frame[i], text=self.quest_title[i], font=40, justify=LEFT))
            self.question_title[i].grid(row=j+1, column=0, padx=1, pady=1)
            self.button_answer.append(tk.Button(self.frame[i], text='Отправить'))

            if type(self.answer[i]) == list:
                count_matching = len(self.answer[i])
                choice = random.randint(1,2)
                for k in range(count_matching):
                    if Generation.is_float(str(self.answer[i][k][1])):
                        self.answer[i][k][1] = round(float(self.answer[i][k][1]),self.fractional_number)
                if choice == 1:
                    self.answer_first_matching_check.append([])
                    self.input_first_answer_matching.append([])
                    self.answer_second_matching_check.append([])
                    self.input_second_answer_matching.append([])
                    list_answers = []
                    list_choice = []
                    for k in range(count_matching):
                        list_answers.append(str(self.answer[i][k][1]))
                        list_choice.append(self.answer[i][k][0])
                        self.answer_first_matching_check[i].append(str(self.answer[i][k][1]))
                    list_answers_out = list_answers
                    random.shuffle(list_answers)
                    column = 1
                    for k in range(count_matching):
                        self.answer_second_matching_check[i].append(StringVar())
                        self.answer_second_matching_check[i][k].set(list_answers[k])
                        self.input_first_answer_matching[i].append(tk.Label(self.frame[i], text=self.answer[i][k][0]))
                        self.input_first_answer_matching[i][k].grid(row=j+1, column=column, padx=1, pady=1)
                        self.input_second_answer_matching[i].append(tk.OptionMenu(self.frame[i], self.answer_second_matching_check[i][k], *list_answers))
                        self.input_second_answer_matching[i][k].grid(row=j+1, column=column+1, padx=1, pady=1)
                        column += 2
                    self.input_answer_checkbox.append([]) #заглушки
                    self.answer_check.append([])
                    self.correct_answer.append([])
                    self.input_answer.append(tk.Entry(self.frame[i]))
                    check_matching = 0
                    self.button_answer[i].bind('<Button-1>', partial(self.check_matching, i, count_matching, check_matching))
                    self.button_answer[i].grid(row=j+1, column=column+1, padx=1, pady=1)
                    output = 4
                elif choice == 2 or quiz[3] == 1 or quiz[3] == 2:
                    if Generation.is_number(str(self.answer[i][0][1])): #число ответ
                        list_numbers = []
                        fractional_number_answer = list(self.generator['fractional_number_answer'])
                        number_answer = list(self.generator['number_answer'])
                        self.correct_answer.append([])
                        for k in range(count_matching):
                            self.correct_answer[i].append(str(self.answer[i][k][1])) #Правильный ответ
                        for k in range(count_matching):
                            if Generation.is_float(str(self.answer[i][k][1])):
                                number = self.answer[i][k][1]
                                list_numbers.append(list(arange(number-fractional_number_answer[0], number+fractional_number_answer[1], 1 / (10 ** self.fractional_number))))
                                list_numbers[k] = [round(v,self.fractional_number) for v in list_numbers[k]]
                            else:                               
                                number = int(self.answer[i][k][1])
                                list_numbers.append(list(range(number-number_answer[0], number+number_answer[1])))
                            random.shuffle(list_numbers)                           
                            self.correct_answer[i].append(str(list_numbers[k][0]))
                        self.create_input(i,j,count_matching*2, count_matching)
                    elif self.answer[i] in self.sign_for_action:
                        random.shuffle(self.sign_for_action)
                        self.correct_answer.append([])
                        for k in range(count_matching):
                            self.correct_answer[i].append(self.answer[i]) #Правильный ответ
                        k = 0
                        for num in self.sign_for_action:
                            if num != self.answer[i]:
                                self.correct_answer[i].append(str(num))
                                k += 1
                                if k == (count_matching*2)-1:
                                    break
                        self.create_input(i,j,count_matching*2)
                    output = 6
                print(self.answer[i])     
            else:
                if Generation.is_number(self.answer[i]) == False:
                    choice = 1 # вводный ответ по умолчанию
                else:
                    choice = random.randint(2,3) #множественная выборка или вводный ответ
                if Generation.is_float(str(self.answer[i])):
                    self.answer[i] = str(round(float(self.answer[i]),self.fractional_number))

                if Generation.is_number(str(self.answer[i])) and choice == 3: #число ответ
                    if Generation.is_float(str(self.answer[i])):
                        fractional_number_answer = list(self.generator['fractional_number_answer'])
                        number = float(self.answer[i])
                        list_numbers = list(arange(number-fractional_number_answer[0], number+fractional_number_answer[1], 1 / (10 ** self.fractional_number)))
                        list_numbers = [round(v,self.fractional_number) for v in list_numbers]
                    else:
                        number_answer = list(self.generator['number_answer'])
                        number = int(self.answer[i])
                        list_numbers = list(range(number-number_answer[0], number+number_answer[1]))
                    random.shuffle(list_numbers)
                    self.correct_answer.append([])
                    self.correct_answer[i].append(self.answer[i]) #Правильный ответ
                    k = 0
                    for num in list_numbers:
                        if num != number:
                            self.correct_answer[i].append(str(num))
                            k += 1
                            if k == self.count_multichoice-1:
                                break
                    self.create_input(i,j,self.count_multichoice,1)
                    output = 2
                elif self.answer[i] in self.sign_for_action and choice == 3: #знаковый ответ
                    random.shuffle(self.sign_for_action)
                    self.correct_answer.append([])
                    self.correct_answer[i].append(self.answer[i]) #Правильный ответ
                    k = 0
                    for num in self.sign_for_action:
                        if num != self.answer[i]:
                            self.correct_answer[i].append(str(num))
                            k += 1
                            if k == self.count_multichoice-1:
                                break
                    self.create_input(i,j,self.count_multichoice,1)
                    output = 2
                elif quiz[3] == 5:
                    self.correct_answer.append([])
                    if self.answer[i] == "yes":
                        self.correct_answer[i].append("Да")
                        self.correct_answer[i].append("Нет")
                    else:
                        self.correct_answer[i].append("Нет")
                        self.correct_answer[i].append("Да")
                    self.create_input(i,j,2,1)
                    output = 3
                elif choice == 1 or (Generation.is_number(self.answer[i]) and choice == 2) or (self.answer[i] in self.sign_for_action and choice == 2): #Вводный ответ
                    self.input_answer_checkbox.append([]) #заглушки
                    self.answer_check.append([])
                    self.correct_answer.append([])
                    self.answer_first_matching_check.append([])
                    self.input_first_answer_matching.append([])
                    self.answer_second_matching_check.append([])
                    self.input_second_answer_matching.append([])
                    self.input_answer.append(tk.Entry(self.frame[i], width=30, font=40))
                    self.input_answer[i].grid(row=j+1, column=1, padx=1, pady=1)
                    self.button_answer[i].bind('<Button-1>', partial(self.check_answer, i))
                    self.button_answer[i].grid(row=j+1, column=2, padx=1, pady=1)
                    if Generation.is_number(self.answer[i]) == True:
                        output = 1
                    else:
                        output = 5
                print("Ответ: "+str(self.answer[i]))
            j += 2
            generate.delete_file()   
        
            if output == 1:
                self.Quiz.addShortAnswerQuestion("Вопрос №"+str(i+1), self.quest_title[i], self.quest[i], str(self.answer[i]))
            elif output == 2:
                self.Quiz.addMultipleChoiceQuestion("Вопрос №"+str(i+1), self.quest_title[i], self.quest[i], self.correct_answer[i], self.count_multichoice, 1)
            elif output == 3:
                self.Quiz.addTrueFalseQuestion("Вопрос №"+str(i+1), self.quest_title[i], self.quest[i], self.correct_answer[i])
            elif output == 4:
                self.Quiz.addMatchingQuestion("Вопрос №"+str(i+1), self.quest_title[i], self.quest[i], list_answers_out, list_choice)
            elif output == 5:
                self.Quiz.addNumericalResponseQuestion("Вопрос №"+str(i+1), self.quest_title[i], self.quest[i], self.answer[i])
            else:
                self.Quiz.addMultipleChoiceQuestion("Вопрос №"+str(i+1), self.quest_title[i], self.quest[i], self.correct_answer[i], count_matching*2, count_matching)
        self.Quiz.close()
        self.Quiz.delete_file()

    def check_matching(self, i, count_matching, check_matching, event):
        self.button_answer[i].destroy()
        self.count_number -= 1
        right_result = 0
        for k in range(count_matching):
            if self.answer_first_matching_check[i][k] == self.answer_second_matching_check[i][k].get():
                right_result += 1
                self.input_first_answer_matching[i][k].config(state="disabled",bg="lightgreen")
                self.input_second_answer_matching[i][k].config(state="disabled",bg="lightgreen")
            else:
                self.input_first_answer_matching[i][k].config(state="disabled",bg="tomato")
                self.input_second_answer_matching[i][k].config(state="disabled",bg="tomato")
        if right_result == count_matching:
            self.score += 1
            self.frame[i].config(bg="lightgreen")
            self.question[i].config(bg="lightgreen")
            self.question_title[i].config(bg="lightgreen")
        else:
            self.frame[i].config(bg="tomato")
            self.question[i].config(bg="tomato")
            self.question_title[i].config(bg="tomato")
        self.result()

    def check_answer_box(self, i, count_multi, count_true, event):
        self.button_answer[i].destroy()
        self.count_number -= 1
        check = 0
        for k in range(count_true):
            if self.answer_check[i][k].get() == True:
                check = 1
            else:
                check = 0
        if check == 1:
            self.score += 1
            for k in range(count_multi):
                self.input_answer_checkbox[i][k].config(state="disabled",bg="lightgreen")
            self.frame[i].config(bg="lightgreen")
            self.question[i].config(bg="lightgreen")
            self.question_title[i].config(bg="lightgreen")
        else:
            for k in range(count_multi):
                self.input_answer_checkbox[i][k].config(state="disabled",bg="tomato")
            self.frame[i].config(bg="tomato")
            self.question[i].config(bg="tomato")
            self.question_title[i].config(bg="tomato")
        self.result()

    def check_answer(self, i, event):
        self.button_answer[i].destroy()
        self.count_number -= 1
        if self.input_answer[i].get() == str(self.answer[i]):
            self.input_answer[i].config(state="readonly",bg="lightgreen")
            self.score += 1
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
            mb.showinfo("Результат", "Количество правильных ответов: {score} из {number}".format(score = self.score, number = self.score_count))
            self.Quiz.preview()
            self.delete_elements()
            self.generator_test()

if __name__ == "__main__":
    app = Main()
    if sys.platform == "win32" or sys.platform == "win64":
        app.iconbitmap(os.getcwd()+'/icon.ico')
    app.mainloop()