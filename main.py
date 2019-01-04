# -*- coding: utf-8  -*-

from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
import os
from datetime import datetime
import webbrowser

import pyttsx3
speaker = pyttsx3.init()

import wikipedia

wikipedia.set_lang('pt')

import speech_recognition as sr

from googleapiclient.discovery import build

my_api_key = 'your keyt'
my_cse_id = 'your cse_id'

bot = ChatBot('Jarvis', read_only=True)

keywords = ['quem é', 'o que é', 'quem foi', 'definição', 'defina']

google_keywords = ['pesquisar por', 'pesquise por']

dict_cmds = {}

def load_cmds():
    lines = open('cmds.txt', 'r').readlines()
    for line in lines:
        line = line.replace('\n', '')
        parts = line.split('\t')
        dict_cmds.update({parts[0]: parts[1]})

def set_voice():
    voices = speaker.getProperty('voices')

    for voice in voices:
        if voice.name == 'brazil':
            speaker.setProperty('voice', voice.id)


def speak(text):
	speaker.say(text)
	speaker.runAndWait()

def evaluate(text):
    result = None
    try:
        result = dict_cmds[text]
    except:
        result = None
    return result

def run_cmd(cmd_type):
    result = None

    if cmd_type == 'asktime':
        now = datetime.now()
        result = 'São ' + str(now.hour) + ' horas e ' + str(now.minute) + ' minutos'
    elif cmd_type == 'askdate':
        now = datetime.now()
        months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho',
                  'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        result = 'Hoje é ' + str(now.day) + ' de ' + months[now.month - 1]
    else:
        result = None
    return result


def get_answer(text):
    result = None

    if text is not None:
        for key in keywords:
            if text.startswith(key):
                result = text.replace(key, '')

    if result is not None:
        results = wikipedia.search(result)
        result = wikipedia.summary(results[0], sentences=2)
    return result

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build('customsearch', 'v1', developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items'][0]['link']


def seach_web(text):
    result = None
    if text is not None:
        for key in google_keywords:
            if text.startswith(key):
                result = text.replace(key, '')
        if result is not None:
            url = google_search(result, my_api_key, my_cse_id, num=1)
            webbrowser.open_new_tab(url)
            return 'Pesquisando por ' + result.rstrip() + '...'
    return result

set_voice()
load_cmds()

for k, v in dict_cmds.items():
    print(k, ' ====> ', v)


r = sr.Recognizer()

with sr.Microphone() as s:
    r.adjust_for_ambient_noise(s)

    while True:
        try:

            audio = r.listen(s)

            speech = r.recognize_google(audio, language='pt').lower()
            response = run_cmd(evaluate(speech))

            if response == None:
                response = get_answer(speech)
                if response == None:
                    response = seach_web(speech)
                    if response == None:
                        response = bot.get_response(speech)

            print('Você disse: %s' % speech)
            print('Bot: %s' % response)
            speak(response)

        except sr.UnknownValueError:
            #print('Erro no reconhecimento de fala')
            print('Aguardando algum comando de voz...')
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except Exception as e:
            raise e
