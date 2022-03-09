import json
import numpy as np


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


# 在python3.x中 对 json数据 编码 / 解码 需要指定 解析器  否则会报错
if __name__ == '__main__':
    dic = {'id': 1, 'title': b'\xe7\xac\xac\xe4\xb8\x80\xe7\xab\xa0 \xe7\xa7\xa6\xe7\xbe\xbd'}
    # dum = json.dumps(dic, ensure_ascii=False)
    # 编码
    dum = json.dumps(dic, cls=MyEncoder, ensure_ascii=True, indent=4)
    # 解码
    # load = json.loads(dum)
    # print(load)
    print(dum)
