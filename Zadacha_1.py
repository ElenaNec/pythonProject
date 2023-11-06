#Написать функцию на Python, которой передаются в качестве параметров команда и текст.
#Функция должна возвращать True, если команда успешно выполнена и текст найден в ее выводе.
# Передаваться должна только одна строка, разбиение вывода использовать не нужно.
import subprocess

def comand_exe(command, text ):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout
    if result.returncode == 0:
        lst = out.split('\n')
        if text in lst:
            return True
        else:
            return False

if __name__ == '__main__':
    # command = 'cat /etc/os-release'
    # text = 'VERSION_CODENAME=jammy'
    command = 'ls /home/user'
    text = 'test'
    print(comand_exe(command, text))
