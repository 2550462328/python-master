import os
import cv2
from PIL import Image, ImageDraw
from datetime import datetime


# 返回图像中所有人脸的矩形坐标（矩形左上、右下顶点）
# 使用haar特征的级联分类器haarcascade_frontalface_default.xml，在haarcascades目录下还有其他的训练好的xml文件可供选择。
# 注：haarcascades目录下训练好的分类器必须以灰度图作为输入。
def detect_faces(image_name):
    img = cv2.imread(image_name)
    face_cascade = cv2.CascadeClassifier(os.getcwd() + '\\haarcascade\\haarcascade_frontalface_alt.xml')
    # 如果img维度为3，说明不是灰度图，先转化为灰度图gray，如果不为3，也就是2，原图就是灰度图
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    # 1.3和5是特征的最小、最大检测窗口，它改变检测结果也会改变
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    result = []
    for (x, y, width, height) in faces:
        result.append((x, y, x + width, y + height))
    return result


# 保存人脸图
def save_face_img(image_name):
    faces = detect_faces(image_name)
    if faces:
        save_dir = image_name.split('.')[0] + '_faces'
        os.mkdir(save_dir)
        count = 0
        for (x1, y1, x2, y2) in faces:
            file_name = os.path.join(save_dir, str(count) + '.jpg')
            # Image.open获取图像句柄，crop剪切图像(剪切的区域就是detectFaces返回的坐标)，save保存
            Image.open(image_name).crop((x1, y1, x2, y2)).save(file_name)
            count += 1


# 标注人脸（画矩形）
def draw_face_rect(path, image_name):
    faces = detect_faces(path + image_name)
    if faces:
        img = Image.open(path + image_name)
        draw_instance = ImageDraw.Draw(img)
        for (x1, y1, x2, y2) in faces:
            draw_instance.rectangle((x1, y1, x2, y2), outline=(255, 0, 0))
        img.save(path + 'drawafaces_' + image_name)


# 返回 图片中 人眼的 上下顶点坐标
# 这里是基于人脸 识别 人眼的 当然也可以直接根据人眼的 级联分类器直接找到人眼的顶点坐标
def detect_eyes(image_name):
    eye_cascade = cv2.CascadeClassifier(os.getcwd() + '\\haarcascade\\haarcascade_eye.xml')
    faces = detect_faces(image_name)

    if faces:
        img = cv2.imread(image_name)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = []
        for (x1, y1, x2, y2) in faces:
            roi_gray = gray[y1:y2, x1:x2]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 2)
            for (ex, ey, ew, eh) in eyes:
                result.append((x1 + ex, y1 + ey, x1 + ex + ew, y1 + ey + eh))
            return result


# 标注人眼（画矩形）
def draw_eyes_rect(path, image_name):
    eyes = detect_eyes(path + image_name)
    if eyes:
        img = Image.open(path + image_name)
        draw_instance = ImageDraw.Draw(img)
        for (x1, y1, x2, y2) in eyes:
            draw_instance.rectangle((x1, y1, x2, y2), outline=(0, 0, 255))
        img.save(path + 'draweyes_' + image_name)


# 返回 图片中 笑脸的 上下顶点坐标
def detect_smiles(image_name):
    img = cv2.imread(image_name)
    smile_cascade = cv2.CascadeClassifier(os.getcwd() + '\\haarcascade\\haarcascade_smile.xml')
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    smiles = smile_cascade.detectMultiScale(gray, 4, 5)
    result = []
    for (x, y, width, height) in smiles:
        result.append((x, y, x + width, y + height))
    return result


# 标注笑脸（画矩形）
def draw_smiles_rect(path, image_name):
    smiles = detect_smiles(path + image_name)
    if smiles:
        img = Image.open(path + image_name)
        draw_instance = ImageDraw.Draw(img)
        for (x1, y1, x2, y2) in smiles:
            draw_instance.rectangle((x1, y1, x2, y2), outline=(100, 100, 0))
        img.save(path + 'drawsmiles_' + image_name)


if __name__ == '__main__':
    start_time = datetime.now()
    result = detect_faces('E:\\py\\day9\\images\\heying.jpg')
    end_time = datetime.now()
    print('耗时:' + str(end_time - start_time))
    if len(result) > 0:
        print('有人存在,人数为:' + str(len(result)))
    else:
        print('视图中没有人')

    # draw_face_rect('E:\\py\\day9\\images\\', 'heying.jpg')
    # save_face_img('E:\\py\\day9\\images\\heying.jpg')
    # draw_eyes_rect('E:\\py\\day9\\images\\', 'people.jpg')
    draw_smiles_rect('E:\\py\\day9\\images\\', 'people.jpg')
"""
上面的代码将眼睛、人脸、笑脸在不同的图像上框出，如果需要在同一张图像上框出，改一下代码就可以了。
总之，利用opencv里训练好的haar特征的xml文件，在图片上检测出人脸的坐标，利用这个坐标，我们可以将人脸区域剪切保存，也可以在原图上将人脸框出。剪切保存人脸以及用矩形工具框出人脸，本程序使用的是PIL里的Image、ImageDraw模块。
此外，opencv里面也有画矩形的模块，同样可以用来框出人脸。
"""
