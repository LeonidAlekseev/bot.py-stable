#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tabulate import tabulate
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
import pymongo
from pymongo import MongoClient
import datetime
import math
import time
import codecs
import shutil
import os
from PIL import Image
import pytesseract
import io
import urllib.request
import signal
app = Flask(__name__)
sslify = SSLify(app)

token = str(os.environ.get("TOKEN"))+"/"
mongo_login=str(os.environ.get("MONGO_LOGIN"))
mongo_cluster=str(os.environ.get("MONGO_CLUSTER"))
mongo_collection=str(os.environ.get("MONGO_COLLECTION"))
URL = 'https://api.telegram.org/bot'+token
pytesseract.pytesseract.tesseract_cmd = '/app/vendor/tesseract-ocr/bin/tesseract'
now = datetime.datetime.now()

def send_message(chat_id, text='Какой-то текст.'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()
#Line search
def w_line(text):
    c=text.count("line")
    n=0
    while n<c:
        n=n+1
        ret=text.find("line") 
        text=text[ret+5:] 
    stop=text.find(" ") 
    if stop == -1: 
        line_n=text[0:]
    else:
        line_n=text[0:stop]
    line=line_n.replace(',','')
    return line
#-Line search
#Definitions
def transtlate(errname):
    if "BlockInfinityErrore" in errname:
        sut="время обработки операции превысило допустимое значение (бесконечные циклы запрещены)"
    elif "BaseException" in errname:
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
    elif "ModuleNotFoundError" in errname:
        sut="не импортирован вызываемый модуль"
    else:
        sut="ошибка не опознана"
    return sut
#-Definitions
#MongoDB
cluster=MongoClient("mongodb+srv://"+mongo_login+"@cluster0-umqxp.mongodb.net/test?retryWrites=true&w=majority")
db = cluster[mongo_cluster]
collection = db[mongo_collection]
def find_string(user):
    answer = False
    post = {"user":user}
    results = collection.find(post)
    for result in results:
        if result != '':
            answer = True
    return answer
def find_password(user):
    answer = False
    post = {"user":user}
    passwords = collection.find(post)
    check="0"
    for password in passwords:
        check = password["password"]
        if check != "0":
            answer = True
    return answer
def new_password(user,password):
    user_post = {"user":user}
    pass_post = {"$set":{"password":password}}
    results = collection.update_one(user_post,pass_post)
def new_user(user):
    post = {"user": user,"password": "0"}
    collection.insert_one(post)
#-MongoDB
#Auth
def key():
    key = str(math.fabs(math.sin(now.minute+now.day)))[2:7]
    return key+'-LIL'
def add_key(user):
    new_user(user)
def add_pass(user,pas):
    new_password(user,pas)
def check_key(user):
    if find_string(user):
        return 'yes'
    else:
        return 'no'
def check_pass(user):
    if find_password(user):
        return 'yes'
    else:
        return 'no'
#-Auth
#Cms
def cms(wel):
    lineerrexit=""
    with open('help.txt', 'w') as f:
        with redirect_stdout(f):
            if "input(" not in wel:
                try:
                    def long_function_call(inp):
                        exec(inp)
                    def signal_handler(signum, frame):
                        raise Exception("BlockInfinityErrore")
                    signal.signal(signal.SIGALRM, signal_handler)
                    #how much seconds
                    signal.alarm(3)
                    long_function_call(wel)
                except Exception:
                    print(traceback.format_exc())
            else:
                if "input(" in wel:
                    print("Ввод невозможен")
    with open('help.txt', 'r') as f:
        exit=f.read()
        if 'Traceback' in exit:
            lines = open('help.txt').readlines()
            open('helpfull.txt', 'w').writelines(lines[-20:-10])
            open('helpfull.txt', 'a').writelines(lines[-2])
            open('help.txt', 'w').writelines(lines[5:-1])
            preexit=open('help.txt').read()
            nameerrexit=str(open('help.txt').readlines())
            lineerrexit="линия " + str(w_line(str(preexit)))
            sutexit=transtlate(nameerrexit)
            if "BlockInfinityErrore" in nameerrexit:
                preexit=open('helpfull.txt').read()
                lineerrexit="неопределено"
            exit='\u26A0 ОШИБКА \u26A0 \n'+preexit+'\n\uD83D\uDE3B ПОЯСНЕНИЕ \uD83D\uDE3B \n  Суть ошибки: '+sutexit+'\n  Место ошибки: '+lineerrexit
        else:
            exit=open('help.txt', 'r').read()
            if exit == '' or exit == ' ':
                exit='В консоль ничего не вывелось! Проверьте, пожалуйста, возможно где-то не хватает print() или return.'
    return exit, lineerrexit
#-Cms
#OCR
def get_ocr(url):
    #download file
    filename = url.split("/")[-1]
    send_message(676318616, text="1")
    filetype = filename.split('.')
    send_message(676318616, text="2")
    if filetype[-1] != "jpg" and filetype[-1] != "png":
        return 111
    send_message(676318616, text="3")
    response = requests.get(url, stream=True)
    send_message(676318616, text="4")
    with open(str(filename), 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    send_message(676318616, text="5")
    del response
    send_message(676318616, text="6")
    #size of image
    img = Image.open(filename)
    send_message(676318616, text="7")
    new_size = tuple(4*x for x in img.size)
    send_message(676318616, text="8")
    img = img.resize(new_size, Image.ANTIALIAS)
    send_message(676318616, text="9")
    img.save("4x"+filename)
    send_message(676318616, text="10")
    #pytesseract
    text = pytesseract.image_to_string(Image.open("4x"+filename))
    send_message(676318616, text="11")
    text = text.replace("\n\n","\n")
    send_message(676318616, text="12")
    if text != '':
        return text
    else:
        return 222
    send_message(676318616, text="1")
    #delete file
    os.remove(filename)
    send_message(676318616, text="1")
    os.remove("4x"+filename)
    send_message(676318616, text="1")
#-OCR
#Flask
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        photo_id="0"
        message=""
        try:
            message = r['message']['text']
        except BaseException:
            pass
        try:
            photo_id=r['message']['photo'][-1]['file_id']
        except BaseException:
            pass
        user_first_name='0'
        user_last_name='0'
        try:
            user_first_name = r['message']['chat']['first_name']
        except BaseException:
            pass
        try:
            user_last_name = r['message']['chat']['last_name']
        except BaseException:
            pass
        user = user_first_name+' '+user_last_name
        if user=='0 0':
            user=chat_id
        m = re.compile(r'[a-zA-Z0-9]*$')
        if check_key(user)=='yes' and check_pass(user)=='yes':
            if photo_id != "0":
                send_message(chat_id, text="Подождите, пока фото обрабатывается.")
                photo=URL+"getFile?file_id="+str(photo_id)
                ph = requests.get(photo)
                ph= ph.json()
                photo_path=ph['result']['file_path']
                path_to_download="https://api.telegram.org/file/bot"+token+str(photo_path)
                try:
                    text_ocr = get_ocr(path_to_download)
                except BaseException:
                    text_ocr = 333
                my_string=str(text_ocr)
                mapping = [("“", "\x22"), ("‘", "\x22"), ("\x27", "\x22"), ("\x22\x22", "\x22")]
                for k, v in mapping:
                    my_string = my_string.replace(k, v)
                if text_ocr == 111:
                    send_message(chat_id, text="Ошибка формата. Конвертируйте фото в png или jpg!")
                elif text_ocr == 222:
                    send_message(chat_id, text="Ошибка распознавания. Попробуйте ещё раз!")
                elif text_ocr == 333:
                    send_message(chat_id, text="Технические неполадки. Обратитесь к отцу бота! Lil Dojd - https://vk.com/misterlil")
                else:
                    send_message(chat_id, text="Вот что у нас получилось:")
                    send_message(chat_id, text=my_string)
                    send_message(chat_id, text="1) Проверьте правильность распознования \n2) Скопируйте код \n3) Отправьте его нам для исполнения\n**Если вы что-то упустите, мы подскажем, где ошибка!")
            elif message != "":
                if now.hour+3 == 4 and 0<now.minute<5:
                    result = "Бот перезагружен. Приятной работы!"
                else:
                    try:
                        result = cms(message)[0]
                        #----------------------restart----------------------
                        #result = "Бот остановлен! Обратитесь к отцу бота! Lil Dojd - https://vk.com/misterlil"
                        #---------------------------------------------------
                    except BaseException:
                        result = "Ошибка сиситемы. Код не может быть выполнен. Обратитесь к отцу бота! Lil Dojd - https://vk.com/misterlil"
                send_message(chat_id, text=result)
                try:
                    if "ПОЯСНЕНИЕ" in result and "BlockInfinityErrore" not in result:
                        message=message+"\n"
                        s=message.split("\n") 
                        line_sec=cms(message)[1]
                        line_sec=int(line_sec.split(" ")[-1])
                        for i in range(len(s)):
                            if i == line_sec:
                                s[i-1] = s[i-1] + " \u26A0"
                        send_message(chat_id, text=str("\n".join(s)))
                except BaseException:
                    pass
        elif message == '/start':
            send_message(chat_id, text="Инструкция:\n 1) Сначала введите ключ активации. Его можно запросить у Lil Dojd - https://vk.com/misterlil.\n 2) Затем зарегистрируйтесь с паролем. Он необходим в случае переноса бота на другой сервис или при глобальном обновлении.")
        elif message == key() and check_key(user)=='no':
            add_key(user)
            send_message(chat_id, text="Ключ активирован!")
            send_message(chat_id, text="Пожалуйста, зарегистрируйте пароль!\nНе менее 6 символов. Латинские буквы и цифры.")
        elif message != '' and len(message)>6 and str(message).isalpha()!=1 and str(message).isdigit()!=1 and check_key(user)=='yes' and check_pass(user)=='no' and m.match(str(message)):
            add_pass(user,message)
            send_message(chat_id, text="Аккаунт зарегистрирован!")
            send_message(chat_id, text="Можно приступать к работе с ботом!")
        elif message != '' and check_key(user)=='no':
            send_message(chat_id, text="Пожалуйста, введите ключ активации!")
        elif message != '' and check_key(user)=='yes' and check_pass(user)=='no':
            send_message(chat_id, text="Пожалуйста, зарегистрируйте пароль!\nНе менее 6 символов. Латинские буквы и цифры.")
        return jsonify(r)
    return '<h1>Bot.py working now!</h1>'
#-Flask

if __name__ == '__main__':
    app.run()
 
