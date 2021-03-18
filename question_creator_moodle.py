from question_creator_interface import QuestionCreatorInterface
from contextlib import redirect_stdout
import sys, os


'''
QuestionCreatorMoodle class implements the QuestionCreatorInterface for Moodle questions
'''
class QuestionCreatorMoodle(QuestionCreatorInterface):
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

    def setMainCategory(self, mainCategory):
        self.mainCategory = mainCategory

    def setCategory(self, category):
        with redirect_stdout(self.f):
            print("<!-- question: 0  -->")
            print('<question type="category">')
            print(" <category>")
            if self.mainCategory:
                print("<text>$course$/top/"+self.mainCategory+"/"+category+"</text>")
            else:
                print("<text>$course$/top/"+category+"</text>")
            print("</category>")
            print("</question>")

    def addMultipleChoiceQuestion(self, name, question, choiceList):
        if len(choiceList) != 4: # check we got 4 options
            print("Error: addMultipleChoiceQuestion requires exactly 4 options. Given:\n", choiceList)
            sys.exit(-1)
        if len(set(choiceList)) != 4: # check all options are different
            print("Предупреждение: добавление вопроса с несколькими вариантами выбора с неуникальными опциями было проигнорировано:\n ", choiceList)
            return

        choiceList = [str(i) for i in choiceList]

        with redirect_stdout(self.f):
            self.questionHeader("multichoice", name, question)
            print(' <answer fraction="100" format="html"> <text><![CDATA[' + choiceList[0] + ']]></text> </answer>')
            for item in choiceList[1:]:
                print(' <answer fraction="-33.33333" format="html"> <text><![CDATA[' + item + ']]></text> </answer>')
            # Uncomment for old Moodle versions
            #print('<answer fraction="0"> <text>' + "No vull contestar la pregunta" + '</text> </answer>')
            print('<answernumbering>none</answernumbering>')
            print('<shuffleanswers>1</shuffleanswers>')
            print('<single>true</single>')
            print('</question>')
            print()

        self.addHtmlHeader()
        self.addHtmlQuestionBlock(name, question, 'multichoice')
        self.addHtmlAnswerBlockMultichoice(choiceList)





    def addNumericalQuestion(self, name, question, answer, tolerance=0.01):
        if type(answer)!=type(list()):
            answer=[answer]
        with redirect_stdout(self.f):
            self.questionHeader("numerical", name, question)
            print("<defaultgrade>1.0000000</defaultgrade>")
            for item in answer:
                print('<answer fraction="100" format="moodle_auto_format"> <text>' + str(item) + '</text> <tolerance>'+str(tolerance) + '</tolerance> </answer>')

            print("<unitgradingtype>0</unitgradingtype><unitsleft>0</unitsleft>")
            print("</question>")
            print()

        self.addHtmlHeader()
        self.addHtmlQuestionBlock(name, question, 'numerical')
        self.addHtmlAnswerBlockNumerical(str(answer))

    # Experimental code!
    def addMultiNumericalQuestion(self, name, question, answerList, tolerance=0.01):
        with redirect_stdout(self.f):
            fullquestion = question
            for item in answerList:
                fullquestion+= '<p>{:NUMERICAL:%100%' + str(item) + ':'+str(tolerance)+'#}</p>'

            self.questionHeader("cloze", name, fullquestion)
            print("<defaultgrade>1.0000000</defaultgrade> <hidden>0</hidden>")
            print("</question>")
            print()

            # TODO: add preview

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



    def addMatchingQuestion(self, name, question, pairList):
        with redirect_stdout(self.f):
            self.questionHeader("matching", name, question)
            print('<defaultgrade>1.0000000</defaultgrade>')
            print('<penalty>0.3333333</penalty>')
            for pair in pairList:
                print('<subquestion format="html"> <text> <![CDATA[' + pair[0] + ']]> </text> <answer> <text> <![CDATA[' + pair[1] + ']]> </text></answer> </subquestion>')
            print(' <shuffleanswers>1</shuffleanswers>')
            print('</question>')

        self.addHtmlHeader()
        self.addHtmlQuestionBlock(name, question, 'match')
        self.addHtmlAnswerBlockMatch(pairList)

    def close(self):
        with redirect_stdout(self.f):
            print('</quiz>')
        self.f.close()

    def questionHeader(self, type, name, question):
        with redirect_stdout(self.f):
            print('<question type="' + type + '">')
            print(' <name>')
            print('  <text>' + name +'</text>')
            print(' </name>')
            print(' <questiontext format="html">')
            print('  <text><![CDATA[' + question + ']]> ')
            print('  </text>')
            print(' </questiontext>')

    # experimental!
    def addHtmlHeader(self):
        if os.path.getsize(self.htmlFilename):
            return
        html = """
        <!DOCTYPE html>
        <html>
        <head>
        <title>Question preview</title>
        <script type="text/javascript" async
        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/latest.js?config=TeX-MML-AM_CHTML">
        </script>
        <link rel="stylesheet" type="text/css" href="https://gentest.moodlecloud.com/theme/yui_combo.php?rollup/3.17.2/yui-moodlesimple-min.css" />
        <script type="text/css"></script>
        <link rel="stylesheet" type="text/css" href="https://gentest.moodlecloud.com/theme/styles.php/classic/1591760472_1/all" />
        <style>
        body
        {
        margin-top: 20px;
        margin-right: 20px;
        margin-bottom: 20px;
        margin-left: 20px; <!-110>
        }
        h1
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
        # TODO filter HTML in name
        html = f'<body><h1> {name} </h1> <div class="que {questionType} deferredfeedback ">'
        html += f'<div class="content"> <div class="formulation clearfix"> <div class="qtext"> {question} </div>'
        f=open(self.htmlFilename, 'a', encoding="utf-8")
        f.write(html)
        f.close()

    def addHtmlAnswerBlockMultichoice(self, choiceList):
        html = '<div class="ablock"> <div class="prompt">Выберите вариант ответа:</div> <div class="answer">'
        for item in choiceList:
            html+=f'<div class="r0"> <input type="radio" {"checked" if item==choiceList[0] else ""}/><label>' + item + '</label> </div>'
        html+='</div></div></div></div></div></body></html>'
        f=open(self.htmlFilename, 'a', encoding="utf-8")
        f.write(html)
        f.close()

    def addHtmlAnswerBlockMatch(self, pairList):
        html = '<div class="ablock"> <table class="answer"> <tbody>'
        for i in range(len(pairList)):
            item = pairList[i][0]
            html+=f'<tr class="r0"><td class="text"><p>{item}<br></p></td><td class="control"><select class="select custom-select custom-select m-l-1">'
            html+=f'<option selected="selected" value="{i}">{pairList[i][1]}</option>'
            for item2 in pairList:
                html+=f'<option>{item2[1]}</option>'
            html+='</select></td></tr>'
        html+='</tbody></table>'
        html+='</div></div></div></div></div></div></body></html>'
        f=open(self.htmlFilename, 'a', encoding="utf-8")
        f.write(html)
        f.close()

    def addHtmlAnswerBlockNumerical(self, answer):
        # TODO filter answer
        html = f'<div class="ablock"> <label>Ответ:</label> <span class="answer"><input type="text" size="30" class="form-control d-inline" /> <br><em>Правильный ответ: {answer} </em></span> </div> </div> </div> </div> </body></html>'
        f=open(self.htmlFilename, 'a', encoding="utf-8")
        f.write(html)
        f.close()

    def addHtmlAnswerBlockShortAnswer(self, answer):
        # TODO filter answer
        html = f'<div class="ablock"> <label>Ответ:</label> <span class="answer"><input type="text" size="80" class="form-control d-inline" /> <p> Правильный ответ: {answer} </span> </div> </div> </div> </div> </body></html>'
        f=open(self.htmlFilename, 'a', encoding="utf-8")
        f.write(html)
        f.close()



