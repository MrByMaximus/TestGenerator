from question import Question2
import subprocess
import random
import ctypes
import os

cmd_codepage = os.device_encoding(1) or ctypes.windll.kernel32.GetOEMCP()
os.chdir("mingw/bin")

a = random.randint(1,100)
b = random.randint(1,100)

quest1_tmp = """#include <iostream>

using namespace std;

int main() {{
    int a = {a_number};
    int b = {b_number};

    cout << "min: ";
    if (a > b)
        cout << b;
    else
        cout << a;

    return 0;
}}
"""

quest2_tmp = """#include <iostream>

using namespace std;

int main() {{
    int a = {a_number};
    int b = {b_number};

    cout << "max: ";
    if (a < b)
	    cout << b;
    else
	    cout << a;

    return 0;
}}
"""

question_prompts = [
    quest1_tmp.format(a_number=a, b_number=b), quest2_tmp.format(a_number=a, b_number=b)
]

quest = random.choice(question_prompts)

file = open(os.path.abspath('../../quest.cpp'),'w')
file.write(quest)
file.close()
os_out = "g++ {path} && a.exe"
ans = subprocess.check_output(os_out.format(path = os.path.abspath('../../quest.cpp')), shell=True, encoding=cmd_codepage)

print(quest)
print("Введите ответ программы:")

answer = input()
if answer == ans:
    print("Ответ правильный!")
else:
    print("Ответ неправильный!")