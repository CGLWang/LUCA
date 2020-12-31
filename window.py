import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from windowQt import Ui_MainWindow
from Input import Ui_Dialog
import cv2 as cv
import xml.etree.ElementTree as ET
import time
import os
import _thread

recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read('facebook/trainner.xml')
face_cascade = cv.CascadeClassifier('facebook/haarcascade_frontalface_default.xml')
font = cv.FONT_HERSHEY_SIMPLEX
names = ['初始']

tree = ET.parse('facebook/dictionary.xml')
root = tree.getroot()
for face in root:
    names.append(face.attrib['name'])

class MyPyQT_Form(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyPyQT_Form, self).__init__()
        self.timer_camera = QtCore.QTimer()
        self.timer_recognize = QtCore.QTimer()
        self.camera = cv.VideoCapture(0)
        self.begin_recognize = False
        self.setupUi(self)
        self.slot_ca()
    def slot_ca(self):
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_recognize.timeout.connect(self.recognize)
    def show_camera(self):
        success, img = self.camera.read()
        if success:
            show = cv.resize(img,(640,480))     #把读到的帧的大小重新设置为 640x480
            # cv.imwrite('camera/' + 'img.jpg', show)
            if self.begin_recognize:
                img_gray = cv.cvtColor(show, cv.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(img_gray, 1.1, 5)
                for (x, y, w, h) in faces:
                    cv.rectangle(show, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    idnum, confidence = recognizer.predict(img_gray[y: y+h, x: x+w])
                    if confidence<100:
                        idum = names[idnum]
                        confidence = "{0}%".format(round(100-confidence))
                    else:
                        idum = 'unknown'
                        confidence = "{0}%".format(round(100 - confidence))
                    cv.putText(show, str(idum), (x + 5, y - 5), font, 1, (0, 0, 255), 1)
                    cv.putText(show, str(confidence), (x + 5, y + h - 5), font, 1, (255, 0, 0), 1)
            show = cv.cvtColor(show, cv.COLOR_BGR2RGB)
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            self.label_2.setPixmap(QtGui.QPixmap.fromImage(showImage))
    def recognize(self):
        pass
        # os.system('Recognize.py')
    def Button1_Clicked(self):
        if self.pushButton.text() == '打开摄像头':
            self.pushButton.setText('关闭摄像头')
            self.timer_camera.start(10)
        else:
            self.pushButton.setText('打开摄像头')
    def Button2_Clicked(self):
        self.begin_recognize = True

    def Button3_Clicked(self):
        self.textBrowser.append("你点击了按钮3")

class Input_Name(QDialog, Ui_Dialog):
    def __init__(self):
        super(Input_Name, self).__init__()
        self.setupUi(self)
    def Button1_Clicked(self):
        if self.textEdit.toPlainText() != '':
            self.close()
            return self.textEdit.toPlainText()
        else:
            QMessageBox.warning(self, '警告', '请输入姓名', QMessageBox.Yes | QMessageBox.No)
    def Button2_Clicked(self):
        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
