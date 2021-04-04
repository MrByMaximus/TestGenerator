import webbrowser, sys, os
from sympy.core.basic import Basic
from sympy import *
from contextlib import redirect_stdout

class Quiz:
    def __init__(self, filename, htmlFilename="", questionCreator=None):
        if questionCreator:
            self.C = questionCreator
        else:
            self.C = QuestionCreatorMoodle()
        self.filename=filename
        if not htmlFilename:
            htmlFilename=os.path.splitext(filename)[0]+".html"
        self.htmlFilename = str(os.path.abspath(htmlFilename))
        self.C.open(filename, htmlFilename)

    def addShortAnswerQuestion(self, name, question, answer):
        if isinstance(question, Basic):
            question = f"\({latex(question)}\)"
        self.C.addShortAnswerQuestion(name, question, answer)

    def addMultipleChoiceQuestion(self, name, question, choiceList):
        if isinstance(question, Basic):
            question = f"\({latex(question)}\)"
        if len(choiceList) > 4:
            tmp = choiceList[1:]
            shuffle(tmp)
            choiceList = [choiceList[0]] + tmp[:3]
        choiceList = [ f"\({latex(item)}\)" if isinstance(item, Basic) else item for item in choiceList]

        self.C.addMultipleChoiceQuestion(name, question, choiceList)

    def preview(self):
        webbrowser.open_new_tab(self.htmlFilename)

    def close(self):
        self.C.close()

class QuestionCreatorMoodle():
    def __init__(self):
        super().__init__()
        self.mainCategory = ""

    def open(self, filename, htmlFilename=""):    
        self.f = open(filename, 'w', encoding="utf-8")
        with redirect_stdout(self.f):
            print('<?xml version="1.0" ?> <quiz>')

        if not htmlFilename:
            htmlFilename=os.path.splitext(filename)[0]+".html"
        self.htmlFilename = htmlFilename
        file = open(htmlFilename, 'w', encoding="utf-8")
        file.close()

    def addShortAnswerQuestion(self, name, question, answer):
        with redirect_stdout(self.f):
            self.questionHeader("shortanswer", name, question)
            print("<usecase>0</usecase>")
            print('<answer fraction="100" format="moodle_auto_format"><text>' + answer + '</text></answer>')
            print("</question>")
            print()

        self.addHtmlHeader()
        self.addHtmlQuestionBlock(name, question, 'shortanswer')
        self.addHtmlAnswerBlockShortAnswer(answer)

    def addMultipleChoiceQuestion(self, name, question, choiceList):
        if len(choiceList) != 4:
            print("Ошибка: добавление вопроса с множественным выбором требует ровно 4 варианта ответов. Дано:\n", choiceList)
            sys.exit(-1)
        if len(set(choiceList)) != 4:
            print("Предупреждение: добавление вопроса с несколькими вариантами выбора с неуникальными опциями было проигнорировано:\n ", choiceList)
            return

        choiceList = [str(i) for i in choiceList]

        with redirect_stdout(self.f):
            self.questionHeader("multichoice", name, question)
            print(' <answer fraction="100" format="html"> <text><![CDATA[' + choiceList[0] + ']]></text> </answer>')
            for item in choiceList[1:]:
                print(' <answer fraction="-33.33333" format="html"> <text><![CDATA[' + item + ']]></text> </answer>')
            print('<answernumbering>none</answernumbering>')
            print('<shuffleanswers>1</shuffleanswers>')
            print('<single>true</single>')
            print('</question>')
            print()

        self.addHtmlHeader()
        self.addHtmlQuestionBlock(name, question, 'multichoice')
        self.addHtmlAnswerBlockMultichoice(choiceList)

    def questionHeader(self, type, name, question):
        with redirect_stdout(self.f):
            print('<question type="' + type + '">')
            print(' <name>')
            print('  <text>' + name +'</text>')
            print(' </name>')
            print(' <questiontext format="html">')
            print('  <text><![CDATA[\n' + question + ']]> ')
            print('  </text>')
            print(' </questiontext>')

    def addHtmlHeader(self):
        if os.path.getsize(self.htmlFilename):
            return
        html = """
        <!DOCTYPE html>
        <html>
        <head>
        <title>Тест по программированию на C++</title>
        <style>
        body
        {
        margin-top: 20px;
        margin-right: 20px;
        margin-bottom: 20px;
        margin-left: 20px; <!-110>
        }
        h2
        {
        margin-left: 120px;
        }
        </style>
        </head>
        """
        f=open(self.htmlFilename, 'a', encoding="utf-8")
        f.write(html)
        f.close()

    def addHtmlQuestionBlock(self, name, question, questionType):
        html = f'<body><h2> {name} </h2> <div class="que {questionType} deferredfeedback ">'
        html += f'<div class="content"> <div class="formulation clearfix"> <div class="qtext">\n {question} </div>'
        f=open(self.htmlFilename, 'a', encoding="utf-8")
        f.write(html)
        f.close()

    def addHtmlAnswerBlockMultichoice(self, choiceList):
        html = f'<br /><div class="ablock"> <div class="answer">'
        for item in choiceList:
            html+=f'<div class="r0"> <input type="radio" {"checked" if item==choiceList[0] else ""}/><label>' + item + '</label> </div>'
        html+='</div></div></div></div></div></body></html>'
        f=open(self.htmlFilename, 'a', encoding="utf-8")
        f.write(html)
        f.close()

    def addHtmlAnswerBlockShortAnswer(self, answer):
        html = f'<br /><div class="ablock"> <span class="answer"><input type="text" size="80" class="form-control d-inline" /> <p> Правильный ответ: {answer} </span> </div> </div> </div> </div> </body></html>'
        f=open(self.htmlFilename, 'a', encoding="utf-8")
        f.write(html)
        f.close()

    def close(self):
        with redirect_stdout(self.f):
            print('</quiz>')
        self.f.close()