import codecs
import time
import os

from aip import AipSpeech
from django.http import HttpResponse
from django.shortcuts import render


def main(request):
    return render(request, 'm_index.html')


def m_main(request):
    return render(request, 'm_index.html')


def convert(request):
    message = request.POST.get('message')
    switch = request.POST.get('switch')
    mp3 = du_say(message, switch)
    return HttpResponse(mp3)


def du_say(message, switch):
    app_id = '208522'
    api_key = 'sYi4GIqdPrzC4K80IFvA29pD'
    secret_key = 'rhF5SHsEuUAz3cs3TgTpj4jllTn11gFG'
    client = AipSpeech(app_id, api_key, secret_key)
    if switch == 'true':
        switch = 3
    else:
        switch = 4
    result = client.synthesis(message, 'zh', 1, {'vol': 5, 'per': switch})
    t = time.time()
    now_time = lambda: int(round(t * 1000))
    # path = 'E:\\py\\day17\\audio\\'
    path = os.getcwd() + os.path.sep + "static" + os.path.sep + "audio" + os.path.sep
    audio = path + str(now_time()) + '.mp3'
    if not isinstance(result, dict):
        with open(audio, 'xb') as f:
            f.write(result)
    return str(now_time()) + '.mp3'


def write_txt(message):
    t = time.time()
    now_time = lambda: int(round(t * 1000))
    # path = 'E:\\py\\day17\\text\\'
    path = os.getcwd() + os.path.sep + "static" + os.path.sep + "audio" + os.path.sep
    text = path + str(now_time()) + '.txt'
    with codecs.open(text, 'a', encoding='utf8') as f:
        f.write(message)


if __name__ == '__main__':
    du_say('傻逼玩意儿', 'true')
