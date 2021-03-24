from tkinter import *
import configparser
import argparse
import quiz2
from jinja2 import Template

score = 0

window = Tk()

def btn_click():
    print("text")

window.title("Генерация тестов по программированию")
window.geometry('640x480')
window.resizable(width=False, height=False)

canvas = Canvas(window, height=300, width=250)
canvas.pack()

frame = Frame(window)
frame.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

title = Label(frame, text='Добро пожаловать', font=40)
title.pack()
btn = Button(frame, text='Сгенерировать тест', command=btn_click, bg='gray')
btn.pack()

window.mainloop()