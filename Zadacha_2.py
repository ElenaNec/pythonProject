#Доработать ф-ю из предыдущего задания так, чтобы у нее появился дополнительный режим работы,
#в котором вывод разбивается на слова с удалением всех знаков пунктуации(string.punctuation модуля string).
#В этом режиме должно проверяться наличие слова в выводе

import subprocess
import string

def comand_exe(command, text ):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout
    if result.returncode == 0:
        word = out.translate(str.maketrans('', '', string.punctuation))
        if text in word:
            return True
        else:
            return False

if __name__ == '__main__':
    command = 'cat /etc/os-release'
    text = 'jammy'
    # command = 'ls /home/user'
    # text = 'test'
    print(comand_exe(command, text))
