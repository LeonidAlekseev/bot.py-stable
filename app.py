#! /usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
import ast
import re
from flask_sslify import SSLify
import traceback
import sys
from contextlib import redirect_stdout


app = Flask(__name__)
sslify = SSLify(app)
URL = 'https://api.telegram.org/bot953353291:AAEgHkSY2PLKa2Ve2Z7Mu3WAOM5pir_fUmk/'


def send_message(chat_id, text='Какой-то текст.'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()

def transtlate(errname):
    if "BaseException" in errname:
        sut="базовое исключение, от которого берут начало все остальные"
    elif "SystemExit" in errname:
        sut="исключение, порождаемое функцией sys.exit при выходе из программы"
    elif "KeyboardInterrupt" in errname:
        sut="порождается при прерывании программы пользователем (обычно сочетанием клавиш Ctrl+C)"
    elif "GeneratorExit" in errname:
        sut="порождается при вызове метода close объекта generator"
    elif "Exception" in errname:
        sut="а вот тут уже заканчиваются полностью системные исключения (которые лучше не трогать) и начинаются обыкновенные, с которыми можно работать"
    elif "StopIteration" in errname:
        sut="порождается встроенной функцией next, если в итераторе больше нет элементов"
    elif "ArithmeticError" in errname:
        sut="арифметическая ошибка"
    elif "FloatingPointError" in errname:
        sut="порождается при неудачном выполнении операции с плавающей запятой"
    elif "OverflowError" in errname:
        sut="возникает, когда результат арифметической операции слишком велик для представления - не появляется при обычной работе с целыми числами (так как python поддерживает длинные числа), но может возникать в некоторых других случаях"
    elif "ZeroDivisionError" in errname:
        sut="деление на ноль"
    elif "AssertionError" in errname:
        sut="выражение в функции assert ложно"
    elif "AttributeError" in errname:
        sut="объект не имеет данного атрибута (значения или метода)"
    elif "BufferError" in errname:
        sut="операция, связанная с буфером, не может быть выполнена"
    elif "EOFError" in errname:
        sut="функция наткнулась на конец файла и не смогла прочитать то, что хотела"
    elif "ImportError" in errname:
        sut="не удалось импортирование модуля или его атрибута"
    elif "LookupError" in errname:
        sut="некорректный индекс или ключ"
    elif "IndexError" in errname:
        sut="индекс не входит в диапазон элементов"
    elif "KeyError" in errname:
        sut="несуществующий ключ (в словаре, множестве или другом объекте)"
    elif "MemoryError" in errname:
        sut="недостаточно памяти"
    elif "NameError" in errname:
        sut="не найдено переменной с таким именем"
    elif "UnboundLocalError" in errname:
        sut="сделана ссылка на локальную переменную в функции, но переменная не определена ранее"
    elif "OSError" in errname:
        sut="ошибка, связанная с системой"
    elif "BlockingIOError" in errname:
        sut="ошибка, связанная с системой"
    elif "ChildProcessError" in errname:
        sut="неудача при операции с дочерним процессом"
    elif "ConnectionError" in errname:
        sut="базовый класс для исключений, связанных с подключениями"
    elif "BrokenPipeError" in errname:
        sut="проблемы с подключенем"
    elif "ConnectionAbortedError" in errname:
        sut="проблемы с подключенем"
    elif "ConnectionRefusedError" in errname:
        sut="проблемы с подключенем"
    elif "ConnectionResetError" in errname:
        sut="проблемы с подключенем"
    elif "FileExistsError" in errname:
        sut="попытка создания файла или директории, которая уже существует"
    elif "FileNotFoundError" in errname:
        sut="файл или директория не существует"
    elif "InterruptedError" in errname:
        sut="системный вызов прерван входящим сигналом"
    elif "IsADirectoryError" in errname:
        sut="ожидался файл, но это директория"
    elif "NotADirectoryError" in errname:
        sut="ожидалась директория, но это файл"
    elif "PermissionError" in errname:
        sut="не хватает прав доступа"
    elif "ProcessLookupError" in errname:
        sut="указанного процесса не существует"
    elif "TimeoutError" in errname:
        sut="закончилось время ожидания"
    elif "ReferenceError" in errname:
        sut="попытка доступа к атрибуту со слабой ссылкой"
    elif "RuntimeError" in errname:
        sut="возникает, когда исключение не попадает ни под одну из других категорий"
    elif "NotImplementedError" in errname:
        sut="возникает, когда абстрактные методы класса требуют переопределения в дочерних классах"
    elif "SyntaxError" in errname:
        sut="синтаксическая ошибка"
    elif "IndentationError" in errname:
        sut="неправильные отступы"
    elif "TabError" in errname:
        sut="смешивание в отступах табуляции и пробелов"
    elif "SystemError" in errname:
        sut="внутренняя ошибка"
    elif "TypeError" in errname:
        sut="операция применена к объекту несоответствующего типа"
    elif "ValueError" in errname:
        sut="функция получает аргумент правильного типа, но некорректного значения"
    elif "UnicodeError" in errname:
        sut="ошибка, связанная с кодированием / раскодированием unicode в строках"
    elif "UnicodeEncodeError" in errname:
        sut="исключение, связанное с кодированием unicode"
    elif "UnicodeDecodeError" in errname:
        sut="исключение, связанное с декодированием unicode"
    elif "UnicodeTranslateError" in errname:
        sut="исключение, связанное с переводом unicode"
    elif "Warning" in errname:
        sut="предупреждение"
    else:
        sut="ошибка не опознана"
    return sut

def load_dict_from_file():
    f = open('dict.txt','r')
    data=f.read()
    f.close()
    return eval(data)

def save_dict_to_file(dic):
    old=load_dict_from_file()
    old.update(dic)
    f = open('dict.txt','w')
    f.write(str(old))
    f.close()

def add_key(user):
    dic={user:'key'}
    save_dict_to_file(dic)

def add_pass(user,pas):
    dic={user:pas}
    save_dict_to_file(dic)

def check_key(user):
    baza=load_dict_from_file()
    if user in baza:
        return 'yes'
    else:
        return 'no'

def check_pass(user):
    baza=load_dict_from_file()
    if baza[user] != 'key':
        return 'yes'
    else:
        return 'no'

def cms(wel):
    with open('help.txt', 'w') as f:
        with redirect_stdout(f):
            if "while True" not in wel and "input(" not in wel:
                try:
                    exec(wel)
                except Exception:
                    print(traceback.format_exc())
            else:
                if "while True" in wel:
                    print("Бесконечный цикл невозможен")
                if "input(" in wel:
                    print("Ввод невозможен")
    with open('help.txt', 'r') as f:
        exit=f.read()
        if 'Traceback' in exit:
            lines = open('help.txt').readlines()
            open('help.txt', 'w').writelines(lines[3:-1])
            preexit=open('help.txt').read()
            nameerrexit=str(open('help.txt').readlines())
            lineerrexit=open('help.txt').readlines()[0].split(',')[1]
            lineerrexit=lineerrexit.replace("line", "линия")
            sutexit=transtlate(nameerrexit)
            exit='\u26A0 ОШИБКА \u26A0 \n'+preexit+'\n\uD83D\uDE3B РАСШИФРОВКА \uD83D\uDE3B \n  Суть ошибки: '+sutexit+'\n  Место ошибки:'+lineerrexit
        else:
            exit=open('help.txt', 'r').read()
    return exit

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']
        user_first_name = r['message']['chat']['first_name']
        user_last_name = r['message']['chat']['last_name']
        user = user_first_name+' '+user_last_name
        m = re.compile(r'[a-zA-Z0-9]*$')
        if message != '' and check_key(user)=='yes' and check_pass(user)=='yes':
            result = cms(message)
            send_message(chat_id, text=result)
        elif message == '/start':
            send_message(chat_id, text="Инструкция:\n 1) Первым сообщением введите ключ активации\n 2) Вторым сообщением зарегистрируйтесь с паролем")
        elif message == 'PM19-1' and check_key(user)=='no':
            add_key(user)
            send_message(chat_id, text="Ключ активирован!")
            send_message(chat_id, text="Пожалуйста, зарегистрируйте пароль!\nНе менее 6 символов в длину, с латинскими буквами и цифрами.")
        elif message != '' and len(message)>6 and str(message).isalpha()!=1 and str(message).isdigit()!=1 and check_key(user)=='yes' and check_pass(user)=='no' and m.match(str(message)):
            add_pass(user,message)
            send_message(chat_id, text="Пароль зарегистрирован!")
            slip=user+' '+message
            slip=str(slip)
            send_message(chat_id, text=chat_id)
        elif message != '' and check_key(user)=='no':
            send_message(chat_id, text="Пожалуйста, введите ключ активации!")
        elif message != '' and check_key(user)=='yes' and check_pass(user)=='no':
            send_message(chat_id, text="Пожалуйста, зарегистрируйте пароль!\nНе менее 6 символов в длину, с латинскими буквами и цифрами.")
        return jsonify(r)
    return '<h1>PMiIT bot welcomes you</h1>'

@app.route('/dic')
def dic():
    return '<h1>PMiIT bot welcomes you</h1>'

if __name__ == '__main__':
    app.run()
