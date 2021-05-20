import sys, os
import random
import fileinput
import subprocess
import ast
import ctypes
import numpy
import re

class Generation(): #Генерация вопроса
    def __init__(self, path):
        super().__init__()
        self.add_quest = ''
        self.path = path
        self.path_compile = self.path+'/quest.cpp'
        self.path_output = self.path+'/quest.txt'
        self.generator = open(self.path+'/generator.conf','r', encoding="utf-8")
        self.generator = ast.literal_eval(self.generator.read())
        self.sign_for_action = self.generator['sign_for_action']
        self.fractional_number = self.generator['fractional_number']
        self.dictionary = self.generator['dictionary']

    def question_gen(self):
        path_code = self.path+'/'+self.generator['path_cods']
        if (self.generator['code'] == 0):
            code = random.choice(list(filter(lambda x: x.endswith('.txt'), os.listdir(path_code))))
        else:
            code = str(self.generator['code']) + '.txt'
        if (self.generator['type_quiz'] == 0):
            type_quiz = random.randint(1,5) #логические, синтаксические, при результате выдать ответ, стандарт вопрос, да/нет
        else:
            type_quiz = self.generator['type_quiz']

        if type_quiz == 3 and not code.replace(".txt","") in self.generator['type_quiz_exception']: #самостоятельно определять
            type_quiz = 4

        file = open(path_code+"/"+code,'r')
        quest = file.read()
        quest_out = quest
        file.close()

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

        with open(self.number_lines(self.path_output), "r") as f:
                code_out = f.read()
        
        check = subprocess.call(os_out, shell=True, stdout=os.open(os.devnull, os.O_WRONLY), stderr=subprocess.STDOUT)
        if check == 1 and type_quiz != 1 and type_quiz != 2:
            answer = code
            quiz = "[ERROR]"
        else:        
            if type_quiz == 3 and quest_out[3] == 0:
                ans_out = self.answer_true(os_out)[0][1]
                if Generation.is_float(ans_out):
                    ans_out = round(float(ans_out),self.fractional_number)
                quiz = "При каком значении "+quest_out[4]+" программа выдаст результат: "+str(ans_out)
                answer = str(quest_out[2])
            elif type_quiz == 4 or quest_out[3] == 1: #если не найдется ошибки или не выполниться 3 тип вопроса, то сгенерируется стандартный вопрос
                answers = self.answer_true(os_out)
                if type(answers) == list and len(answers) == 1:
                    quiz = "Введите ответ программы"+self.add_quest+" "+str(answers[0][0])+": "
                    answer = str(answers[0][1])
                elif type(answers) != list:
                    quiz = "Введите ответ программы"+self.add_quest+": "
                    answer = answers
                else:
                    quiz = "Сопоставьте решения: "
                    answer = answers
            elif quest_out[3] == 0 and (type_quiz == 1 or type_quiz == 2):
                quiz = "Введите номер(-а) строчки(-ек) кода, где допущена ошибка: "
                if quest_out[2] != '':
                    answer = str(quest_out[2])
                else:
                    answers = self.answer_false(os_out)
                    if len(answers) == 1:
                        answer = str(answers[0][1])
                    else:
                        answer = answers
            elif type_quiz == 5:
                chance = random.randint(1,2)
                answers = self.answer_true(os_out)
                if type(answers) == list and len(answers) > 1:
                    ans_find = random.choice(answers)
                    ans_find = ans_find[1]
                elif type(answers) != list:
                    ans_find = answers
                else:
                    ans_find = answers[0][1]
                if chance == 1:
                    answer = "yes"
                    ans_out = ans_find
                else:
                    answer = "no"
                    ans_out = self.generated_fake_answer(ans_find)
                if Generation.is_float(ans_out):
                    ans_out = round(float(ans_out),self.fractional_number)
                quiz = "После выполнении программы результат будет: "+str(ans_out)
        
        return [code_out,answer,quiz,type_quiz]

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

    def counting(self, quest, search):
        text = quest.split()
        count = 0
        for word in text:
                if word.find(search) != -1:
                    count += 1

        return count

    def noise(self, quest):
        text = quest.split()
        noise = []
        index_first = 0
        index_last = 0
        count_all_noise = self.counting(quest,"{-}")

        if count_all_noise != 0:
            for i in range(count_all_noise):
                index_first = quest.find("{-}", index_first)
                index_last = quest.find("{*}", index_first)
                if index_first != -1:
                    noise.append([])
                    count_noise = 1
                    index = index_first
                    index_last += len("{*}")
                    noise[i].append("{0}")
                    while index < index_last:
                        index = quest.find("{^}",index,index_last)
                        if index != -1:
                            quest = quest[:index] + "{"+str(count_noise)+"}" + quest[index+len("{^}"):] 
                            noise[i].append("{"+str(count_noise)+"}")
                            count_noise += 1
                        else:
                            break
                    noise[i].append("{*}")
                    num = random.randint(0,count_noise-1)
                    quest = quest[:index_first] + "{0}" + quest[index_first+len("{-}"):]
                    noise_num_first = quest.find(noise[i][num],index_first,index_last)+len(noise[i][num])
                    noise_num_last = quest.find(noise[i][num+1],index_first,index_last)
                    quest = quest[:index_first] + quest[noise_num_first:noise_num_last] + quest[index_last:]

        return quest

    def type_code_output(self, quest):
        quest_out = quest
        quest = self.noise(quest)
        quest_out = self.noise(quest)
        count_number = self.counting(quest,"{number}")
        count_action = self.counting(quest,"{action}")
        count_dictionary = self.counting(quest,"{dictionary}")
        choice = random.randint(1,2)
        check_division = 0
        out = ''
        out2 = ''
        generated_number = list(self.generator['generated_number'])
        not_error = 0

        if count_number != 0 and choice == 1:
            j = 0
            number = []
            num = random.randint(0,count_number-1)
            for i in range(count_number):
                index = quest.find("{number}")
                index2 = quest_out.find("{number}")
                quest = quest[:index+len("{number}")-1] + str(i) + quest[index+len("{number}")-1:]
                quest_out = quest_out[:index2+len("{number}")-1] + str(i) + quest_out[index2+len("{number}")-1:]
                number.append(str(random.randint(generated_number[0],generated_number[1])))
                quest = quest.replace("{number"+str(i)+"}", number[j])
                if i != num:
                    quest_out = quest_out.replace("{number"+str(i)+"}", number[j])
                else:
                    quest_out = quest_out.replace("{number"+str(i)+"}", "[number]")
                    out = number[num]
                j += 1
            if count_action != 0:
                action = []
                for i in range(count_action):
                    index = quest.find("{action}")
                    index2 = quest_out.find("{action}")
                    quest = quest[:index+len("{action}")-1] + str(i) + quest[index+len("{action}")-1:]
                    quest_out = quest_out[:index2+len("{action}")-1] + str(i) + quest_out[index2+len("{action}")-1:]
                    action.append(str(random.choice(self.sign_for_action)))
                    quest = quest.replace("{action"+str(i)+"}", action[i])
                    quest_out = quest_out.replace("{action"+str(i)+"}", action[i])
                    if action[i] == '/':
                        check_division = 1
            out2 = "[number]"
        elif count_action != 0 and choice == 2:
            j = 0
            action = []
            num = random.randint(0,count_action-1)
            for i in range(count_action):
                index = quest.find("{action}")
                index2 = quest_out.find("{action}")
                quest = quest[:index+len("{action}")-1] + str(i) + quest[index+len("{action}")-1:]
                quest_out = quest_out[:index2+len("{action}")-1] + str(i) + quest_out[index2+len("{action}")-1:]
                action.append(str(random.choice(self.sign_for_action)))
                quest = quest.replace("{action"+str(i)+"}", action[j])
                if action[i] == '/':
                    check_division = 1
                if i != num:
                    quest_out = quest_out.replace("{action"+str(i)+"}", action[j])
                else:
                    quest_out = quest_out.replace("{action"+str(i)+"}", "[action]")
                    out = action[num]
                j += 1
            if count_number != 0:
                number = []
                for i in range(count_number):
                    index = quest.find("{number}")
                    index2 = quest_out.find("{number}")
                    quest = quest[:index+len("{number}")-1] + str(i) + quest[index+len("{number}")-1:]
                    quest_out = quest_out[:index2+len("{number}")-1] + str(i) + quest_out[index2+len("{number}")-1:]
                    number.append(str(random.randint(generated_number[0],generated_number[1])))
                    quest = quest.replace("{number"+str(i)+"}", number[i])
                    quest_out = quest_out.replace("{number"+str(i)+"}", number[i])
            out2 = "[action]"
        elif count_dictionary != 0:
            dictionary_list = []
            for i in range(count_dictionary):
                index = quest.find("{dictionary}")
                quest = quest[:index+len("{dictionary}")-1] + str(i) + quest[index+len("{dictionary}")-1:]
                dictionary_list.append(random.choice(self.dictionary))
                quest = quest.replace("{dictionary"+str(i)+"}", dictionary_list[i])
            quest_out = quest
            if quest.find("{letter}") != -1:
                dictionary_list_second = dictionary_list[random.randint(0, count_dictionary-1)]
                out = random.choice(list(dictionary_list_second))
                quest = quest.replace("{letter}",out)
                count_letter = 0
                for i in dictionary_list_second: 
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

    def error_line(self, quest, error_delete, error_replace):
        count_error = self.counting(quest, error_delete)
        num_error = random.randint(1,count_error)
        quest_out = ''
        out = ''
        k = 1
        check = 0
        with open(self.path_compile, 'r') as fp:
            for n, line in enumerate(fp, 1):
                if line.find(error_delete) != -1:
                    if k == num_error:
                        check = 1
                    k += 1
                if check == 0:
                    quest_out += line
                else:
                    check = 0
                    quest_out += line.replace(error_delete,error_replace)
                    out = n
        
        return [quest_out, out]

    def num_error_count(self, count_error):
        num_error = []
        num_error_list = random.randint(1,count_error)
        num_error_count = []
        for k in range(count_error):
            num_error_count.append(k)
        random.shuffle(num_error_count)
        for k in num_error_count:
            num_error.append(k)
            num_error_list -= 1
            if num_error_list == 0:
                break
        
        return num_error

    def type_code_error(self, quest, error_choice):
        choice = random.randint(1,2)
        count_error = self.counting(quest, error_choice)
        num_error = self.num_error_count(count_error)
        index = 0

        if count_error != 0 and choice == 1: #добавление или замена      
            for i in range(count_error):
                index = quest.find(error_choice,index)
                if i in num_error:
                    quest = quest[:index] + '{replace_item}' + quest[index+len(error_choice):]
                    quest = quest.replace('{replace_item}', str(error_choice+error_choice))
                    break
                index += len(error_choice)
        elif count_error != 0 and choice == 2: #удаление
            for i in range(count_error):
                index = quest.find(error_choice,index)
                if i in num_error:
                    quest = quest[:index] + '{replace_item}' + quest[index+len(error_choice):]
                    quest = quest.replace('{replace_item}', '')
                    break
                index += len(error_choice)

        return quest

    def type_code_logic(self, quest):
        choice = random.randint(1,3)
        quest_out = ''
        out = ''
        out_error = []
        not_error = 0
        error_choice = random.choice(self.generator['error'])

        if choice == 1 and (quest.find("int result") != -1 or quest.find("float result") != -1) and (quest.find("int func") != -1 or quest.find("float func") != -1): #удаляет return result
            index = quest.find("return result;")
            quest = quest[:index-3] + quest[index+15:]
        elif quest.find("==") != -1 and choice == 2: #a == b
            error_request = self.error_line(quest,"==","=")
            quest_out = error_request[0]
            out = error_request[1]
        elif quest.find(error_choice) != -1 and choice == 3:
            quest = self.type_code_error(quest, error_choice)
        else:
            not_error = 1

        if choice != 2:
            quest_out = quest

        return [quest,quest_out,out,not_error]

    def type_code_syntax(self, quest):
        choice = random.randint(1,7)
        quest_out = ''
        out = ''
        out_error = []
        not_error = 0
        error_choice = random.choice(self.generator['error'])

        if (quest.find("int func") != -1 or quest.find("float func") != -1) and choice == 1:
            count_func = self.counting(quest, "func")
            func_check = []
            index_prev = 0           
            for i in range(count_func):
                index_next = quest.find("func",index_prev)
                if index_next == (quest.find("int func")+4) or index_next == (quest.find("float func")+6):
                    func_check.append(i)
                index_prev = index_next+5
                index_next = quest.find(")",index_prev)
                if not i in func_check:
                    choice_func = random.randint(1,2)
                    choice_func = 2
                    if choice_func == 1:
                        quest = quest[:index_prev] + '{replace_item}' + quest[index_next:]
                        quest = quest.replace('{replace_item}', '')
                    else: #не работает нормально
                        num_delete = random.randrange(index_prev+2,index_next,2)
                        num_delete = index_prev+4
                        quest = quest[:index_prev] + quest[index_prev:num_delete-2] + quest[num_delete:index_next] + quest[index_next:]
        elif quest.find("void func") != -1 and choice == 1: #добавить result в функцию void
            index = quest.find("}\nint main")
            quest = quest[:index] + "return result;\n" + quest[index:]
            quest_out = quest
        elif quest.find("using namespace std;") != -1 and quest.find("cout") != -1 and choice == 2: #если есть using namespace std;
            count_cout = self.counting(quest, "cout")
            for i in range(count_cout):
                index = quest.find(type_choice,index)
                if i == num_error:
                    quest = quest[:index] + '{replace_item}' + quest[index+len(error_choice):]
                    quest = quest.replace('{replace_item}', 'std::cout')
                    break
        elif (quest.find("int") != -1 or quest.find("float") != -1 or quest.find("double") != -1) and choice == 3: #int, float, double на некоторых не выводит ошибку
            num_check = []
            error_replace_type = ['char','bool','string']
            if quest.find("float") != -1:
                type_id = 'float'
            elif quest.find("double") != -1:
                type_id = 'double'
            elif quest.find("int") != -1:
                type_id = 'int'
            count_error = self.counting(quest, type_id)
            num_error = self.num_error_count(count_error)
            index = 0
            for i in range(count_error):
                index = quest.find(type_id,index)
                if index == quest.find("int main") and type_id == 'int':
                    num_check.append(i)
                if (index == quest.find("int func") and type_id == 'int') or (index == quest.find("float func") and type_id == 'float') or (index == quest.find("double func") and type_id == 'double'):
                    num_check.append(i)
                if i in num_error and not num_error in num_check:
                    quest = quest[:index] + '{replace_item}' + quest[index+len(type_id):]
                    choice_type = random.randint(1,3)
                    if choice_type == 1:
                        quest = quest.replace('{replace_item}', '')
                        break
                    elif choice_type == 2:
                        quest = quest.replace('{replace_item}', str(random.choice(self.generator['generated_number']))+type_id)
                        break
                    else:
                        quest = quest.replace('{replace_item}', str(random.choice(error_replace_type)))
                        break
                index += len(type_id)
        elif quest.find("result") != -1 and choice == 4: #вставить const
            if quest.find("int result") != -1:
                quest = quest.replace("int result", "const int result")
            elif quest.find("float result") != -1:
                quest = quest.replace("float result", "const float result")
        elif (quest.find("char str[]") != -1 or quest.find("string str") != -1) and choice == 5: #string и char
            if quest.find("char str[]") != -1:
                quest = quest.replace("char str[]","char *str[]")
            if quest.find("string str") != -1:
                quest = quest.replace("string str","string *str")
        elif quest.find(";") != -1 and choice == 6: #; удалять
            error_request = self.error_line(quest,";","")
            quest_out = error_request[0]
            out = error_request[1]
        elif quest.find(error_choice) != -1 and choice == 7:
            quest = self.type_code_error(quest, error_choice)
        else:
            not_error = 1

        if choice != 6:
            quest_out = quest

        return [quest,quest_out,out,not_error]

    def read_code(self, quest):
        quest = self.noise(quest)
        count_number = self.counting(quest,"{number}")
        count_action = self.counting(quest,"{action}")
        count_dictionary = self.counting(quest,"{dictionary}")
        check_division = 0
        index = 0

        if count_number != 0: #генерация чисел
            generated_number = list(self.generator['generated_number'])
            for i in range(count_number):
                index = quest.find("{number}")
                quest = quest[:index+len("{number}")-1] + str(i) + quest[index+len("{number}")-1:]
                quest = quest.replace("{number"+str(i)+"}", str(random.randint(generated_number[0],generated_number[1])))  
        if count_action != 0: #генерация вычислений
            action = []
            for i in range(count_action):
                index = quest.find("{action}")
                action.append(str(random.choice(self.sign_for_action)))
                if action[i] == '/':
                    check_division = 1
                quest = quest[:index+len("{action}")-1] + str(i) + quest[index+len("{action}")-1:]
                quest = quest.replace("{action"+str(i)+"}", action[i])
            if check_division == 1:
                self.add_quest = " (Округлите до "+str(1 / (10 ** self.fractional_number))+")"
                quest = quest.replace("int","float")
                quest = quest.replace("float main","int main")        
        if count_dictionary != 0: #словарь слов
            dictionary_list = []
            for i in range(count_dictionary):
                index = quest.find("{dictionary}")
                quest = quest[:index+len("{dictionary}")-1] + str(i) + quest[index+len("{dictionary}")-1:]
                dictionary_list.append(random.choice(self.dictionary))
                quest = quest.replace("{dictionary"+str(i)+"}", self.dictionary[i])
            if quest.find("{letter}") != -1:
                letter = list(dictionary_list[random.randint(0, count_dictionary-1)])
                quest = quest.replace("{letter}",random.choice(letter))
        if quest.find("<fstream>") != -1:
            path_files = self.path+'/'+self.generator['files']
            file = open(path_files+"/in.txt",'w', encoding="utf-8")
            if quest.find("count") != -1:
                number_of_generated_numbers = self.generator['number_of_generated_numbers']
                generated_number = list(self.generator['generated_number'])
                numbers = ''
                for i in range(number_of_generated_numbers):
                    numbers += str(random.randint(generated_number[0], generated_number[1]))
                    if i != number_of_generated_numbers-1:
                        numbers += ' '
                file.write(numbers)
            elif quest.find("line") != -1:
                line = random.choice(self.dictionary)
                file.write(line)
            file.close()
            
        return quest

    def generated_fake_answer(self, answer):
        answer_out = ''
        if answer in self.sign_for_action:
            list_sign = []
            for num in self.sign_for_action:
                if num != answer:
                    list_sign.append(str(num))
            answer_out = random.choice(list_sign)
        elif Generation.is_number(str(answer)):
            if Generation.is_float(str(answer)):
                fractional_number_answer = list(self.generator['fractional_number_answer'])
                answer = round(float(answer),self.fractional_number)
                number = answer
                list_numbers = list(numpy.arange(number-fractional_number_answer[0], number+fractional_number_answer[1], 1 / (10 ** self.fractional_number)))
                list_numbers = [round(v,self.fractional_number) for v in list_numbers]
            else:
                number_answer = list(self.generator['number_answer'])
                number = int(answer)
                list_numbers = list(range(number-number_answer[0], number+number_answer[1]))
            list_number = []
            for num in list_numbers:
                if num != number:
                    list_number.append(str(num))
            answer_out = random.choice(list_number)
        elif answer in self.dictionary:
            list_dictionary = []
            for num in self.dictionary:
                if num != answer:
                    list_dictionary.append(str(num))
            answer_out = random.choice(list_dictionary)
        self.add_quest = " ("+answer_out+")"

        return answer_out

    def write_code_output(self, quest):
        file = open(self.path_output,'w', encoding="utf-8")
        file.write(quest)
        file.close()

    def write_code(self, quest):
        file = open(self.path_compile,'w', encoding="utf-8")
        file.write(quest)
        file.close()
        return "g++ " + self.path + "/quest.cpp -o " + self.path + "/quest"

    def delete_file(self):
        os.remove(os.path.join(self.path_compile))
        os.remove(os.path.join(self.path_output))
        if os.path.exists(self.path+"/quest.exe"):
            os.remove(os.path.join("quest.exe"))
        if os.path.exists(self.path+"/quest"):
            os.remove(os.path.join("quest"))

    def answer_true(self, os_out):
        os_out += " && " + self.path + "/quest"
        answer = subprocess.check_output(os_out, shell=True, encoding="utf-8", stderr=subprocess.STDOUT) #shell чувствителен к пути, исправить
        count_ans = self.counting(answer,":")
        answers = []
        if count_ans == 0:
            answers = str(answer).replace('\n','')
        else:
            index_first = 0
            index_middle = 0
            for i in range(count_ans):
                index_first = answer.find(':',index_first)
                index_last = answer.find('\n',index_first)
                if index_first != -1:
                    answers.append([])
                    answers[i].append(str(answer[index_middle:index_first]))
                    answers[i].append(str(answer[index_first+2:index_last]).replace('\n',''))
                    index_first += 2
                    index_middle = index_last+1

        return answers

    def answer_false(self, os_out):
        process = subprocess.Popen(os_out, shell=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        tmp = process.stdout.read()
        tmp = tmp.replace(self.path+"/quest.cpp:","")
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
        count_ans = self.counting(tmp,"error:") + self.counting(tmp,"warning:") + self.counting(tmp,"note:")
        answers = []
        index_first = 0
        for i in range(count_ans):
            index_first = tmp.find("error:",index_first)
            if index_first == -1:
                index_first = tmp.find("warning:",index_first)
            if index_first == -1:
                index_first = tmp.find("note:",index_first)
            index_second = tmp.find("\n",index_first)
            index_last = tmp.find("|",index_second)
            answer = tmp[index_second+1:index_last]
            answer = re.findall('(\d+)',answer)
            if answer != []:
                answers.append([])
                answers[i].append(str(tmp[index_last+2:tmp.find("\n",index_last)]))
                answers[i].append(str(answer[0]))
                index_first = tmp.find("\n",index_last)

        return answers

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