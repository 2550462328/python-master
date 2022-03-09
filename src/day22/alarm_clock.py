import json
import urllib.request

import pygame.mixer
from aip import AipSpeech


# 获取天气
def get_weather():
    url = 'http://www.weather.com.cn/data/cityinfo/101120201.html'
    obj = urllib.request.urlopen(url)
    data_origin = obj.read()
    data_decode = data_origin.decode('utf-8')
    data_json = json.loads(data_decode)
    rc = data_json['weatherinfo']
    weather_info = '青岛天气是 {} 到 {}, 天气是 {}'
    weather_info = weather_info.format(rc['temp1'], rc['temp2'], rc['weather'])
    if '雨' in weather_info:
        weather_info += ', 今日有小雨'
    du_say(weather_info)


# 百度sdk 文字转语音
def du_say(weather_info):
    app_id = '208522'
    api_key = 'sYi4GIqdPrzC4K80IFvA29pD'
    secret_key = 'rhF5SHsEuUAz3cs3TgTpj4jllTn11gFG'
    client = AipSpeech(app_id, api_key, secret_key)
    # per 3是汉子 4是妹子
    result = client.synthesis(weather_info, 'zh', 1, {'vol': 5, 'per': 3, 'spd': 4})
    file = 'E:\\py\\day22\\weather.mp3'
    # 识别正确返回语音二进制，错误返回dict
    if not isinstance(result, dict):
        with open(file, 'wb') as f:
            f.write(result)
    py_game_player(file)


# 播放天气和音乐
def py_game_player(file):
    pygame.mixer.init()
    print('播报天气')
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loops=1, start=0.0)
    print('播放音乐')
    while True:
        if pygame.mixer.music.get_busy() == 0:
            mp3 = 'E:\\py\\day22\\1.mp3'
            pygame.mixer.music.load(mp3)
            pygame.mixer.music.play(loops=1, start=0.0)
            break
    while True:
        if pygame.mixer.music.get_busy() == 0:
            print('起床啦')
            break


# 文字 转语音播放 可用于早起 时天气播报
if __name__ == '__main__':
    get_weather()
