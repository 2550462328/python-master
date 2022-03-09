# -*- coding: utf-8-*-
import pyttsx3
import win32com.client
from aip import AipSpeech
from playsound import playsound

"""
pip3 install pypiwin32
pip3 install pyttsx3
pip3 install baidu-aip
https://blog.52itstyle.vip/
https://pyttsx3.readthedocs.io/en/latest/
"""


def say():
    engine = pyttsx3.init()
    # 音色
    voices = engine.getProperty('voices')
    # 语速
    rate = engine.getProperty('rate')
    # 音量
    volume = engine.getProperty('volume')
    for voice in voices:
        engine.setProperty('voice', voice.id)
        engine.setProperty('rate', rate + 50)
        engine.setProperty('volume', volume + 1.9)
        engine.say('hello world')
    engine.runAndWait()


def win_say():
    speaker = win32com.client.Dispatch('SAPI.SpVoice')
    speaker.Speak('你好啊 世界')


def txt_say():
    file = open('E:\\py\\day16\\test.txt', encoding='UTF-8')
    line = file.readline()
    engine = pyttsx3.init()
    while line:
        print(line, end='')
        engine.say(line)
        line = file.readline()
    engine.runAndWait()
    file.close()


""" 你的百度 APPID AK SK
https://console.bce.baidu.com/ai/#/ai/speech/app/list       应用列表
http://ai.baidu.com/docs#/TTS-Online-Python-SDK/top         API
"""


def du_say():
    app_id = '208522'
    api_key = 'sYi4GIqdPrzC4K80IFvA29pD'
    secret_key = 'rhF5SHsEuUAz3cs3TgTpj4jllTn11gFG'
    client = AipSpeech(app_id, api_key, secret_key)
    txt = '床前明月光，疑是地上霜'
    result = client.synthesis(txt, 'zh', 1, {'vol': 5})
    # 识别正确返回语音二进制 错误则返回dict
    if not isinstance(result, dict):
        with open('E:\\py\\day16\\test.mp3', 'xb') as f:
            f.write(result)
    playsound('E:\\py\\day16\\test.mp3')


# 文字转语音
if __name__ == '__main__':
    # say()
    # win_say()
    # txt_say()
    du_say()
