from imutils.perspective import four_point_transform
# imutils 图像处理函数
from imutils import contours
# 支持大量的维度数组与矩阵运算
import numpy as np
import cv2 as cv


def main():
    ANSEWER_KEY_SCORE = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}
    ANSEWER_CORRECT_OPTION = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}

    img = cv.imread('E:\\py\\day12\\test01.jpg')
    # cv.imshow('origin', img)

    grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # cv.imshow('grey', grey)

    # 高斯模糊
    blur = cv.GaussianBlur(grey, (5, 5), 0)
    # cv.imshow('gaussianBlur', blur)

    # 边缘检测,灰度值小于第2个参数这个值的会被丢弃，大于第三个参数这个值会被当成边缘，在中间的部分，自动检测
    edge = cv.Canny(blur, 75, 200)
    # cv.imshow('edge', edge)

    # 寻找轮廓
    cts, hierarchy = cv.findContours(edge.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # cv.drawContours(img, cts, -1, (0, 0, 255), 3)

    print('寻找轮廓的个数:' + str(len(cts)))

    sort_list = sorted(cts, key=cv.contourArea, reverse=True)

    # cv.imshow('drawContours', img)

    # 正确的个数
    correct_count = 0

    for c in sort_list:
        # 求周长，第一个参数是轮廓，第二个参数是否是闭环
        peri = 0.01 * cv.arcLength(c, True)
        # 求多边形的定点，如果有4个定点，就代表是矩形
        approx = cv.approxPolyDP(c, peri, True)
        print('定点个数:', len(approx))

        if len(approx) == 4:
            # 透视交换 获取 轮廓后的原文内容
            origin_ox = four_point_transform(img, approx.reshape(4, 2))
            grey_ox = four_point_transform(grey, approx.reshape(4, 2))

            # cv.imshow('origin_ox', origin_ox)
            # cv.imshow('grey_ox', grey_ox)

            # 使用ostu二值化算法对灰度图做一个二值化处理
            ret, thresh2 = cv.threshold(grey_ox, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
            # cv.imshow('otsu', thresh2)

            # 继续寻找轮廓
            r_cnt, r_hierarchy = cv.findContours(thresh2.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            print('找到轮廓个数:' + str(len(r_cnt)))
            # cv.drawContours(origin_ox, r_cnt, -1, (0, 0, 255), 2)

            question_contours = []

            for cxx in r_cnt:
                x, y, w, h = cv.boundingRect(cxx)
                ar = w / float(h)

                if w >= 20 and h >= 20 and 0.9 <= ar <= 1.1:
                    question_contours.append(cxx)

            cv.imshow('cv_ox1', origin_ox)
            # 按坐标从上到下排序
            sort_question_contours = contours.sort_contours(question_contours, method='top-to-bottom')[0]

            for (q, i) in enumerate(np.arange(0, len(sort_question_contours), 5)):
                sort_question_contours_sub = contours.sort_contours(question_contours[i:i + 5])[0]

                bubble_rows = []

                for (j, k) in enumerate(sort_question_contours_sub):
                    # 生成一个大小与透视图一样的全黑背景图布
                    mask = np.zeros(grey_ox.shape, dtype='uint8')
                    # 将指定的轮廓 + 白色的填充写到画板上, 255代表亮度值，亮度 = 255的时候，颜色是白色，等于0的时候是黑色
                    cv.drawContours(mask, [k], -1, 255, -1)
                    # 做两个图片做位运算，把每个选项独自显示到画布上，为了统计非0像素值使用，这部分像素最大的其实就是答案
                    mask = cv.bitwise_and(thresh2, thresh2, mask=mask)
                    # 获取每个答案的像素值
                    total = cv.countNonZero(mask)

                    bubble_rows.append((total, j))

                bubble_rows = sorted(bubble_rows, key=lambda x: x[0], reverse=True)
                choice_num = bubble_rows[0][1]

                print('答案：{}，数据：{}'.format(ANSEWER_CORRECT_OPTION.get(choice_num), bubble_rows))

                if ANSEWER_KEY_SCORE.get(q) == choice_num:
                    # 正确 绿色
                    fill_color = (0, 255, 0)
                    correct_count = correct_count + 1
                else:
                    # 错误 红色
                    fill_color = (0, 0, 255)

                cv.drawContours(origin_ox, sort_question_contours_sub[choice_num], -1, fill_color, 2)
            cv.imshow('answer_flagged', origin_ox)

            text1 = 'total:' + str(len(ANSEWER_CORRECT_OPTION)) + ''
            text2 = 'right:' + str(correct_count)
            text3 = 'score:' + str(correct_count * 1.0 / len(ANSEWER_CORRECT_OPTION) * 100) + ''

            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(origin_ox, text1 + ' ' + text2 + ' ' + text3, (10, 30), font, 0.5, (0, 0, 255), 2)

            cv.imshow('score', origin_ox)

            break
    # 阻塞 等待窗体关闭
    cv.waitKey(0)


# 扫描答题卡，标记错误答案，统计得分
# 识别 涂抹部分 获取 涂抹的 原始内容
if __name__ == '__main__':
    main()
