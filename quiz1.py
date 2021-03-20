# Sample script for fill-in-the-blanks questions
from quizgen import *

Q = Quiz('output/listing.xml')
# Add fill-in-the-blanks questions
code = """
    #include <iostream>
 
    int main() {
        std::cout << "I love coding!" << endl;
 
        return 0;
    }
"""
tokens = ['std::', 'return 0;', "#include <iostream>"]
distractors = ['std:', 'return ;', '#include <cstring>']
Q.addCompleteCodeQuestions("", "Завершите программный код: <p> <pre>%s</pre>", code, tokens, distractors)
Q.preview()
Q.close()
