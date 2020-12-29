import cv2
import numpy as np
import dlib

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('facebook/trainner.xml')
face_cascade = cv2.CascadeClassifier('facebook/haarcascade_frontalface_default.xml')
font = cv2.FONT_HERSHEY_SIMPLEX


names = ['初始']
read_dictionary_obj = np.load('facebook/dictionary.npy', allow_pickle=True)    # 此时读出的数据是object类型，不能直接用作字典操作
read_dictionary = read_dictionary_obj[()]   # 把object类型转化为字典
for key in read_dictionary:
    names.append(key)

camera = cv2.VideoCapture(0)
while True:
    success, img = camera.read()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces =face_cascade.detectMultiScale(img_gray, 1.1, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        idnum, confidence = recognizer.predict(img_gray[y: y+h, x: x+w])
        if confidence<100:
            idum = names[idnum]
            confidence = "{0}%".format(round(100-confidence))
        else:
            idum = 'unknown'
            confidence = "{0}%".format(round(100 - confidence))
        cv2.putText(img, str(idum), (x + 5, y - 5), font, 1, (0, 0, 255), 1)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 0, 0), 1)
    cv2.namedWindow('window')
    cv2.imshow('window', img)
    k = cv2.waitKey(20)
    if k == 27:
        break
camera.release()
cv2.destroyAllWindows()