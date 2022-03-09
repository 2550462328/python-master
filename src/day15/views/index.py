from django.shortcuts import render
import os
from utils.qr_code import decode_qr_code
from django.views.decorators.csrf import csrf_exempt


def main(request):
    return render(request, 'index.html')


# 上传文件 -》 读取文件 -》 保存文件 -》 解析文件
@csrf_exempt
def upload(request):
    img = request.FILES.get('img'),
    name = img[0].name
    print(name)
    # 'r'       open for reading (default)
    # 'w'       open for writing, truncating the file first
    # 'x'       create a new file and open it for writing
    # 'a'       open for writing, appending to the end of the file if it exists
    # 'b'       binary mode
    # 't'       text mode (default)
    # '+'       open a disk file for updating (reading and writing)
    # 'U'       universal newline mode (deprecated)
    f = open(os.path.join('static\\images', name), 'xb')

    for chunk in img[0].chunks():
        f.write(chunk)
    f.close()
    result = decode_qr_code(os.path.join('static\\images', name))
    print(result)
    if len(result):
        context = {'context': result[0].data.decode('utf-8')}
    else:
        context = {'context': '请上传正确的二维码'}
    return render(request, 'show.html', context)
