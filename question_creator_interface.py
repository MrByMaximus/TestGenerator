from abc import ABC, abstractmethod

'''
QuestionCreatorInterface - Minimalist interface for creating questions (abstract class)
'''
class QuestionCreatorInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def open(self, filename, previewFilename):
        pass

    @abstractmethod
    def setMainCategory(self, mainCategory):
        pass

    @abstractmethod
    def setCategory(self, category):
        pass

    @abstractmethod
    def addMultipleChoiceQuestion(self, name, question, choiceList):
        pass

    @abstractmethod
    def addNumericalQuestion(self, name, question, answer, tolerance=0.01):
        pass

    @abstractmethod
    def addMultiNumericalQuestion(self, name, question, answerList, tolerance=0.01):
        pass

    @abstractmethod
    def addShortAnswerQuestion(self, name, question, answer):
        pass

    @abstractmethod
    def addMatchingQuestion(self, name, question, pairList):
        pass

    @abstractmethod
    def close(self):
        pass
