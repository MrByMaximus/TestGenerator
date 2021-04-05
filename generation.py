import sys, os
import random
import fileinput
import subprocess
import ast
import re

path = os.getcwd()
path1 = path+'/quest.cpp'
path2 = path+'/quest.txt'
path3 = path+'/quest_xml.txt'
generator = open(path+'/generator.conf','r')
generator = ast.literal_eval(generator.read())
cmd_codepage = os.device_encoding(1) or ctypes.windll.kernel32.GetOEMCP()

class Generation(): #Генерация вопроса
    import re
    def __init__(self):
        super().__init__()

    def question_gen(self):
        DEVNULL = os.open(os.devnull, os.O_WRONLY)
        path4 = path+'/cods'
        #code = random.randint(1,len(os.listdir(path3)))
        #type_quiz = random.randint(1,4)
        type_quiz = 4
        code = 2
        out_error = [] #заглушка
        type_error = 0

        code_error_for_type_quiz = [1]
        if type_quiz == 3 and code in code_error_for_type_quiz:
            type_quiz = 4

        file = open(path4+"/"+str(code)+".txt",'r')
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
        with open(self.number_lines(path2), "r") as f:
            text = f.read()

        #check = subprocess.call(os_out, shell=True, stdout=DEVNULL, stderr=subprocess.STDOUT)
        if type_quiz == 3:
            ans2 = self.answer_true(os_out)
            quiz = "При каком значении "+quest2[3]+" программа выдаст результат: "+ans2
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

        return [text,str(ans),quiz,type_error,out_error]

    def count_num(self, quest):
        text = quest.split()
        count_number = 0
        count_action = 0

        for word in text:
            if word.find("{number_"+str(count_number)+"}") != -1:
                count_number+=1
            if word.find("{action_"+str(count_action)+"}") != -1:
                count_action += 1

        return [count_number, count_action]

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
        count = self.count_num(quest)
        choice = random.randint(1,2)
        check_division = 0
        out = ''
        generated_number = list(generator['generated_number'])

        quest = self.noise(quest)
        quest2 = self.noise(quest)

        if choice == 1:
            if count[0] != 0:
                j = 0
                number = []
                num = random.randint(0,count[0]-1)
                for i in range(count[0]):
                    number.append(str(random.randint(generated_number[0],generated_number[1])))
                    quest = re.sub("{number_"+str(i)+"}", number[j], quest)
                    if i != num:
                        quest2 = re.sub("{number_"+str(i)+"}", number[j], quest2)
                    else:
                        quest2 = re.sub("{number_"+str(i)+"}", "{number}", quest2)
                        out = number[num]
                    j += 1
            if count[1] != 0:
                action = []
                for i in range(count[1]):
                    action.append(str(random.choice(generator['sign_for_action'])))
                    quest = re.sub("{action_"+str(i)+"}", action[i], quest)
                    quest2 = re.sub("{action_"+str(i)+"}", action[i], quest2)
                    if action[i] == '/':
                        check_division = 1
            out2 = "{number}"
        else:
            if count[1] != 0:
                j = 0
                action = []
                num = random.randint(0,count[1]-1)
                for i in range(count[1]):
                    action.append(str(random.choice(generator['sign_for_action'])))
                    quest = re.sub("{action_"+str(i)+"}", action[j], quest)
                    if action[i] == '/':
                        check_division = 1
                    if i != num:
                        quest2 = re.sub("{action_"+str(i)+"}", action[j], quest2)
                    else:
                        quest2 = re.sub("{action_"+str(i)+"}", "{action}", quest2)
                        out = action[num]
                    j += 1
            if count[0] != 0:
                number = []
                for i in range(count[0]):
                    number.append(str(random.randint(generated_number[0],generated_number[1])))
                    quest = re.sub("{number_"+str(i)+"}", number[i], quest)
                    quest2 = re.sub("{number_"+str(i)+"}", number[i], quest2)
            out2 = "{action}"

        if check_division == 1:
            quest = re.sub("int","double",quest)
            quest = re.sub("double main","int main",quest)
            quest2 = re.sub("int","double",quest2)
            quest2 = re.sub("double main","int main",quest2)

        return [quest,quest2,out,out2,0] #Сделать проверку на единественный верный овтет, если при вычислениях будут 1 и больше вариантов

    def type_code_error(self, quest, error_choice):
        text = quest.split()
        choice = random.randint(1,2)
        count_error = 0
        index_prev = 0
        error_syntax = list(generator['error_syntax'])

        for word in text:
            if word.find(error_choice) != -1:
                count_error += 1

        if count_error != 0 and choice == 1: #удаление
            num_error = random.randint(0,count_error-1)
            if error_choice == error_syntax[0]: #int
                num_check = []
                for i in range(count_error):
                    index_next = quest.find(error_choice,index_prev)
                    if index_next == quest.find("int main"):
                        num_check.append(i)
                    if index_next == quest.find("int func") or quest.find("double func"):
                        num_check.append(i)
                    else:
                        index_prev = index_next+len(error_choice)
                    if i == num_error and not num_error in num_check:
                        quest = quest[:index_next] + '{replace_item}' + quest[index_next+len(error_choice)+1:]
                        choice_int = random.randint(1,3)
                        if choice_int == 1:
                            quest = re.sub('{replace_item}', '', quest)
                            break
                        elif choice_int == 2:
                            quest = re.sub('{replace_item}', str(random.choice(generator['generated_number']))+'int', quest)
                            break
                        else:
                            quest = re.sub('{replace_item}', random.choice(generator['error_replace'][0])+' ', quest)
                            break
            else:
                for i in range(count_error):
                    index_next = quest.find(error_choice,index_prev)
                    index_prev = index_next+len(error_choice)
                    if i == num_error:
                        quest = quest[:index_next] + '{replace_item}' + quest[index_next+len(error_choice)+1:]
                        quest = re.sub('{replace_item}', '', quest)
                        break
        elif count_error != 0 and choice == 2: #замена
            error_replace = list(generator['error_replace'])
            del error_replace[0]
            num_error = random.randint(0,count_error-1)
            for i in range(count_error):
                index_next = quest.find(error_choice,index_prev)
                index_prev = index_next+len(error_choice)
                if i == num_error:
                    quest = quest[:index_next] + '{replace_item}' + quest[index_next+len(error_choice)+1:]
                    if error_choice == error_syntax[1]: #(
                        quest = re.sub('{replace_item}', error_replace[1], quest)
                        break
                    elif error_choice == error_syntax[2]: #)              
                        quest = re.sub('{replace_item}', error_replace[2], quest)
                        break
                    elif error_choice == error_syntax[3]: #{
                        quest = re.sub('{replace_item}', error_replace[3], quest)
                        break
                    elif error_choice == error_syntax[4]: #}
                        quest = re.sub('{replace_item}', error_replace[4], quest)
                        break
                    else:
                        quest = re.sub('{replace_item}', random.choice(error_replace), quest)
                        break
        return quest

    def type_code_logic(self, quest):
        quest2 = quest
        #choice = random.randint(1,2)
        choice = 1
        out = ''
        out_error = []
        not_error = 0
        error_choice = random.choice(generator['error_logic'])
        
        if quest.find("int func") or quest.find("double func") and choice == 1:
            choice_func = random.randint(1,2)
            if choice_func == 1:
                quest = re.sub("return result;", "", quest)
                quest2 = quest
                out_error.append("return result")
                out_error.append(random.choice(generator['error_replace'][0])+" result;") #весьма тупо
                out_error.append("return")
                out = "return result;"
            else:
                with open(path1, 'r') as fp:
                    for n, line in enumerate(fp, 1):
                        if line.find("return result;") != -1:
                            quest2 = re.sub("return result;","",quest2)
                            out = n
        elif quest.find(error_choice) and choice == 2:
            quest = self.type_code_error(quest, error_choice)
            quest2 = quest
        else:
            not_error = 1

        return [quest,quest2,out,out_error,not_error]
 #сопоставление пунктов списка

    def type_code_syntax(self, quest):
        quest2 = quest
        #choice = random.randint(1,5)
        choice = 2
        out = ''
        out_error = []
        not_error = 0
        error_choice = random.choice(generator['error_syntax'])

        if quest.find("func(a") != -1 and choice == 1: #не работает
            index1 = quest.find("func(a")
            index = []
            index.append(quest.find("(",index1)-1)
            index2 = quest.find(")",index1)
            i = index1+4
            while i != index2:
                index1 = quest.find(",",index1+2,index2)
                if index1 != -1:
                    index.append(index1)
                i += 2
            index.append(index[len(index)-1])
            num = random.randint(1,len(index)-1)
            quest = quest[:index[num]] + quest[index[len(index)-1]:] #в конце добавить скобку
        elif quest.find("void func") != -1 and choice == 2:
            index = quest.find("}\nint main")
            quest = quest[:index-1] + "\n    return result;\n" + quest[index:]
            quest2 = quest
        elif quest.find("==") != -1 and choice == 3:
            with open(path1, 'r') as fp:
                for n, line in enumerate(fp, 1):
                    if line.find("==") != -1:
                        quest2 = re.sub("==","=",quest2)
                        out = n - 1
        elif quest.find("int result") and choice == 4:
            quest = re.sub("int result", "const int result", quest)
            quest2 = quest
        elif quest.find(error_choice) != -1 and choice == 5:
            quest = self.type_code_error(quest, error_choice)
            quest2 = quest
        else:
            not_error = 1

        return [quest,quest2,out,out_error,not_error]

    def read_code(self, quest):
        #import re
        count = self.count_num(quest)
        quest = self.noise(quest)
        check_division = 0
        generated_number = list(generator['generated_number'])

        if count[0] != 0:
            for i in range(count[0]):
                quest = re.sub("{number_"+str(i)+"}", str(random.randint(generated_number[0],generated_number[1])), quest)
        
        if count[1] != 0:
            action = []
            for i in range(count[1]):
                action.append(str(random.choice(generator['sign_for_action'])))
                if action[i] == '/':
                    check_division = 1
                quest = re.sub("{action_"+str(i)+"}", action[i], quest)

        if check_division == 1:
            quest = re.sub("int","double",quest)
            quest = re.sub("double main","int main",quest)

        return quest

    def write_code_output(self, quest):
        file1 = open(path2,'w')
        file1.write(quest)
        file1.close()
        file2 = open(path3,'w')
        file2.write(quest)
        file2.close()

    def write_code(self, quest):
        file = open(path1,'w')
        file.write(quest)
        file.close()
        if sys.platform == "linux" or sys.platform == "linux2":
            return "g++ " + path + "/quest.cpp -o " + path + "/quest"
        else:
            return "g++ " + path + "\quest.cpp -o " + path + "\quest"

    def delete_file(self):
        os.remove(os.path.join(path1))
        os.remove(os.path.join(path2))
        os.remove(os.path.join(path3))
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
        tmp = tmp.replace(" In function 'int func(int, int)':\n","") #это не нормально
        tmp = tmp.replace(" In function 'double func(int, int)':\n","")
        tmp = tmp.replace(" In function 'void func(int, int)':\n","")
        print(tmp)
        index = tmp.find(":")
        ans = ''
        for i in range(index):
            ans += ''.join(tmp[i])

        return ans

    def number_lines(self, filename, start=1):
        with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
            for n, line in enumerate(file, start=start):
                print(n, '    ', line, end='')
        os.unlink(filename + '.bak')
        return filename
