import time
import logging
from queue import Queue
from WechatPCAPI import WechatPCAPI

logging.basicConfig(level=logging.INFO)
queue_recved_event = Queue()


def on_message(msg):
    queue_recved_event.put(msg)


def login():
    pre_msg = ''
    # 初始化微信实例
    wx_inst = WechatPCAPI(on_message=on_message, log=logging)
    # 启动微信
    wx_inst.start_wechat(block=True)
    # 等待登陆成功，此时需要人为扫码登录微信
    while not wx_inst.get_myself():
        time.sleep(5)
    print('登陆成功')
    while True:
        msg = queue_recved_event.get()
        data = msg.get('data')
        sendinfo = data.get('sendinfo')
        data_type = str(data.get('data_type'))
        msgcontent = str(data.get('msgcontent'))
        is_recv = data.get('is_recv')
        print(msg)
        if data_type == '1' and 'revokemsg' not in msgcontent:
            pre_msg = msgcontent
        if sendinfo is not None and 'revokemsg' in msgcontent:
            user = str(sendinfo.get('wx_id_search'))
            recall = '撤回的消息：' + pre_msg
            wx_inst.send_text(to_user=user, msg=recall)


if __name__ == '__main__':
    login()
