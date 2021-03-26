from tkinter import *
import tkinter as tk
#import configparser
#import argparse
import sys, os
import random
from jinja2 import Template
from quiz import question
from functools import partial
from tkinter import messagebox as mb

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Генерация тестов по программированию")
        self.generator_test()

    def generator_test(self):
        self.geometry('400x100')
        self.resizable(width=False, height=False)

        self.frame1 = tk.Frame(self)
        self.frame1.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

        self.title = tk.Label(self.frame1, text='Добро пожаловать!', font=40)
        self.title.pack(fill=BOTH)
        self.btn = tk.Button(self.frame1, text='Сгенерировать тест', command=self.create_quest)
        self.btn.pack()

        self.score = 0
        self.quest = []
        self.quest2 = []
        self.ans = []
        self.answer = []
        self.input1 = []
        self.input2 = []
        self.input3 = []
        self.input4 = []
        self.question = []
        self.question2 = []
        self.frame = []
        self.button = []
        #self.num = random.randint(5,10)
        self.num = 2
        self.number = self.num
        self.selected_true = 0
        self.selected_false = 0

    def delete_elements(self):
        self.quest.clear()
        self.quest2.clear()
        self.question.clear()
        self.question2.clear()
        self.ans.clear()
        self.answer.clear()
        self.button.clear()
        self.input1.clear()
        self.input2.clear()
        self.input3.clear()
        self.input4.clear()
        self.frame.clear()
        self.button.clear()
        self.canvas.destroy()
        self.frame2.destroy()
        self.scrolly.destroy()
        #self.scrollx.destroy()

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def is_number(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    def checkbox_true(self):
        self.selected_true = 1

    def checkbox_false(self):
        self.selected_false = 1

    def create_quest(self):
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
        #self.scrollx = tk.Scrollbar(self, command=self.canvas.xview)
        self.scrolly.place(relx=1, rely=0, relheight=1, anchor='ne')
        #self.scrollx.place(relx=1, rely=0, relheight=1, anchor='ne')
        self.canvas.configure(yscrollcommand=self.scrolly.set)
        #self.canvas.configure(xscrollcommand=self.scrollx.set)

        j = 0
        for i in range(self.num):
            quiz = question()
            self.quest.append(quiz[0])
            self.quest2.append(quiz[2])
            self.ans.append(quiz[1])
            choice = random.randint(1,2) #выборка или ответ или файл

            self.frame.append(tk.Frame(self.frame2, borderwidth=2, relief="groove"))
            self.frame[i].pack(fill=BOTH)

            self.question.append(tk.Label(self.frame[i], text=self.quest[i], font=10, justify=LEFT))
            self.question2.append(tk.Label(self.frame[i], text=self.quest2[i], font=40, justify=LEFT))
            self.button.append(tk.Button(self.frame[i], text='Отправить'))
            self.button[i].bind('<Button-1>', partial(self.check_answer, i))
            self.question[i].grid(row=j, column=0, padx=1, pady=1)
            self.question2[i].grid(row=j+1, column=0, padx=1, pady=1)

            if self.is_number(self.ans[i]) and choice == 1:
                index4 = random.randint(1, 4)
                ans1 = random.randint(int(self.ans[i])-10, int(self.ans[i])+10) #генерировать без повторений
                ans2 = random.randint(int(self.ans[i])-10, int(self.ans[i])+10)
                ans3 = random.randint(int(self.ans[i])-10, int(self.ans[i])+10)
                if ans1 == int(self.ans[i]):
                    ans1 += 1
                if ans2 == int(self.ans[i]):
                    ans2 += 1
                if ans3 == int(self.ans[i]):
                    ans3 += 1
                self.input1.append(tk.Checkbutton(self.frame[i], text=ans1, variable=ans1, offvalue=0, command=self.checkbox_false))
                self.input2.append(tk.Checkbutton(self.frame[i], text=ans2, variable=ans2, offvalue=0, command=self.checkbox_false))
                self.input3.append(tk.Checkbutton(self.frame[i], text=ans3, variable=ans3, offvalue=0, command=self.checkbox_false))
                self.input4.append(tk.Checkbutton(self.frame[i], text=self.ans[i], variable=self.ans[i], offvalue=0, command=self.checkbox_true))
                if index4 == 1:
                    index1 = 2
                    index2 = 3
                    index3 = 4
                elif index4 == 2:
                    index1 = 1
                    index2 = 3
                    index3 = 4
                elif index4 == 3:
                    index1 = 1
                    index2 = 2
                    index3 = 4
                else:
                    index1 = 1
                    index2 = 2
                    index3 = 3
                self.input1[i].grid(row=j+1, column=index1, padx=1, pady=1)  
                self.input2[i].grid(row=j+1, column=index2, padx=1, pady=1)  
                self.input3[i].grid(row=j+1, column=index3, padx=1, pady=1)  
                self.input4[i].grid(row=j+1, column=index4, padx=1, pady=1)
                self.answer.append(tk.Entry(self.frame[i], width=40, font=40)) #костыль
                self.button[i].grid(row=j+1, column=5, padx=1, pady=1)
            elif choice == 2:
                self.input1.append('')
                self.input2.append('')
                self.input3.append('')
                self.input4.append('')
                self.answer.append(tk.Entry(self.frame[i], width=40, font=40))
                self.answer[i].grid(row=j+1, column=1, padx=1, pady=1)
                self.button[i].grid(row=j+1, column=2, padx=1, pady=1)
            
            j += 2

    def check_answer(self, i, event):
        self.button[i].destroy()
        self.num -= 1

        if self.selected_true == 1 and self.selected_false == 0:
            self.selected_true = 0
            self.score += 1
            self.input1[i].config(state="disabled",bg="lightgreen")
            self.input2[i].config(state="disabled",bg="lightgreen")
            self.input3[i].config(state="disabled",bg="lightgreen")
            self.input4[i].config(state="disabled",bg="lightgreen")
            self.frame[i].config(bg="lightgreen")
            self.question[i].config(bg="lightgreen")
            self.question2[i].config(bg="lightgreen")
        elif self.answer[i].get() == self.ans[i] and self.selected_true == 0 and self.selected_false == 0:
            self.score += 1
            self.answer[i].config(state="readonly",bg="lightgreen")
            self.frame[i].config(bg="lightgreen")
            self.question[i].config(bg="lightgreen")
            self.question2[i].config(bg="lightgreen")
        elif (self.selected_true == 0 and self.selected_false == 1) or (self.selected_true == 1 and self.selected_false == 1):
            self.selected_false = 0
            self.input1[i].config(state="disabled",bg="tomato")
            self.input2[i].config(state="disabled",bg="tomato")
            self.input3[i].config(state="disabled",bg="tomato")
            self.input4[i].config(state="disabled",bg="tomato")
            self.frame[i].config(bg="tomato")
            self.question[i].config(bg="tomato")
            self.question2[i].config(bg="tomato")
        else:
            self.answer[i].config(state="readonly",bg="tomato")
            self.frame[i].config(bg="tomato")
            self.question[i].config(bg="tomato")
            self.question2[i].config(bg="tomato")
        
        if self.num == 0:
            if mb.showinfo("Результат", "Количество правильных ответов: {score} из {number}".format(score = self.score, number = self.number)):
                self.completing_test()

    def completing_test(self):
        self.delete_elements()
        self.generator_test()

if __name__ == "__main__":
    app = Main()
    app.iconbitmap(os.path.abspath("../../question.ico"))
    app.mainloop()