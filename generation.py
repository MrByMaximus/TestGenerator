import sys, os
import random
import fileinput
import subprocess
import ast

path = os.getcwd()
path_compile = path+'/quest.cpp'
path_output = path+'/quest.txt'
path_xml = path+'/quest_xml.txt'
generator = open(path+'/generator.conf','r', encoding="utf-8")
generator = ast.literal_eval(generator.read())
cmd_codepage = os.device_encoding(1) or ctypes.windll.kernel32.GetOEMCP()

class Generation(): #Генерация вопроса
    def __init__(self):
        super().__init__()

    def question_gen(self):
        DEVNULL = os.open(os.devnull, os.O_WRONLY)
        path_code = path+'/cods'
        code = random.randint(1,len(os.listdir(path_code)))
        type_quiz = random.randint(1,4)
        #type_quiz = 3
        #code = 2
        out_error = [] #заглушка
        type_error = 0

        code_error_for_type_quiz = [1,3,4]
        if type_quiz == 3 and code in code_error_for_type_quiz:
            type_quiz = 4

        file = open(path_code+"/"+str(code)+".txt",'r')
        quest = file.read()

        if type_quiz == 1 or type_quiz == 2:
            quest = self.read_code(quest)
            self.write_code(quest)

        if type_quiz == 1: #логический     
            quest2 = self.type_code_logic(quest)
        elif type_quiz == 2: #синтаксический       
            quest2 = self.type_code_syntax(quest) #0-quest,1-quest_output,2-answer,3-answer_error,4-not_error
        elif type_quiz == 3: #выходной ответ
            quest2 = self.type_code_output(quest) #0-quest,1-quest_output,2-answer,3-additional_out
            
        if type_quiz == 4: #входной ответ
            quest = self.read_code(quest)
            self.write_code_output(quest)
            os_out = self.write_code(quest)
        else:
            self.write_code_output(quest2[1])
            os_out = self.write_code(quest2[0])
        
        file.close()
        with open(self.number_lines(path_output), "r") as f:
            text = f.read()

        #check = subprocess.call(os_out, shell=True, stdout=DEVNULL, stderr=subprocess.STDOUT)
        if type_quiz == 3:
            ans2 = self.answer_true(os_out)
            if self.is_number(ans2):
                ans2 = round(float(ans2),generator['fractional_number'])
            quiz = "При каком значении "+quest2[3]+" программа выдаст результат: "+str(ans2)
            ans = quest2[2]
        elif type_quiz == 4 or quest2[4] == 1:
            quiz = "Введите ответ программы:"
            ans = self.answer_true(os_out)
        else:
            quiz = "Введите строчку кода, где допущена ошибка:"
            if quest2[3]:
                out_error = list(quest2[3])
                type_error = 1 #определиться посылать ли единчные варианты или просто тип вопроса - разницы по сути нет
            if quest2[2] != '':
                ans = quest2[2]
            else:
                ans = self.answer_false(os_out)

        return [text,ans,quiz,type_error,out_error]

    def is_number(self, str):
        try:
            float(str)
            if str.find('.') != -1 and str.count('.') == 1:
                return True
            else:
                raise ValueError
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
            quest2 = quest[noise_num1+5:noise_num2]
            quest = quest[:first] + quest[end:]
            quest = quest.replace("{^-^}", quest2)

        return quest

    def type_code_output(self, quest):
        quest2 = quest
        quest = self.noise(quest)
        quest2 = self.noise(quest)
        count = self.count_elements(quest)
        choice = random.randint(1,2)
        check_division = 0
        out = ''
        generated_number = list(generator['generated_number'])

        if choice == 1:
            if count[0] != 0:
                j = 0
                number = []
                num = random.randint(0,count[0]-1)
                for i in range(count[0]):
                    index = quest.find("{number}")
                    index2 = quest2.find("{number}")
                    quest = quest[:index+7] + str(i) + quest[index+7:]
                    quest2 = quest2[:index2+7] + str(i) + quest2[index2+7:]
                    number.append(str(random.randint(generated_number[0],generated_number[1])))
                    quest = quest.replace("{number"+str(i)+"}", number[j])
                    if i != num:
                        quest2 = quest2.replace("{number"+str(i)+"}", number[j])
                    else:
                        quest2 = quest2.replace("{number"+str(i)+"}", "[number]")
                        out = number[num]
                    j += 1
            if count[1] != 0:
                action = []
                for i in range(count[1]):
                    index = quest.find("{action}")
                    index2 = quest2.find("{action}")
                    quest = quest[:index+7] + str(i) + quest[index+7:]
                    quest2 = quest2[:index2+7] + str(i) + quest2[index2+7:]
                    action.append(str(random.choice(generator['sign_for_action'])))
                    quest = quest.replace("{action"+str(i)+"}", action[i])
                    quest2 = quest2.replace("{action"+str(i)+"}", action[i])
                    if action[i] == '/':
                        check_division = 1
            out2 = "[number]"
        else:
            if count[1] != 0:
                j = 0
                action = []
                num = random.randint(0,count[1]-1)
                for i in range(count[1]):
                    index = quest.find("{action}")
                    index2 = quest2.find("{action}")
                    quest = quest[:index+7] + str(i) + quest[index+7:]
                    quest2 = quest2[:index2+7] + str(i) + quest2[index2+7:]
                    action.append(str(random.choice(generator['sign_for_action'])))
                    quest = quest.replace("{action"+str(i)+"}", action[j])
                    if action[i] == '/':
                        check_division = 1
                    if i != num:
                        quest2 = quest2.replace("{action"+str(i)+"}", action[j])
                    else:
                        quest2 = quest2.replace("{action"+str(i)+"}", "[action]")
                        out = action[num]
                    j += 1
            if count[0] != 0:
                number = []
                for i in range(count[0]):
                    index = quest.find("{number}")
                    index2 = quest2.find("{number}")
                    quest = quest[:index+7] + str(i) + quest[index+7:]
                    quest2 = quest2[:index2+7] + str(i) + quest2[index2+7:]
                    number.append(str(random.randint(generated_number[0],generated_number[1])))
                    quest = quest.replace("{number"+str(i)+"}", number[i])
                    quest2 = quest2.replace("{number"+str(i)+"}", number[i])
            out2 = "[action]"

        if check_division == 1:
            quest = quest.replace("int","double")
            quest = quest.replace("double main","int main")
            quest2 = quest2.replace("int","double")
            quest2 = quest2.replace("double main","int main")

        return [quest,quest2,out,out2,0] #Сделать проверку на единественный верный ответ, если при вычислениях будут 1 и больше вариантов

    def type_code_error(self, quest, error_choice):
        text = quest.split()
        choice = random.randint(1,2)
        count_error = self.counting(quest, error_choice)
        index = 0
        error_syntax = list(generator['error_syntax'])

        if count_error != 0 and choice == 1: #удаление
            num_error = random.randint(0,count_error-1)
            if error_choice == error_syntax[0]: #int
                num_check = []
                for i in range(count_error):
                    index = quest.find(error_choice,index)
                    if index == quest.find("int main"):
                        num_check.append(i)
                    if index == quest.find("int func") or index == quest.find("double func"):
                        num_check.append(i)
                    if i == num_error and not num_error in num_check:
                        quest = quest[:index] + '{replace_item}' + quest[index+len(error_choice)+1:]
                        choice_int = random.randint(1,3)
                        if choice_int == 1:
                            quest = quest.replace('{replace_item}', '')
                            break
                        elif choice_int == 2:
                            quest = quest.replace('{replace_item}', str(random.choice(generator['generated_number']))+'int')
                            break
                        else:
                            quest = quest.replace('{replace_item}', random.choice(generator['error_replace'][0])+' ')
                            break
            else:
                for i in range(count_error):
                    index = quest.find(error_choice,index)
                    if i == num_error:
                        quest = quest[:index] + '{replace_item}' + quest[index+len(error_choice)+1:]
                        quest = quest.replace('{replace_item}', '')
                        break
        elif count_error != 0 and choice == 2: #замена
            error_replace = list(generator['error_replace'])
            del error_replace[0]
            num_error = random.randint(0,count_error-1)
            for i in range(count_error):
                index = quest.find(error_choice,index)
                if i == num_error:
                    quest = quest[:index] + '{replace_item}' + quest[index+len(error_choice):]
                    if error_choice == error_syntax[1]: #(
                        quest = quest.replace('{replace_item}', error_replace[1])
                        break
                    elif error_choice == error_syntax[2]: #)              
                        quest = quest.replace('{replace_item}', error_replace[2])
                        break
                    elif error_choice == error_syntax[3]: #{
                        quest = quest.replace('{replace_item}', error_replace[3])
                        break
                    elif error_choice == error_syntax[4]: #}
                        quest = quest.replace('{replace_item}', error_replace[4])
                        break
                    else:
                        quest = quest.replace('{replace_item}', random.choice(error_replace))
                        break
        return quest

    def type_code_logic(self, quest):
        choice = random.randint(1,2)
        quest2 = quest
        #choice = 1
        out = ''
        out_error = []
        not_error = 0
        if choice == 2:
            error_choice = random.choice(generator['error_logic'])
        
        if quest.find("int func") or quest.find("double func") and choice == 1:
            choice_func = random.randint(1,2)
            if choice_func == 1:
                quest = quest.replace("return result;", "")
                quest2 = quest
                out_error.append("return result")
                out_error.append(random.choice(generator['error_replace'][0])+" result;") #весьма тупо
                out_error.append("return")
                out = "return result;"
            else:
                with open(path_compile, 'r') as fp:
                    for n, line in enumerate(fp, 1):
                        if line.find("return result;") != -1:
                            quest2 = quest.replace("return result;","")
                            out = n
        elif quest.find(error_choice) and choice == 2:
            quest = self.type_code_error(quest, error_choice)
            quest2 = quest
        else:
            not_error = 1
            quest2 = quest

        return [quest,quest2,out,out_error,not_error]
 #сопоставление пунктов списка

    def type_code_syntax(self, quest):
        #choice = random.randint(1,5)
        quest2 = quest
        choice = 5
        out = ''
        out_error = []
        not_error = 0
        if choice == 5:
            error_choice = random.choice(generator['error_syntax'])

        if (quest.find("int func") != -1 or quest.find("double func") != -1) and choice == 1: #не работает
            count_func = self.counting(quest, "func")
            func_check = []
            index_prev = 0           
            for i in range(count_func):
                index_next = quest.find("func",index_prev)
                if index_next == (quest.find("int func")+4) or index_next == (quest.find("double func")+7):
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
            quest2 = quest
        elif quest.find("void func") != -1 and choice == 2:
            index = quest.find("}\nint main")
            quest = quest[:index-1] + "\n    return result;\n" + quest[index:]
            quest2 = quest
        elif quest.find("==") != -1 and choice == 3:
            with open(path_compile, 'r') as fp:
                for n, line in enumerate(fp, 1):
                    if line.find("==") != -1:
                        quest2 = quest.replace("==","=")
                        out = n - 1
        elif quest.find("result") and choice == 4:
            if quest.find("int result") != -1:
                quest = quest.replace("int result", "const int result")
            elif quest.find("double result") != -1:
                quest = quest.replace("double result", "const double result")
            quest2 = quest
        elif quest.find(error_choice) != -1 and choice == 5:
            quest = self.type_code_error(quest, error_choice)
            quest2 = quest
        else:
            not_error = 1
            quest2 = quest

        return [quest,quest2,out,out_error,not_error]

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
                action.append(str(random.choice(generator['sign_for_action'])))
                if action[i] == '/':
                    check_division = 1
                quest = quest[:index+7] + str(i) + quest[index+7:]
                quest = quest.replace("{action"+str(i)+"}", action[i])
            if check_division == 1:
                quest = quest.replace("int","double")
                quest = quest.replace("double main","int main")
        if count[2] != 0: #словарь слов
            for i in range(count[2]):
                index = quest.find("{dictionary}")
                quest = quest[:index+11] + str(i) + quest[index+11:]
                quest = quest.replace("{dictionary"+str(i)+"}", str(random.choice(generator['dictionary'])))

        return quest

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

        return ans[index+2:]

    def answer_false(self, os_out):
        process = subprocess.Popen(os_out, shell=True, stdout=subprocess.PIPE, encoding=cmd_codepage, stderr=subprocess.STDOUT)
        tmp = process.stdout.read()
        #print(tmp)
        tmp = tmp.replace(path+"\quest.cpp:","")
        tmp = tmp.replace(" In function 'int main()':\n","")
        index = tmp.find(" In function 'int func")
        if index != -1:
            index2 = tmp.find(":\n",index)
            tmp = self.delete_error_code(tmp,index,index2)
        index = tmp.find(" In function 'double func")
        if index != -1:
            index2 = tmp.find(":\n",index)
            tmp = self.delete_error_code(tmp,index,index2)
        index = tmp.find(" In function 'void func")
        if index != -1:
            index2 = tmp.find(":\n",index)
            tmp = self.delete_error_code(tmp,index,index2)
        #print(tmp)
        index = tmp.find(":")
        ans = ''
        for i in range(index):
            ans += ''.join(tmp[i])
        return ans

    def delete_error_code(self, tmp, index, index2):
        tmp = tmp[:index] + tmp[index2+3:]
        return tmp

    def number_lines(self, filename, start=1):
        with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
            for n, line in enumerate(file, start=start):
                print(n, '    ', line, end='')
        os.unlink(filename + '.bak')
        return filename