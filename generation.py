import sys, os
import random
import fileinput
import subprocess
import ast
import ctypes
import numpy

path = os.getcwd()
path_compile = path+'/quest.cpp'
path_output = path+'/quest.txt'
path_xml = path+'/quest_xml.txt'
generator = open(path+'/generator.conf','r', encoding="utf-8")
generator = ast.literal_eval(generator.read())
sign_for_action = generator['sign_for_action']
fractional_number = generator['fractional_number']
dictionary = generator['dictionary']
cmd_codepage = os.device_encoding(1) or ctypes.windll.kernel32.GetOEMCP()

class Generation(): #Генерация вопроса
    def __init__(self):
        super().__init__()

    def question_gen(self):
        DEVNULL = os.open(os.devnull, os.O_WRONLY)
        path_code = path+'/cods'
        code = random.choice(list(filter(lambda x: x.endswith('.txt'), os.listdir(path_code))))
        type_quiz = random.randint(1,5) #логические, синтаксические, при результате выдать ответ, стандарт вопрос
        type_quiz = 5
        #code = 'code_2.txt'

        if type_quiz == 3 and not code.replace(".txt","") in generator['type_quiz_exception']:
            type_quiz = 4

        file = open(path_code+"/"+code,'r')
        quest = file.read()
        quest_out = quest

        if type_quiz == 1 or type_quiz == 2:
            quest = self.read_code(quest)
            self.write_code(quest)

        if type_quiz == 1: #логический     
            quest_out = self.type_code_logic(quest)
        elif type_quiz == 2: #синтаксический       
            quest_out = self.type_code_syntax(quest) #0-quest,1-quest_output,2-answer,3-answer_error,4-not_error
        elif type_quiz == 3: #выходной ответ
            quest_out = self.type_code_output(quest) #0-quest,1-quest_output,2-answer,3-additional_out
            
        if type_quiz == 4 or type_quiz == 5: #входной ответ
            quest = self.read_code(quest)
            self.write_code_output(quest)
            os_out = self.write_code(quest)
        else:
            self.write_code_output(quest_out[1])
            os_out = self.write_code(quest_out[0])

        file.close()
        with open(self.number_lines(path_output), "r") as f:
            text = f.read()

        #check = subprocess.call(os_out, shell=True, stdout=DEVNULL, stderr=subprocess.STDOUT)
        if type_quiz == 3 and quest_out[3] == 0:
            ans_out = self.answer_true(os_out)
            if Generation.is_float(ans_out):
                ans_out = round(float(ans_out),fractional_number)
            quiz = "При каком значении "+quest_out[4]+" программа выдаст результат: "+str(ans_out)
            ans = quest_out[2]
        elif type_quiz == 4 or quest_out[3] == 1: #если не найдется ошибки или не выполниться 3 тип вопроса, то сгенерируется стандартный вопрос
            quiz = "Введите ответ программы:"
            ans = self.answer_true(os_out)
        elif quest_out[3] == 0 and (type_quiz == 1 or type_quiz == 2):
            quiz = "Введите строчку кода, где допущена ошибка:"
            if quest_out[2] != '':
                ans = quest_out[2]
            else:
                ans = self.answer_false(os_out)
        elif type_quiz == 5:
            chance = random.randint(1,2)
            ans_find = self.answer_true(os_out)
            if chance == 1:
                ans = "yes"
                ans_out = ans_find
            else:
                ans = "no"
                ans_out = self.generated_fake_answer(ans_find)
            if Generation.is_float(ans_out):
                ans_out = round(float(ans_out),fractional_number)
            quiz = "При компиляции программы результат будет: "+str(ans_out)
        
        return [text,str(ans),quiz,type_quiz]

    def is_float(str):
        try:
            float(str)
            if str.find('.') != -1 and str.count('.') == 1:
                return True
            else:
                raise ValueError
        except ValueError:
            return False

    def is_number(str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    def count_elements(self, quest): #продумать без нумерации
        text = quest.split()
        count_number = 0
        count_action = 0
        count_dictionary = 0

        for word in text:
            if word.find("{number}") != -1:
                count_number+=1
            if word.find("{action}") != -1:
                count_action += 1
            if word.find("{dictionary}") != -1:
                count_dictionary += 1

        return [count_number, count_action, count_dictionary]

    def counting(self, quest, search):
        text = quest.split()
        count = 0
        for word in text:
                if word.find(search) != -1:
                    count += 1
        return count

    def noise(self, quest):
        count_noise = 0
        text = quest.split()
        noise = []

        for word in text:
            if word.find("{^"+str(count_noise)+"^}") != -1:
                noise.append("{^"+str(count_noise)+"^}")
                count_noise+=1

        if count_noise != 0:
            noise.append("{^-^}")
            num = random.randint(0,count_noise-1)
            noise_num1 = quest.find(noise[num])
            first = quest.find(noise[0])
            end = quest.find(noise[count_noise])
            noise_num2 = quest.find(noise[num+1])
            quest_out = quest[noise_num1+5:noise_num2]
            quest = quest[:first] + quest[end:]
            quest = quest.replace("{^-^}", quest_out)

        return quest

    def type_code_output(self, quest):
        quest_out = quest
        quest = self.noise(quest)
        quest_out = self.noise(quest)
        count = self.count_elements(quest)
        choice = random.randint(1,2)
        check_division = 0
        out = ''
        out2 = ''
        generated_number = list(generator['generated_number'])
        not_error = 0

        if count[0] != 0 and choice == 1:
            j = 0
            number = []
            num = random.randint(0,count[0]-1)
            for i in range(count[0]):
                index = quest.find("{number}")
                index2 = quest_out.find("{number}")
                quest = quest[:index+7] + str(i) + quest[index+7:]
                quest_out = quest_out[:index2+7] + str(i) + quest_out[index2+7:]
                number.append(str(random.randint(generated_number[0],generated_number[1])))
                quest = quest.replace("{number"+str(i)+"}", number[j])
                if i != num:
                    quest_out = quest_out.replace("{number"+str(i)+"}", number[j])
                else:
                    quest_out = quest_out.replace("{number"+str(i)+"}", "[number]")
                    out = number[num]
                j += 1
            if count[1] != 0:
                action = []
                for i in range(count[1]):
                    index = quest.find("{action}")
                    index2 = quest_out.find("{action}")
                    quest = quest[:index+7] + str(i) + quest[index+7:]
                    quest_out = quest_out[:index2+7] + str(i) + quest_out[index2+7:]
                    action.append(str(random.choice(sign_for_action)))
                    quest = quest.replace("{action"+str(i)+"}", action[i])
                    quest_out = quest_out.replace("{action"+str(i)+"}", action[i])
                    if action[i] == '/':
                        check_division = 1
            out2 = "[number]"
        elif count[1] != 0 and choice == 2:
            j = 0
            action = []
            num = random.randint(0,count[1]-1)
            for i in range(count[1]):
                index = quest.find("{action}")
                index2 = quest_out.find("{action}")
                quest = quest[:index+7] + str(i) + quest[index+7:]
                quest_out = quest_out[:index2+7] + str(i) + quest_out[index2+7:]
                action.append(str(random.choice(sign_for_action)))
                quest = quest.replace("{action"+str(i)+"}", action[j])
                if action[i] == '/':
                    check_division = 1
                if i != num:
                    quest_out = quest_out.replace("{action"+str(i)+"}", action[j])
                else:
                    quest_out = quest_out.replace("{action"+str(i)+"}", "[action]")
                    out = action[num]
                j += 1
            if count[0] != 0:
                number = []
                for i in range(count[0]):
                    index = quest.find("{number}")
                    index2 = quest_out.find("{number}")
                    quest = quest[:index+7] + str(i) + quest[index+7:]
                    quest_out = quest_out[:index2+7] + str(i) + quest_out[index2+7:]
                    number.append(str(random.randint(generated_number[0],generated_number[1])))
                    quest = quest.replace("{number"+str(i)+"}", number[i])
                    quest_out = quest_out.replace("{number"+str(i)+"}", number[i])
            out2 = "[action]"
        elif count[2] != 0:
            dictionary = []
            for i in range(count[2]):
                index = quest.find("{dictionary}")
                quest = quest[:index+11] + str(i) + quest[index+11:]
                dictionary.append(random.choice(dictionary))
                quest = quest.replace("{dictionary"+str(i)+"}", dictionary[i])
            quest_out = quest
            if quest.find("{letter}") != -1:
                dictionary2 = dictionary[random.randint(0, count[2]-1)]
                out = random.choice(list(dictionary2))
                quest = quest.replace("{letter}",out)
                count_letter = 0
                for i in dictionary2: 
                    if i == out: 
                        count_letter += 1
                if count_letter == 1:
                    quest_out = quest
                    not_error = 1
                else:               
                    quest_out = quest_out.replace("{letter}","[letter]")
                    out2 = "[letter]"
            else:
                not_error = 1
        else:
            not_error = 1

        if check_division == 1:
            quest = quest.replace("int","float")
            quest = quest.replace("float main","int main")
            quest_out = quest_out.replace("int","float")
            quest_out = quest_out.replace("float main","int main")

        return [quest,quest_out,out,not_error,out2] #Сделать проверку на единественный верный ответ, если при вычислениях будут 1 и больше вариантов

    def type_code_error(self, quest, error_choice):
        text = quest.split()
        choice = random.randint(1,2)
        choice = 2
        count_error = self.counting(quest, error_choice)
        index = 0
        error_syntax = list(generator['error_syntax'])
        num_error = random.randint(0,count_error-1)

        if count_error != 0 and error_choice == error_syntax[0] and choice == 1: #int
            num_check = []
            for i in range(count_error):
                index = quest.find(error_choice,index)
                if index == quest.find("int main"):
                    num_check.append(i)
                if index == quest.find("int func") or index == quest.find("float func"):
                    num_check.append(i)
                if i == num_error and not num_error in num_check:
                    quest = quest[:index] + '{replace_item}' + quest[index+len(error_choice):]
                    choice_int = random.randint(1,3)
                    if choice_int == 1:
                        quest = quest.replace('{replace_item}', '')
                        break
                    elif choice_int == 2:
                        quest = quest.replace('{replace_item}', str(random.choice(generator['generated_number']))+'int')
                        break
                    else:
                        quest = quest.replace('{replace_item}', str(random.choice(generator['error_replace'][0]))+' ')
                        break
        elif count_error != 0 and choice == 2 and error_choice != error_syntax[0]: #добавление или замена
            #error_replace = list(generator['error_replace'])
            error_syntax.remove('int')            
            for i in range(count_error):
                index = quest.find(error_choice,index)
                if i == num_error:
                    quest = quest[:index] + '{replace_item}' + quest[index+len(error_choice):]
                    quest = quest.replace('{replace_item}', str(error_choice+error_choice))
                    break
        else: #удаление
            for i in range(count_error):
                index = quest.find(error_choice,index)
                if i == num_error:
                    quest = quest[:index] + '{replace_item}' + quest[index+len(error_choice):]
                    quest = quest.replace('{replace_item}', '')
                    break

        return quest

    def type_code_logic(self, quest):
        choice = random.randint(1,2)
        quest_out = quest
        #choice = 1
        out = ''
        out_error = []
        not_error = 0
        error_choice = random.choice(generator['error_logic'])

        if choice == 1 and (quest.find("int result") != -1 or quest.find("float result") != -1) and (quest.find("int func") != -1 or quest.find("float func") != -1): #удаляет return result
            index = quest.find("return result;")
            quest = quest[:index-3] + quest[index+15:]
            quest_out = quest
        elif quest.find(error_choice) != -1 and choice == 2:
            quest = self.type_code_error(quest, error_choice)
            quest_out = quest
        else:
            not_error = 1
            quest_out = quest

        return [quest,quest_out,out,not_error]
 #сопоставление пунктов списка

    def type_code_syntax(self, quest): #; не работает - не выводит ошибку вообще
        choice = random.randint(1,5)
        choice = 6
        quest_out = quest
        out = ''
        out_error = []
        not_error = 0
        error_choice = random.choice(generator['error_syntax'])

        if (quest.find("int func") != -1 or quest.find("float func") != -1) and choice == 1: #не работает
            count_func = self.counting(quest, "func")
            func_check = []
            index_prev = 0           
            for i in range(count_func):
                index_next = quest.find("func",index_prev)
                if index_next == (quest.find("int func")+4) or index_next == (quest.find("float func")+7):
                    func_check.append(i)
                index_prev = index_next+5
                index_next = quest.find(")",index_prev)
                if not i in func_check:
                    choice_func = random.randint(1,2)
                    if choice_func == 1:
                        quest = quest[:index_prev] + '{replace_item}' + quest[index_next:]
                        quest = quest.replace('{replace_item}', '')
                    else:
                        num_delete = random.randrange(index_prev+2,index_next,2)
                        quest = quest[:index_prev] + quest[index_prev:num_delete-2] + quest[num_delete:index_next] + quest[index_next:]
            quest_out = quest
        elif quest.find("void func") != -1 and choice == 2: #добавить result в функцию void
            index = quest.find("}\nint main")
            quest = quest[:index-1] + "\n    return result;\n" + quest[index:]
            quest_out = quest
        elif quest.find("==") != -1 and choice == 3:
            with open(path_compile, 'r') as fp:
                for n, line in enumerate(fp, 1):
                    if line.find("==") != -1:
                        quest_out = quest.replace("==","=")
                        out = n - 1
        elif quest.find("result") != -1 and choice == 4: #вставить const
            if quest.find("int result") != -1:
                quest = quest.replace("int result", "const int result")
            elif quest.find("float result") != -1:
                quest = quest.replace("float result", "const float result")
            quest_out = quest
        elif (quest.find("char str[]") != -1 or quest.find("string str") != -1) and choice == 5:
            if quest.find("char str[]") != -1:
                quest = quest.replace("char str[]","char *str[]")
            if quest.find("string str") != -1:
                quest = quest.replace("string str","string *str")
            quest_out = quest
        elif quest.find(error_choice) != -1 and choice == 6:
            quest = self.type_code_error(quest, error_choice)
            quest_out = quest
        else:
            not_error = 1
            quest_out = quest

        return [quest,quest_out,out,not_error]

    def read_code(self, quest):
        quest = self.noise(quest)
        count = self.count_elements(quest)
        check_division = 0
        index = 0

        if count[0] != 0: #генерация чисел
            generated_number = list(generator['generated_number'])
            for i in range(count[0]):
                index = quest.find("{number}")
                quest = quest[:index+7] + str(i) + quest[index+7:]
                quest = quest.replace("{number"+str(i)+"}", str(random.randint(generated_number[0],generated_number[1])))  
        if count[1] != 0: #генерация вычислений
            action = []
            for i in range(count[1]):
                index = quest.find("{action}")
                action.append(str(random.choice(sign_for_action)))
                if action[i] == '/':
                    check_division = 1
                quest = quest[:index+7] + str(i) + quest[index+7:]
                quest = quest.replace("{action"+str(i)+"}", action[i])
            if check_division == 1:
                quest = quest.replace("int","float")
                quest = quest.replace("float main","int main")        
        if count[2] != 0: #словарь слов
            dictionary = []
            for i in range(count[2]):
                index = quest.find("{dictionary}")
                quest = quest[:index+11] + str(i) + quest[index+11:]
                dictionary.append(random.choice(dictionary))
                quest = quest.replace("{dictionary"+str(i)+"}", dictionary[i])
            if quest.find("{letter}") != -1:
                letter = list(dictionary[random.randint(0, count[2]-1)])
                quest = quest.replace("{letter}",random.choice(letter))
        if quest.find("<fstream>") != -1:
            path_files = path+'/files'
            file = open(path_files+"/in.txt",'w', encoding="utf-8")
            if quest.find("count"):
                generated_number = list(generator['generated_number'])
                numbers = ''
                for i in range(generator['number_of_generated_numbers']):
                    numbers += str(random.randint(generated_number[0], generated_number[1]))
                    if i != generator['number_of_generated_numbers']-1:
                        numbers += ' '
                print(numbers)
                file.write(numbers)
            elif quest.find("line"):
                line = random.choice(dictionary)
                print(line)
                file.write(line)
            file.close()
            
        return quest

    def generated_fake_answer(self, answer):
        print("Правильный ответ: "+str(answer))
        answer_out = ''
        if answer in sign_for_action:
            list_sign = []
            for num in sign_for_action:
                if num != answer:
                    list_sign.append(str(num))
            answer_out = random.choice(list_sign)
        elif Generation.is_number(answer):
            if Generation.is_float(answer):
                fractional_number_answer = list(generator['fractional_number_answer'])
                answer = round(float(answer),fractional_number)
                number = answer
                list_numbers = list(numpy.arange(number-fractional_number_answer[0], number+fractional_number_answer[1], 1 / (10 ** fractional_number)))
                list_numbers = [round(v,fractional_number) for v in list_numbers]
            else:
                number_answer = list(generator['number_answer'])
                number = int(answer)
                list_numbers = list(range(number-number_answer[0], number+number_answer[1]))
            list_number = []
            for num in list_numbers:
                if num != number:
                    list_number.append(str(num))
            answer_out = random.choice(list_number)
        elif answer in dictionary:
            list_dictionary = []
            for num in dictionary:
                if num != answer:
                    list_dictionary.append(str(num))
            answer_out = random.choice(list_dictionary)
        
        return answer_out

    def write_code_output(self, quest):
        file1 = open(path_output,'w', encoding="utf-8")
        file1.write(quest)
        file1.close()
        file2 = open(path_xml,'w', encoding="utf-8")
        file2.write(quest)
        file2.close()

    def write_code(self, quest):
        file = open(path_compile,'w', encoding="utf-8")
        file.write(quest)
        file.close()
        if sys.platform == "linux" or sys.platform == "linux2":
            return "g++ " + path + "/quest.cpp -o " + path + "/quest"
        else:
            return "g++ " + path + "\quest.cpp -o " + path + "\quest"

    def delete_file(self):
        os.remove(os.path.join(path_compile))
        os.remove(os.path.join(path_output))
        os.remove(os.path.join(path_xml))
        if os.path.exists(path+"/quest.exe"):
            os.remove(os.path.join("quest.exe")) #Надо еще для linux
        if os.path.exists(path+"/quest"):
            os.remove(os.path.join("quest")) #Надо еще для linux

    def answer_true(self, os_out):
        if sys.platform == "linux" or sys.platform == "linux2":
            os_out += " && " + path + "/quest" #Проверить в linux
        else:
            os_out += " && " + path + "\quest"
        ans = subprocess.check_output(os_out, shell=True, encoding=cmd_codepage, stderr=subprocess.STDOUT)
        index = ans.find(":")
        if index != -1:
            ans = ans[index+2:]

        return ans

    def answer_false(self, os_out):
        process = subprocess.Popen(os_out, shell=True, stdout=subprocess.PIPE, encoding=cmd_codepage, stderr=subprocess.STDOUT)
        tmp = process.stdout.read()
        #print(tmp)
        tmp = tmp.replace(path+"\quest.cpp:","")
        tmp = tmp.replace(" In function 'int main()':\n","")
        index = tmp.find(" In function 'int func")
        if index != -1:
            tmp = self.delete_error_code(tmp,index)
        index = tmp.find(" In function 'float func")
        if index != -1:
            tmp = self.delete_error_code(tmp,index)
        index = tmp.find(" In function 'void func")
        if index != -1:
            tmp = self.delete_error_code(tmp,index)
        ans = ''
        index = tmp.find(":")
        for i in range(index):
            ans += ''.join(tmp[i])

        return ans

    def delete_error_code(self, tmp, index):
        index2 = tmp.find(":\n",index)
        tmp = tmp[:index] + tmp[index2+3:]
        
        return tmp

    def number_lines(self, filename, start=1):
        with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
            for n, line in enumerate(file, start=start):
                print(n, '    ', line, end='')
        os.unlink(filename + '.bak')
        return filename