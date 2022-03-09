from __future__ import unicode_literals
from wxpy import *
import sys

# 触发 微信告警通知
if (len(sys.argv)) == 4:
    bot = Bot('bot.pk1')
    alarm_group = bot.groups().search('相亲相爱一家人')[0]
    message = '项目名：{type},日志路径：{path},详细信息：{message}'.format(type=sys.argv[1], path=sys.argv[2], message=sys.argv[3])
    alarm_group.send(message)
