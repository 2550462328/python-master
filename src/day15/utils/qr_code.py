# -*- coding:utf-8 -*-
import os.path

import qrcode
from PIL import Image
from pyzbar import pyzbar


def make_qr_code_easy(content, save_path=None):
    img = qrcode.make(data=content)
    if save_path:
        img.save(save_path)
    else:
        img.show()


def make_qr_code(content, save_path=None):
    qr_code_maker = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=1)
    qr_code_maker.add_data(data=content)
    qr_code_maker.make(fit=True)
    img = qr_code_maker.make_image(fill_color='black', back_color='white')
    if save_path:
        img.save(save_path)
    else:
        img.show()


def make_qr_code_with_icon(content, icon_path, save_path=None):
    if not os.path.exists(icon_path):
        raise FileExistsError(icon_path)

    qr_code_maker = qrcode.QRCode(version=4, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=1)
    qr_code_maker.add_data(data=content)
    qr_code_maker.make(fit=True)
    qr_code_img = qr_code_maker.make_image(fill_color='black', back_color='white').convert('RGBA')

    icon_img = Image.open(icon_path)
    code_width, code_height = qr_code_img.size
    icon_img = icon_img.resize((code_width // 4, code_height // 4), Image.ANTIALIAS)

    qr_code_img.paste(icon_img, (code_width * 3 // 8, code_width * 3 // 8))

    if save_path:
        qr_code_img.save(save_path)
    else:
        qr_code_img.show()


def decode_qr_code(code_img_path):
    if not os.path.exists(code_img_path):
        raise FileExistsError(code_img_path)

    return pyzbar.decode(Image.open(code_img_path), symbols=[pyzbar.ZBarSymbol.QRCODE])


# 生成二维码 和 解析二维码
if __name__ == '__main__':
    # count = 0
    # for i in range(1, 33):
    #     file_path = 'E:\\py\\day13\\img\\' + str(i) + '.png'
    #     results = decode_qr_code(file_path)
    #     if len(results):
    #         print(results[0].data.decode('utf-8'))
    #     else:
    #         print('can not recognize : ' + file_path)
    #         count += 1
    # print('测试失败的数量：' + str(count))
    # make_qr_code_easy('张辉最帅', 'E:\\py\\day13\\1.png')
    # make_qr_code('张辉最帅', 'E:\\py\\day13\\2.png')
    make_qr_code_with_icon('张辉最帅', 'E:\\py\\day13\\icon.jpg', 'E:\\py\\day13\\3.png')
