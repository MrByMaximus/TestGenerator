import webbrowser, sys, os
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
            print('<?xml version="1.0" ?><quiz>')
        file = open(htmlFilename, 'w', encoding="utf-8")
        file.close()

    def CheckChoiceList(self, choiceList, count_multichoice):
        if len(choiceList) > count_multichoice:
            tmp = choiceList[1:]
            shuffle(tmp)
            choiceList = [choiceList[0]] + tmp[:count_multichoice-1]

        if len(choiceList) != count_multichoice:
            print("Ошибка: добавление вопроса с множественным выбором требует ровно" + count_multichoice + " варианта ответов. Дано:\n", choiceList)
            sys.exit(-1)
        if len(set(choiceList)) != count_multichoice:
            print("Предупреждение: добавление вопроса с несколькими вариантами выбора с неуникальными опциями было проигнорировано:\n ", choiceList)
            return

        choiceList = [str(i) for i in choiceList]
        
        return choiceList

    def addShortAnswerQuestion(self, name, question_title, question, answer):
        with redirect_stdout(self.f):
            self.questionHeader("shortanswer", name, question, question_title)
            xml = Template('<usecase>0</usecase>\n<answer fraction="100" format="moodle_auto_format"><text>{{answer}}</text></answer>\n</question>')
            print(str(xml.render(answer=answer)))

        self.addHtmlHeader()
        self.addHtmlQuestionBlock(name, question, question_title, 'shortanswer')
        self.addHtmlAnswerBlockShortAnswer(answer)
        self.edit_open('</body></html>')
    
    def addTrueFalseQuestion(self, name, question_title, question, choiceList):
        choiceList = self.CheckChoiceList(choiceList, 2)        

        with redirect_stdout(self.f):
            self.questionHeader("truefalse", name, question, question_title)
            xml = Template(' <answer fraction="100"><text>{{item}}</text></answer>')
            print(str(xml.render(item=choiceList[0])))
            xml = Template(' <answer fraction="0"><text>{{item}}</text></answer>')
            print(str(xml.render(item=choiceList[1])))
            print('</question>')

        self.addHtmlHeader()
        self.addHtmlQuestionBlock(name, question, question_title, 'truefalse')
        self.addHtmlAnswerBlockMultichoice(choiceList)
        self.edit_open('</body></html>')

    def addMatchingQuestion(self, name, question_title, question, choiceList, ChoiceListAnswer, count_multichoice):
        choiceList = self.CheckChoiceList(choiceList, count_multichoice)
        choiceListAnswer = self.CheckChoiceList(choiceListAnswer, count_multichoice)

        with redirect_stdout(self.f):
            self.questionHeader("matching", name, question, question_title)
            for (item, item_answer) in zip(choiceList, choiceListAnswer):
                xml = Template(' <subquestion><text>{{item_answer}}</text><answer><text>{{item}}</text></answer></subquestion>')
                print(str(xml.render(item=item,item_answer=item_answer)))
            print('<shuffleanswers>true</shuffleanswers>\n</question>')

        self.addHtmlHeader()
        self.addHtmlQuestionBlock(name, question, question_title, 'matching')
        self.addHtmlAnswerBlockMultichoice(choiceList)
        self.edit_open('</body></html>')

    def addMultipleChoiceQuestion(self, name, question_title, question, choiceList, count_multichoice):
        choiceList = self.CheckChoiceList(choiceList, count_multichoice)

        with redirect_stdout(self.f):
            self.questionHeader("multichoice", name, question, question_title)
            xml = Template(' <answer fraction="100"><text>{{choiceList}}</text></answer>')
            print(str(xml.render(choiceList=choiceList[0])))
            for item in choiceList[1:]:
                xml = Template(' <answer fraction="-33.33333" format="html"><text>{{item}}</text></answer>')
                print(str(xml.render(item=item)))
            print('<answernumbering>none</answernumbering>\n<shuffleanswers>1</shuffleanswers>\n<single>true</single>\n</question>')

        self.addHtmlHeader()
        self.addHtmlQuestionBlock(name, question, question_title, 'multichoice')
        self.addHtmlAnswerBlockMultichoice(choiceList)
        self.edit_open('</body></html>')

    def questionHeader(self, type, name, question, question_title):
        with redirect_stdout(self.f):
            xml = Template('<question type="{{type}}">\n <name>\n  <text>{{name}}</text>\n </name>\n <questiontext>\n  <text>\n{{question_title}}<br /><br />')
            print(str(xml.render(type=type,name=name,question_title=question_title)))
            line_numbers = 1
            for item in question:
                xml = Template('<pre>{{line_numbers}}    {{item | e}}</pre>')
                print(str(xml.render(line_numbers=line_numbers,item=item)))
                line_numbers += 1
            print(' ]]>\n  </text>\n </questiontext>')

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
        self.edit_open(html)

    def addHtmlQuestionBlock(self, name, question, question_title, questionType):
        html_out = Template('<body><h2>{{name}}</h2><div class="que {{questionType}} deferredfeedback "><div class="content"><div class="formulation clearfix"><div class="qtext">\n{{question_title}}<br /><br />')
        html = str(html_out.render(name=name,questionType=questionType,question_title=question_title))
        line_numbers = 1
        for item in question:
            html_out = Template('<pre>{{line_numbers}}    {{item | e}}</pre>')
            html += str(html_out.render(line_numbers=line_numbers,item=item))
            line_numbers += 1
        html += '</div>\n'
        self.edit_open(html)

    def addHtmlAnswerBlockMultichoice(self, choiceList):
        html = '<br /><div class="ablock"><div class="answer">'
        for item in choiceList:
            html_out = Template('<div class="r0"><input type="radio" {"checked" if item==choiceList[0] else ""}/><label>{{item}}</label></div>')
            html += str(html_out.render(item=item))
        html += '</div></div></div></div></div>'
        self.edit_open(html)

    def addHtmlAnswerBlockShortAnswer(self, answer):
        html = Template('<br /><div class="ablock"><span class="answer"><input type="text" size="80" class="form-control d-inline" /><p>Правильный ответ: {{answer}} </span></div></div></div></div>')
        self.edit_open(html.render(answer=answer))

    def preview(self):
        webbrowser.open_new_tab(self.htmlFilename)

    def edit_open(self, html):
        f = open(self.htmlFilename, 'a', encoding="utf-8")
        f.write(str(html))
        f.close()

    def close(self):
        with redirect_stdout(self.f):
            print('</quiz>')
        self.f.close()

    def check_empty_file(self):
        if os.stat(self.htmlFilename).st_size == 0:
            os.remove(os.path.join(self.htmlFilename))
        if os.stat(self.filename).st_size == 0:
            os.remove(os.path.join(self.filename))