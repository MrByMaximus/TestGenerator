from random import random, randint, sample, shuffle
from sympy.core.basic import Basic
from sympy import *
import webbrowser, os
from question_creator_moodle import QuestionCreatorMoodle

'''
Quiz

In all questions, the question text accepts html code.
'''

class Quiz:
     # create a new empty Quiz in filename, and an HTML file for preview
     # default format is XML Moodle
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

    # setMainCategory
    # set the current main (parent) category (for incoming questions)
    # Example:
    # setMainCategory("Exam 2020-21")
    def setMainCategory(self, category):
        self.C.setMainCategory(category)

    # setCategory
    # set the current category (for incoming questions)
    # Example:
    # setCategory("Shadow mapping")
    def setCategory(self, category):
        self.C.setCategory(category)


    '''
        The following methods add a single question
    '''

    # addMultipleChoiceQuestion
    # add a multiple-choice, single-answer question
    # choiceList must contain exactly 4 options (the first one is the correct)
    # Example:
    # addMultipleChoiceQuestion("Mix function","Which function interpolates two values?", ["mix()", "dot()", "cross()", "distance()"])
    def addMultipleChoiceQuestion(self, name, question, choiceList):
        if isinstance(question, Basic): # sympy expr
            question = f"\({latex(question)}\)"
        if len(choiceList) > 4: # select first item + three random items
            tmp = choiceList[1:]
            shuffle(tmp)
            choiceList = [choiceList[0]] + tmp[:3]
        choiceList = [ f"\({latex(item)}\)" if isinstance(item, Basic) else item for item in choiceList]

        self.C.addMultipleChoiceQuestion(name, question, choiceList)

    # addNumericalQuestion
    # add a numerical question
    # answer can be a number or a list of numbers (all of them correct)
    # Example:
    # addNumericalQuestion("Simple sum", f"Compute {a}+{b}", a+b)
    def addNumericalQuestion(self, name, question, answer, tolerance=0.01):
        if isinstance(question, Basic): # sympy expr
            question = f"\({latex(question)}\)"
        self.C.addNumericalQuestion(name, question, answer, tolerance)

    # addMultiNumericalQuestion  (expermental!)
    # add a numerical question asking for multiple numbers (as much as len(answerList))
    # Example:
    # addMultiNumerical("Sum and product", f"Compute {a}+{b} and {a}*{b}", [a+b, a*b])
    def addMultiNumericalQuestion(self, name, question, answerList, tolerance=0.01):
        if isinstance(question, Basic): # sympy expr
            question = f"\({latex(question)}\)"
        self.C.addMultiNumericalQuestion(name, question, answerList, tolerance)

    # addShortAnswerQuestion
    # add a short-answer question; students are asked to enter a short text
    # Example:
    # addShortAnswerQuestion("About mix", "Which GLSL function is used for linear interpol?", "mix")
    def addShortAnswerQuestion(self, name, question, answer):
        if isinstance(question, Basic): # sympy expr
            question = f"\({latex(question)}\)"
        self.C.addShortAnswerQuestion(name, question, answer)


    # addMatchingQuestion
    # add a matching question
    def addMatchingQuestion(self, name, question, pairList):
        if isinstance(question, Basic): # sympy expr
            question = f"\({latex(question)}\)"
        self.C.addMatchingQuestion(name, question, pairList)


    '''
        The following methods add one or more random questions
    '''

    # addMultipleChoiceQuestions
    # add random multiple-choice, single-answer questions by choosing one correct answer
    # from correctAnswers and three distractors.
    # addMultipleChoiceQuestions("VS tasks", "Which tasks can be executed in a VS?", list_of_VS_tasks, list_of_non_VS_tasks)
    def addMultipleChoiceQuestions(self, title, question, correctAnswers, distractors, numQuestions=-1):
        distractors  = list(set(distractors)-set(correctAnswers))
        L = len(correctAnswers)
        if numQuestions == -1: # auto
            numQuestions = L
        # create up to L questions
        shuffle(correctAnswers)
        for good in correctAnswers[0:numQuestions]:
            dist = list(set(distractors)-set([good]))
            d  = sample(distractors, 3)
            self.addMultipleChoiceQuestion(title, question, [good]+d)
        # add more random questions, if needed
        for _ in range(L, numQuestions):
            good = sample(correctAnswers, 1)
            d  = sample(distractors, 3)
            self.addMultipleChoiceQuestion(title, question, good+d)


    # addMultipleChoiceQuestionsFromPairs
    # add single-answer multiple-choice questions by selecting one item from a list of (question,answer) pairs
    # The 4 choices will consist of the correct answer + 3 other (distinct) anwsers from the list and  moreDistractors.
    # questionPattern should include a '%s' that will be replaced by the specific question
    # Example:
    # addMultipleChoiceQuestionsFromPairs("Complete", "Compute the expression: %s", [ ("2+2", "4"),  ("sqrt(9)", "3")...])
    def addMultipleChoiceQuestionsFromPairs(self, title, questionPattern, solutionPairs, moreDistractors=[], numQuestions=-1):

        L = len(solutionPairs)
        if numQuestions == -1: # auto
            numQuestions = L
        if numQuestions <= L: # prevent questions sharing question text
            pairs = sample(solutionPairs, numQuestions)
        else:
            pairs = [ sample(solutionPairs, 1)[0] for _ in range(numQuestions) ]

        for pair in pairs:
            question, answer = pair[0], pair[1]

            if isinstance(question, Basic): # sympy expr
                question = f"\({latex(question)}\)"

            q = questionPattern.replace("%s", question)

            bads = [ pair[1] for pair in solutionPairs] + moreDistractors
            bads = list(set(bads))
            while answer in bads:
                bads.remove(answer)

            shuffle(bads)
            self.addMultipleChoiceQuestion(title, q, [answer] + bads[0:3])



    # addOrderingQuestions
    # select 4 random items from a sorted list to create questions asking to sort them
    # Creates matching questions where items must be assigned their rank order 1..4
    # addOrderingQuestion("Sort tasks", "Assign each task with its execution order", ["CPU", "VS", "TCS", "TES", "GS", "FS"])
    def addOrderingQuestions(self, title, question, sortedList, numQuestions=-1):
        L = len(sortedList)
        if numQuestions == -1: # auto
            numQuestions = L
        for _ in range(numQuestions):
            s = sample(range(len(sortedList)), 4)
            s.sort()
            items = [sortedList[i] for i in s]
            pairs = list(zip(items, "1234"))
            self.addMatchingQuestion(title, question, pairs)


    # addCompleteCodeQuestions
    # add multiple-choice, single-answer questions by choosing one token from the token list, and replacing
    # all its occurrences in the source code by "_____".
    # questionPattern should include a %s which will be replaced by the (incomplete) source code.
    # The 4 choices are the correct one, and 3 other (distinct) anwsers from the list + distractors.
    # Example:
    # addCompleteCodeQuestions("Complete func", "Completa la funció següent: %s", "int main()...", ["modelMatrix", "viewMatrix", ...], [normalMatrix, ...])
    def addCompleteCodeQuestions(self, title, questionPattern, sourceCode, tokens, distractors = [], numQuestions=-1):
        pairs = []
        for token in tokens:
            code = sourceCode.replace(token, "__________")
            pairs.append((code, token))
        self.addMultipleChoiceQuestionsFromPairs(title, questionPattern, pairs, distractors, numQuestions)


    # preview
    # open a web browser to preview the quiz
    def preview(self):
        webbrowser.open_new_tab(self.htmlFilename)

    # close
    # close Quiz
    def close(self):
        self.C.close()

