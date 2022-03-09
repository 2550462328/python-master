from __future__ import unicode_literals
from wxpy import *
from wechat_sender import listen

# 打开微信网页版监听
bot = Bot('bok.pk1')
listen(bot)
