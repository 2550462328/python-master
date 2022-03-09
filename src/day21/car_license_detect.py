import os
import cv2
import numpy as np
from tensorflow import keras
from util.CNN import cnn_predict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'h5')

location = keras.models.load_model(os.path.join(MEDIA_ROOT, 'location.h5'))  # 车牌定位
cnn = keras.models.load_model(os.path.join(MEDIA_ROOT, 'cnn.h5'))  # 车牌识别


# 图片预处理
def img_process(path):
    img = cv2.imread(path)
    # 统一规定大小
    img = cv2.resize(img, (640, 480))
    # 高斯模糊
    img_Gas = cv2.GaussianBlur(img, (5, 5), 0)
    # RGB通道分离
    img_B = cv2.split(img_Gas)[0]
    img_G = cv2.split(img_Gas)[1]
    img_R = cv2.split(img_Gas)[2]
    # 读取灰度图 和 HSV空间图
    img_gray = cv2.cvtColor(img_Gas, cv2.COLOR_BGR2GRAY)
    img_HSV = cv2.cvtColor(img_Gas, cv2.COLOR_BGR2HSV)
    return img, img_Gas, img_B, img_G, img_R, img_gray, img_HSV


# 初步识别
def pre_indetification(img_gray, img_HSV, img_B, img_R):
    for i in range(480):
        for j in range(640):
            # 普通蓝色车牌，同时排除透明反光物质的干扰
            if ((img_HSV[:, :, 0][i, j] - 115) ** 2 < 15 ** 2) and (img_B[i, j] > 70) and (img_R[i, j] < 40):
                img_gray[i, j] = 255
            else:
                img_gray[i, j] = 0
    # 定义核
    kernel_small = np.ones((3, 3))
    kernel_big = np.ones((7, 7))

    # 高斯平滑
    img_gray = cv2.GaussianBlur(img_gray, (5, 5), 0)
    # 腐蚀5次
    img_di = cv2.dilate(img_gray, kernel_small, iterations=5)
    # 闭操作
    img_close = cv2.morphologyEx(img_di, cv2.MORPH_CLOSE, kernel_big)
    # 高斯平滑
    img_close = cv2.GaussianBlur(img_close, (5, 5), 0)
    # 二值化
    _, img_bin = cv2.threshold(img_close, 100, 255, cv2.THRESH_BINARY)
    return img_bin


