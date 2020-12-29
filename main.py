import cv2 as cv
import time

yourname = input('Please input your name:')
face_cascade = cv.CascadeClassifier(r'facebook\haarcascade_frontalface_default.xml')
# 打开摄像机
camera = cv.VideoCapture(0)
# 创建窗口
cv.namedWindow('window')

n = 1
while(n <= 50):    # 拍50张照片
    # 拍一张照片
    success, img = camera.read()  # success：拍摄是否成功    img：拍摄的图片
    if success:
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # 图片转成灰色
        face = face_cascade.detectMultiScale(img_gray, 1.1, 3)  # 识别人脸
        for (x, y, w, h) in face:
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 框出人脸
            cv.imwrite('Pictures\\Known\\'+yourname+'_'+str(n)+'.jpg', img)
            n += 1
            cv.imshow('window', img)    # 显示框出人脸的图片
print('拍照完成，即将退出...')
time.sleep(2)
camera.release()
cv.destroyAllWindows()
