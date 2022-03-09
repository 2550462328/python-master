import os
import tempfile


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")  # 去除尾部 \ 符号

    # 判断路径是否存在
    # 存在 True
    # 不存在 False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + u' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + u' 目录已存在')
        return False


if __name__ == '__main__':
    file_path = u'E:\\py\\day29\\huizhang43'
    mkdir(file_path)
    # 临时文件目录  'C:\\Users\\huizhang43\\AppData\\Local\\Temp'
    temp_path = tempfile.gettempdir()
    # 当前脚本所在目录  'D:\\develop\\workspace\\workspace-python\\helloworld\\src\\day29\\file_util.py'
    realpath = os.path.realpath(__file__)
    # 文件名  'file_util.py'
    file_name = os.path.basename(realpath)
    # 文件目录  空（当前目录）
    file_path = os.path.dirname(realpath)
    # 文件扩展名 '.py'
    extension_name = os.path.splitext(realpath)[1]


