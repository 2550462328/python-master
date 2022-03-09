import cv2

# 读取图片
img = cv2.imread('E:\\py\\day9\\images\\heying.jpg')
# 打开新窗口
cv2.namedWindow('Image')
# 展示图片
cv2.imshow('Image', img)
cv2.waitKey(0)
