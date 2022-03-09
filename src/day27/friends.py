import time
import jieba
import logging
import numpy as np
from PIL import Image
from wordcloud import WordCloud
from WechatPCAPI import WechatPCAPI

logging.basicConfig(level=logging.INFO)


def on_message(message):
    pass


def get_friends():
    # 初始化微信实例
    wx_inst = WechatPCAPI(on_message=on_message, log=logging)
    # 启动微信
    wx_inst.start_wechat(block=True)
    # 等待登陆成功，此时需要人为扫码登录微信
    while not wx_inst.get_myself():
        time.sleep(5)
    print('登陆成功')
    nicknames = []
    # 排除的词
    remove = ['还是', '不会', '一些', '所以', '果然',
              '起来', '东西', '为什么', '真的', '这么',
              '但是', '怎么', '还是', '时候', '一个',
              '什么', '自己', '一切', '样子', '一样',
              '没有', '不是', '一种', '这个', '为了'
              ]
    for key, value in wx_inst.get_friends().items():
        if key in ['fmessage', 'floatbottle', 'filehelper'] or 'chatroom' in key:
            continue
        nicknames.append(value['wx_nickname'])
    words = []
    for text in nicknames:
        if not text:
            continue
        for t in jieba.cut(text):
            if t in remove:
                continue
            words.append(t)
    global word_cloud
    # 用逗号隔开词语
    word_cloud = '，'.join(words)


def nk_cloud():
    # 打开词云背景图
    cloud_mask = np.array(Image.open('bg.png'))
    # 定义词云的一些属性
    wc = WordCloud(
        # 背景图分割颜色为白色
        background_color='white',
        # 背景图样
        mask=cloud_mask,
        # 显示最大词数
        max_words=300,
        # 显示中文
        font_path='./fonts/simkai.ttf',
        # 最大尺寸
        max_font_size=70
    )
    global word_cloud
    # 词云函数
    x = wc.generate(word_cloud)
    # 生成词云图片
    image = x.to_image()
    # 展示词云图片
    image.show()
    # 保存词云图片
    wc.to_file('nk.png')


if __name__ == '__main__':
    get_friends()
    nk_cloud()