# 定位
def fix_position(img, img_bin):
    # 检测外轮廓,只留下矩形的四个顶点
    contours, _ = cv2.findContours(img_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # 形状和大小筛选校验
    det_x_max = 0
    det_y_max = 0
    num = 0
    for i in range(len(contours)):
        x_min = np.min(contours[i][:, :, 0])
        x_max = np.max(contours[i][:, :, 0])
        y_min = np.min(contours[i][:, :, 1])
        y_max = np.max(contours[i][:, :, 1])
        det_x = x_max - x_min
        det_y = y_max - y_min
        if (det_x / det_y > 1.8) and (det_x > det_x_max) and (det_y > det_y_max):
            det_y_max = det_y
            det_x_max = det_x
            num = i
    # 获取 最可疑区域轮廓点集
    points = np.array(contours[num][:, 0])
    return points


# 寻找顶点
def find_vertices(points):
    # 获取最小外接矩阵,中心点坐标,宽高,旋转角度
    rect = cv2.minAreaRect(points)
    # 获取 矩形的四个顶点,浮点型
    box = cv2.boxPoints(rect)
    # 取整
    box = np.int0(box)
    # 获取四个顶点坐标
    left_point_x = np.min(box[:, 0])
    right_point_x = np.max(box[:, 0])
    top_point_y = np.min(box[:, 1])
    bottom_point_y = np.max(box[:, 1])

    left_point_y = box[:, 1][np.where(box[:, 0] == left_point_x)][0]
    right_point_y = box[:, 1][np.where(box[:, 0] == right_point_x)][0]
    top_point_x = box[:, 0][np.where(box[:, 1] == top_point_y)][0]
    bottom_point_x = box[:, 0][np.where(box[:, 1] == bottom_point_y)][0]

    vertices = np.array([[top_point_x, top_point_y], [bottom_point_x, bottom_point_y], [left_point_x, left_point_y],
                         [right_point_x, right_point_y]])
    return vertices, rect


def tilt_correction(vertices, rect):
    # 畸变情况1:
    if rect[2] > -45:
        new_right_point_x = vertices[0, 0]
        new_right_point_y = int(vertices[1, 1] - (vertices[0, 0] - vertices[1, 0]) / (
                vertices[3, 0] - vertices[1, 0] * (vertices[1, 1] - vertices[3, 1])))
        new_left_point_x = vertices[1, 0]
        new_left_point_y = int(vertices[0, 1] + (vertices[0, 0] - vertices[1, 0]) / (
                vertices[0, 0] - vertices[2, 0] * (vertices[2, 1] - vertices[0, 1])))
        # 校正后的四个顶点坐标
        point_set_1 = np.float32([[440, 0], [0, 0], [0, 140], [440, 140]])
    # 畸变情况2
    elif rect[2] < -45:
        new_right_point_x = vertices[1, 0]
        new_right_point_y = int(vertices[0, 1] - (vertices[1, 0] - vertices[0, 0]) / (
                vertices[3, 0] - vertices[0, 0] * (vertices[3, 1] - vertices[0, 1])))
        new_left_point_x = vertices[0, 0]
        new_left_point_y = int(vertices[1, 1] - (vertices[1, 0] - vertices[0, 0]) / (
                vertices[1, 0] - vertices[2, 0] * (vertices[1, 1] - vertices[2, 1])))
        # 校正后的四个顶点坐标
        point_set_1 = np.float32([[0, 0], [0, 140], [440, 140], [440, 0]])

    new_box = np.array([(vertices[0, 0], vertices[0, 1]), (new_left_point_x, new_left_point_y),
                        (vertices[1, 0], vertices[1, 1]), (new_right_point_x, new_right_point_y)])
    point_set_0 = np.float32(new_box)
    return point_set_0, point_set_1, new_box


def transform(img, point_set_0, point_set_1):
    # 变化矩阵
    mat = cv2.getPerspectiveTransform(point_set_0, point_set_1)
    # 投影变换
    lic = cv2.warpPerspective(img, mat, (440, 140))
    return lic


# 截取车牌(蓝牌)
# 参考链接:https://www.cnblogs.com/HL-space/p/10588423.html
def main():
    path = 'E:\\py\\day21\\img\\0.jpg'
    # 图像预处理
    img, img_Gas, img_B, img_G, img_R, img_gray, img_HSV = img_process(path)
    # 初步识别
    img_bin = pre_indetification(img_gray, img_HSV, img_B, img_R)
    points = fix_position(img, img_bin)
    vertices, rect = find_vertices(points)
    point_set_0, point_set_1, new_box = tilt_correction(vertices, rect)
    img_draw = cv2.drawContours(img.copy(), [new_box], -1, (0, 0, 255), 3)
    lic = transform(img, point_set_0, point_set_1)
    # # 原图上框出车牌
    # cv2.namedWindow('Image')
    # cv2.imshow('Image', img_draw)
    # # 二值化图像
    # cv2.namedWindow('Image_Bin')
    # cv2.imshow('Image_Bin', img_bin)
    # # 显示校正后的车牌
    # cv2.namedWindow('Lic')
    # cv2.imshow('Lic', lic)
    # # 暂停等待关闭窗口
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    Lic_predict = cnn_predict(cnn, lic)  # 利用cnn进行车牌的识别预测,Lic_pred中存的是元祖(车牌图片,识别结果)
    license_plate = ""
    if Lic_predict:
        for i, lic in enumerate(Lic_predict):
            if i == 0:
                license_plate = lic[1]
            elif i == 1:
                license_plate = lic[1]
            elif i == 2:
                license_plate = lic[1]
        print("车牌号：" + license_plate)
    else:  # Lic_predict 为空说明未能识别
        print("未能识别")


if __name__ == '__main__':
    main()
