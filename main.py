import cv2 as cv
import numpy as np
import time
import os


yourname = input('Please input your name:')
name_exist = False
m = 1

if os.path.exists('facebook/dictionary.npy'):
    read_dictionary_obj = np.load('facebook/dictionary.npy', allow_pickle=True)    # 此时读出的数据是object类型，不能直接用作字典操作
    read_dictionary = read_dictionary_obj[()]   # 把object类型转化为字典
    for key in read_dictionary:
        if yourname == key:
            print(key+':'+str(read_dictionary[key]))
            name_exist = True
            m = read_dictionary[key]
            break
    if not name_exist:
        read_dictionary[yourname] = m + 1
        np.save('facebook/dictionary.npy', read_dictionary)
else:
    dictionary={yourname: m}
    np.save('facebook/dictionary.npy', dictionary)

face_cascade = cv.CascadeClassifier(r'facebook\haarcascade_frontalface_default.xml')
# 打开摄像机
camera = cv.VideoCapture(0)
# 创建窗口
cv.namedWindow('window')

# 以下为人脸识别代码，该函数只实现拍照功能，人脸识别功能在Trainner.py里实现
# n = 1
# while(n <= 50):    # 拍50张照片
#     # 拍一张照片
#     success, img = camera.read()  # success：拍摄是否成功    img：拍摄的图片
#     if success:
#         img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # 图片转成灰色
#         face = face_cascade.detectMultiScale(img_gray, 1.1, 3)  # 识别人脸
#         for (x, y, w, h) in face:
#             cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 框出人脸
#             cv.imwrite('Pictures\\Known\\'+yourname+'_'+str(n)+'.jpg', img)
#             n += 1
#             cv.imshow('window', img)    # 显示框出人脸的图片

n = 1
while(n <= 50):
    success, img = camera.read()  # success：拍摄是否成功    img：拍摄的图片
    if success:
        cv.imwrite('Pictures\\Known\\' + yourname + '_' + str(n) + '.jpg', img)
        n += 1
print('拍照完成，即将退出...')
time.sleep(2)
camera.release()
cv.destroyAllWindows()