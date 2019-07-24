import os
from datetime import datetime
import subprocess as subp

import pyttsx3
import wikipedia

from selenium.webdriver import Firefox, Chrome

from util.search_selenium import SearchGoogle
from util.email import Email

class CommandsBoot(object):

    def __init__(self):
        self.speaker = pyttsx3.init()
        wikipedia.set_lang('pt')

        self.keywords = ['quem é', 'o que é', 'quem foi', 'definição', 'defina']

        self.google_keywords = ['pesquisar por', 'pesquise por']

        self.email_keywords = ['informe dados']

        self.open_programs_keywords = ['abrir subl', 'abrir google-chrome', 'abrir telegram-desktop']

        self.dict_cmds = {}

    def load_cmds(self):
        lines = open('cmds.txt', 'r').readlines()
        for line in lines:
            line = line.replace('\n', '')
            parts = line.split('\t')
            self.dict_cmds.update({parts[0]: parts[1]})

    def set_voice(self):
        voices = self.speaker.getProperty('voices')

        for voice in voices:
            if voice.name == 'brazil':
                self.speaker.setProperty('voice', voice.id)


    def speak(self, text):
        self.speaker.say(text)
        self.speaker.runAndWait()

    def evaluate(self, text):
        result = None
        try:
            result = self.dict_cmds[text]
        except:
            result = None
        return result

    def run_cmd(self, cmd_type):
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


    def get_answer(self, text):
        result = None

        if text is not None:
            for key in self.keywords:
                if text.startswith(key):
                    result = text.replace(key, '')

        if result is not None:
            results = wikipedia.search(result)
            result = wikipedia.summary(results[0], sentences=2)
        return result


    def seach_web(self, text):
        google = SearchGoogle(Chrome())

        result = None
        if text is not None:
            for key in self.google_keywords:
                if text.startswith(key):
                    result = text.replace(key, '')
            if result is not None:
                google.open_navegator()
                google.search(keyword=result, 
                    label_class='gLFyf', 
                    label_xpath='.//input[@name="btnK"]')
                return 'Pesquisando por ' + result.rstrip() + '...'
        return result


    def send_mail(self, text):
        result = None

        if text is not None:
            for key in self.email_keywords:
                if text.startswith(key):
                    result = text.replace(key, '')
        for key in self.email_keywords:
            if text.startswith(key):
                result = text.replace(key, '')
        if result is not None:
            sender = input('login: ').lower()

            passw = input('password: ')

            recipient = input('Destinatário: ')

            subject_matter = input('Assunto: ')

            text_email = input('Text: ')

            print('\nTodos os dados foram preechidos!')

            email = Email(sender, passw, recipient)
            email.send_mail(subject_matter, text_email)

            print('\nemail enviado com sucesso!\n')


    def open_program(self, text):
        result = None
        if text is not None:
            for key in self.open_programs_keywords:
                if text.startswith(key):
                    result = text.replace(key, '')
            if result is not None:
                for i, v in enumerate(self.open_programs_keywords):
                    subp.Popen(v.split(' ')[-1])