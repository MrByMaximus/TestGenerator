import webbrowser, sys, os
from sympy.core.basic import Basic
from sympy import *
from contextlib import redirect_stdout
from jinja2 import Template
from generation import generator

class Quiz: #Запись в html и xml
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