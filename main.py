from tkinter import *
import tkinter as tk
#import configparser
#import argparse
import sys, os
import random
from jinja2 import Template
from quiz import question

class QuestionWindow(tk.Toplevel):
    def __init__(self, parent, score):
        super().__init__(parent)
        self.title("Результат тестирования")

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.focus_set() #фокус не работает
        self.title("Генерация тестов по программированию")
        #self.iconbitmap('question.ico')
        self.geometry('400x100')
        self.resizable(width=False, height=False)

        self.frame1 = tk.Frame(self)
        self.frame1.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

        self.title = tk.Label(self.frame1, text='Добро пожаловать!', font=40)
        self.title.pack(fill=BOTH)
        self.btn = tk.Button(self.frame1, text='Сгенерировать тест', command=self.create_quest)
        self.btn.pack()
        self.hide_widgets()

        self.score = 0
        self.ans = []
        self.input = []
        self.num = random.randint(5,10)

    def clear(self):
        self.input.delete(0, END)

    def hide_widgets(self):
        self.frame1.grid_forget()

    def open_window(self):
        window = QuestionWindow(self)
        window.grab_set()

    def _on_mousewheel(self, event):
        self.canv.yview(-1*(event.delta/120), "units")

    def create_quest(self):
        self.geometry('800x600')
        self.resizable(width=True, height=True)

        self.outer_frame = tk.Frame(self, bd=0, width=300, height=400)
        self.outer_frame.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        self.canv = tk.Canvas(self.outer_frame)
        #self.canv.bind_all("<MouseWheel>", self._on_mousewheel)
        
        self.canv.config(width=300, height=200)
        self.canv.config(scrollregion=(0, 0, 300, 2000))

        self.sbar = tk.Scrollbar(self.outer_frame)
        self.sbar.config(command=self.canv.yview)
        self.canv.config(yscrollcommand=self.sbar.set)
        self.sbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canv.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        self.frame = tk.Frame(self.canv, width=300, height=2000)
        self.canv.create_window((0, 0), window=self.frame, anchor=tk.NW)

        quest = []
        quest2 = []
        j = 0

        for i in range(self.num):
            #answer = StringVar()
            quiz = question()
            quest.append(quiz[0])
            quest2.append(quiz[2])
            self.ans.append(quiz[1])
            
            self.question = tk.Label(self.frame, text=quest[i], justify=LEFT, font=10, borderwidth=2, relief="groove")
            self.question.grid(row=j, column=0, padx=1, pady=1)
            self.label = tk.Label(self.frame, text=quest2[i], font=40, justify=LEFT)
            self.label.grid(row=j+1, column=0, padx=1, pady=1)
            #self.input = tk.Entry(self.frame, width=40, font=40, justify=LEFT, textvariable=self.ans2)
            #self.input.grid(row=j+1, column=1, padx=1, pady=1)
            self.input.append(tk.Entry(self.frame, width=40, font=40, justify=LEFT))
            self.input[i].grid(row=j+1, column=1, padx=1, pady=1)
            self.button = tk.Button(self.frame, text='Отправить', justify=LEFT, command=self.check_answer)
            self.button.grid(row=j+1, column=2, padx=1, pady=1)
            j += 2

    def check_answer(self):
        #print(self.ans)
        for i in range(len(self.input)):
            for j in range(len(self.ans)):
                if self.input[i].get() == self.ans[j]:
                    del self.input[i]
                    del self.ans[j]
                    self.num -= 1
                    self.score += 1
                    print('true')
                    break
            break

if __name__ == "__main__":
    app = Main()
    app.iconbitmap(os.path.abspath("../../question.ico"))
    app.mainloop()