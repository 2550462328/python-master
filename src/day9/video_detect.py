# -*- coding: utf-8 -*-
import os
import cv2
import sys
import importlib

importlib.reload(sys)


# 返回当前视频中的人脸数量
def detect_video_face(video_path):
    # 指定视频流 可以是 存储视频 / 实时监控视频  / 网络流
    video_capture = cv2.VideoCapture(video_path)
    face_cascade = cv2.CascadeClassifier(os.getcwd() + "\\haarcascade\\haarcascade_frontalface_alt2.xml")
    count = 0

    # 逐帧读取
    while video_capture.isOpened():
        # 读取的 帧
        ok, iread = video_capture.read()
        if not ok:
            break
        grey = cv2.cvtColor(iread, cv2.COLOR_BGR2GRAY)
        face_detect = face_cascade.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        if len(face_detect) > 0:
            count += 1
    return count


# 截取视频中的人脸图
def video_screenshot(window_name, video_path, max_catch_num, catch_name_prefix):
    cv2.namedWindow(window_name)
    # 指定视频流 可以是 存储视频 / 实时监控视频 / 网络流
    # 存储视频
    # video_capture = cv2.VideoCapture(video_path)
    # 电脑实时监控视频
    video_capture = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(os.getcwd() + "\\haarcascade\\haarcascade_frontalface_alt2.xml")
    count = 0

    # 逐帧读取
    while video_capture.isOpened():
        # 读取的 帧
        ok, iread = video_capture.read()
        if not ok:
            break
        grey = cv2.cvtColor(iread, cv2.COLOR_BGR2GRAY)
        face_detects = face_cascade.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        if len(face_detects) > 0:
            for face_detect in face_detects:
                x, y, w, h = face_detect

                # 将当前帧保存为图片
                img_name = '%s/%d.jpg' % (catch_name_prefix, count)
                screenshot_img = iread[y - 10:y + h + 10, x - 10:x + w + 10]
                cv2.imwrite(img_name, screenshot_img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])

                count += 1
                if count >= max_catch_num:
                    break
                # 画出矩形框
                cv2.rectangle(iread, (x - 10, y - 10), (x + w + 10, y + h + 10), (0, 255, 0), 2)

                # 提示当前已经捕捉了 多少张人脸
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(iread, 'num:%d/100' % count, (x + 30, y + 30), font, 1, (255, 0, 255), 4)

        if count > max_catch_num:
            break
        # 显示截图画像
        cv2.imshow(window_name, iread)
        key = cv2.waitKey(10)

        if key & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # video_face_count = detect_video_face('E:\\py\\day9\\video\\xiaojiejie.mp4')
    # if video_face_count > 0:
    #     print('监控视频发现人脸')
    # else:
    #     print('监控区域未发现人脸')
    video_screenshot('监控视频区域', 'E:\\py\\day9\\video\\xiaojiejie.mp4', 100, 'E:\\py\\day9\\video\\screenshot')
