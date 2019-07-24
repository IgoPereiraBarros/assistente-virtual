# -*- coding: utf-8  -*-

from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
import speech_recognition as sr

from commands_boot import CommandsBoot

bot = ChatBot('Jarvis', read_only=True)

commands_boot = CommandsBoot()
commands_boot.set_voice()
commands_boot.load_cmds()

for k, v in commands_boot.dict_cmds.items():
    print(k, ' ====> ', v)


r = sr.Recognizer()

with sr.Microphone() as s:
    r.adjust_for_ambient_noise(s)

    while True:
        try:

            audio = r.listen(s)

            speech = r.recognize_google(audio, language='pt').lower()
            response = commands_boot.run_cmd(commands_boot.evaluate(speech))

            if response == None:
                response = commands_boot.get_answer(speech)
                if response == None:
                    response = commands_boot.seach_web(speech)
                    if response == None:
                        response = commands_boot.send_mail(speech)
                        if response == None:
                            response = commands_boot.open_program(speech)
                            if response == None:
                                response = bot.get_response(speech)

            print('Você disse: %s' % speech)
            print('Bot: %s' % response)
            commands_boot.speak(response)

        except sr.UnknownValueError:
            #print('Erro no reconhecimento de fala')
            print('Aguardando algum comando de voz...')
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except Exception as e:
            raise e
