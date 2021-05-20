import webbrowser, sys, os
from contextlib import redirect_stdout
from jinja2 import Template
import random

class Quiz: #Запись в html и xml
    def __init__(self, filename, htmlFilename=""):
        super().__init__()
        self.filename = filename
        if not htmlFilename:
            htmlFilename = os.path.splitext(filename)[0]+".html"
        self.htmlFilename = str(htmlFilename)
        self.xmlFilename = open(filename, 'w', encoding="utf-8")
        with redirect_stdout(self.xmlFilename):
            print('<?xml version="1.0" ?><quiz>')
        file = open(htmlFilename, 'w', encoding="utf-8")
        file.close()

    def checkChoiceList(self, choiceList, count_multichoice, count_true):
        if len(choiceList) > count_multichoice:
            tmp = choiceList[count_true:]
            random.shuffle(tmp)
            for k in range(count_true):
                choiceList += [choiceList[k]]
            choiceList += tmp[:count_multichoice-1]
        choiceList = [str(i) for i in choiceList]
        
        return choiceList

    def addShortAnswerQuestion(self, name, question_title, question, answer):
        with redirect_stdout(self.xmlFilename):
            self.questionHeader("shortanswer", name, question, question_title)
            xml = Template('<usecase>0</usecase>\n<answer fraction="100" format="moodle_auto_format"><text>{{answer}}</text></answer>\n</question>')
            print(str(xml.render(answer=answer)))

        self.addHtmlHeader()
        self.addHtmlQuestionBlock(name, question, question_title, 'shortanswer')
        self.addHtmlAnswerBlockShortAnswer(answer)
        self.edit_open('</body></html>')
    
    def addNumericalResponseQuestion(self, name, question_title, question, answer):
        with redirect_stdout(self.xmlFilename):
            self.questionHeader("numerical", name, question, question_title)
            xml = Template('<usecase>0</usecase>\n<answer fraction="100" format="moodle_auto_format"><text>{{answer}}</text></answer>\n</question>')
            print(str(xml.render(answer=answer)))

        self.addHtmlHeader()
        self.addHtmlQuestionBlock(name, question, question_title, 'numerical')
        self.addHtmlAnswerBlockShortAnswer(answer)
        self.edit_open('</body></html>')

    def addTrueFalseQuestion(self, name, question_title, question, choiceList):
        #choiceList = self.CheckChoiceList(choiceList, 2, 1)        
        with redirect_stdout(self.xmlFilename):
            self.questionHeader("truefalse", name, question, question_title)
            xml = Template(' <answer fraction="100"><text>{{item}}</text></answer>')
            print(str(xml.render(item=choiceList[0])))
            xml = Template(' <answer fraction="0"><text>{{item}}</text></answer>')
            print(str(xml.render(item=choiceList[1])))
            print('</question>')

        self.addHtmlHeader()
        self.addHtmlQuestionBlock(name, question, question_title, 'truefalse')
        self.addHtmlAnswerBlockMultichoice(choiceList, 1)
        self.edit_open('</body></html>')

    def addMatchingQuestion(self, name, question_title, question, сhoiceListAnswer, choiceList):
        #random.shuffle(сhoiceListAnswer)
        with redirect_stdout(self.xmlFilename):
            self.questionHeader("matching", name, question, question_title)
            for (item, item_answer) in zip(choiceList, сhoiceListAnswer):
                xml = Template(' <subquestion><text>{{item}}</text><answer><text>{{item_answer}}</text></answer></subquestion>')
                print(str(xml.render(item=item,item_answer=item_answer)))
            print('<shuffleanswers>true</shuffleanswers>\n</question>')

        self.addHtmlHeader()
        self.addHtmlQuestionBlock(name, question, question_title, 'matching')
        self.addHtmlAnswerBlockMatching(сhoiceListAnswer, choiceList)
        self.edit_open('</body></html>')

    def addMultipleChoiceQuestion(self, name, question_title, question, choiceList, count_multichoice, count_true):
        choiceList = self.checkChoiceList(choiceList, count_multichoice, count_true)
        with redirect_stdout(self.xmlFilename):
            self.questionHeader("multichoice", name, question, question_title)
            for item in choiceList[:count_true]:
                xml = Template(' <answer fraction="100"><text>{{item_true}}</text></answer>')
                print(str(xml.render(item_true=item)))
            for item in choiceList[count_true:]:
                xml = Template(' <answer fraction="-33.33333" format="html"><text>{{item_false}}</text></answer>')
                print(str(xml.render(item_false=item)))
            print('<answernumbering>none</answernumbering>\n<shuffleanswers>1</shuffleanswers>\n<single>true</single>\n</question>')

        self.addHtmlHeader()
        self.addHtmlQuestionBlock(name, question, question_title, 'multichoice')
        self.addHtmlAnswerBlockMultichoice(choiceList, count_true)
        self.edit_open('</body></html>')

    def questionHeader(self, type, name, question, question_title):
        with redirect_stdout(self.xmlFilename):
            xml = Template('<question type="{{type}}">\n <name>\n  <text>{{name}}</text>\n </name>\n <questiontext format="html">\n  <text><![CDATA[<pre>')
            print(str(xml.render(type=type,name=name)))
            xml = Template('{{question | e}}')
            print(str(xml.render(question=question)))
            xml = Template('</pre><br /><br />{{question_title}}]]>\n  </text>\n </questiontext>')
            print(str(xml.render(question_title=question_title)))

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
        html_out = Template('<body><h2>{{name}}</h2><div class="que {{questionType}} deferredfeedback "><div class="content"><div class="formulation clearfix"><div class="qtext"><pre>')
        html = str(html_out.render(name=name,questionType=questionType))
        html_out = Template('{{question | e}}')
        html += str(html_out.render(question=question))
        html_out = Template('</pre><br /><br />{{question_title}}</div>\n')
        html += str(html_out.render(question_title=question_title))
        self.edit_open(html)

    def addHtmlAnswerBlockMatching(self, сhoiceListAnswer, choiceList):
        html = '<br /><div class="ablock"><div class="answer">'
        for item in choiceList:
            html_out = Template('<label>{{item}}</label>')
            html += str(html_out.render(item=item)) + '<form action="formdata" method="post" name="form1"><select name="list1">'
            for item_answer in сhoiceListAnswer:
                html_out = Template('<option>{{item_answer}}</option>')
                html += str(html_out.render(item_answer=item_answer))
            html += '</select></form>'        
        html += '</div></div></div></div></div>'
        self.edit_open(html)

    def addHtmlAnswerBlockMultichoice(self, choiceList, count_true):
        html = '<br /><div class="ablock"><div class="answer">'
        for item in choiceList:
            html += f'<div class="r0"><input type="radio" {"checked" if item in choiceList[:count_true] else ""}/>'
            html_out = Template('<label>{{item}}</label></div>')
            html += str(html_out.render(item=item))
        html += '</div></div></div></div></div>'
        self.edit_open(html)

    def addHtmlAnswerBlockShortAnswer(self, answer):
        html = Template('<br /><div class="ablock"><span class="answer"><input type="text" size="80" class="form-control d-inline" value="{{answer}}"/></span></div></div></div></div>')
        self.edit_open(html.render(answer=answer))

    def preview(self):
        if os.path.getsize(self.htmlFilename) > 0:
            webbrowser.open_new_tab(self.htmlFilename)

    def edit_open(self, html):
        f = open(self.htmlFilename, 'a', encoding="utf-8")
        f.write(str(html))
        f.close()

    def close(self):
        with redirect_stdout(self.xmlFilename):
            print('</quiz>')
        self.xmlFilename.close()

    def delete_file(self):
        if os.path.getsize(self.htmlFilename) == 0:
            os.remove(os.path.join(self.htmlFilename))
        if os.path.getsize(self.filename) <= 37:
            os.remove(os.path.join(self.filename))