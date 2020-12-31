import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from windowQt import Ui_MainWindow
from Input import Ui_Dialog
import cv2 as cv
import xml.etree.ElementTree as ET
import shutil
import time
import os
import _thread

recognizer = cv.face.LBPHFaceRecognizer_create()
face_cascade = cv.CascadeClassifier('facebook/haarcascade_frontalface_default.xml')
font = cv.FONT_HERSHEY_SIMPLEX
names = ['初始']
yourname = ''

def find_dic_name(yourname):
    name_exist = False
    m = 1
    if os.path.exists('facebook/dictionary.xml'):
        tree = ET.parse('facebook/dictionary.xml')
        root = tree.getroot()
        for face in root:
            if face.attrib['name'] == yourname:
                print(face.attrib['name'] + ':' + face.attrib['label'])
                name_exist = True
                break
        m = len(root)
        if not name_exist:
            print(yourname + ':' + str(m + 1))
            new_node = ET.Element('face', {'name': yourname, 'label': str(m + 1)})
            root.append(new_node)
            tree.write('facebook/dictionary.xml')
    else:
        root = ET.Element('facebook')
        new_node = ET.SubElement(root, 'face', {'name': yourname, 'label': str(m)})
        tree = ET.ElementTree(root)
        tree.write('facebook/dictionary.xml', encoding='utf-8', xml_declaration=True)

class Input_Name(QDialog, Ui_Dialog):
    def __init__(self):
        super(Input_Name, self).__init__()
        self.setupUi(self)
    def Button1_Clicked(self):
        if self.textEdit.toPlainText() != '':
            global yourname
            yourname = self.textEdit.toPlainText()
            self.close()
            return yourname
        else:
            QMessageBox.warning(self, '警告', '请输入姓名', QMessageBox.Yes | QMessageBox.No)
    def Button2_Clicked(self):
        self.close()

class MyPyQT_Form(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyPyQT_Form, self).__init__()
        self.timer_camera = QtCore.QTimer()
        self.camera = cv.VideoCapture(0)
        self.begin_recognize = False
        self.begin_take_photo = False
        self.path = ''
        self.yourname = ''
        self.num = 1
        self.setupUi(self)
        self.slot_ca()
    def slot_ca(self):
        self.timer_camera.timeout.connect(self.show_camera)
    def show_camera(self):
        success, img = self.camera.read()
        if success:
            show = cv.resize(img, (640, 480))     #把读到的帧的大小重新设置为 640x480
            if self.begin_take_photo:
                if self.num <= 50:
                    cv.imwrite(self.path + '/' + self.yourname + '_' + str(self.num) + '.jpg', show)
                    self.num += 1
                else:
                    global yourname
                    self.num = 1
                    self.label_3.setText(yourname + '人脸录制完成！！！')
                    yourname = ''
                    self.begin_take_photo = False
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
    def Button1_Clicked(self):
        if self.pushButton.text() == '打开摄像头':
            self.pushButton.setText('关闭摄像头')
            self.timer_camera.start(10)
        else:
            self.timer_camera.stop()
            self.pushButton.setText('打开摄像头')
    def Button2_Clicked(self):
        if self.pushButton_2.text() == '识别人脸':
            self.pushButton.setText('停止识别')
            tree = ET.parse('facebook/dictionary.xml')
            root = tree.getroot()
            for face in root:
                names.append(face.attrib['name'])
            recognizer.read('facebook/trainner.xml')
            self.begin_recognize = True
        else:
            self.begin_recognize = False

            self.pushButton.setText('识别人脸')
    def Button3_Clicked(self):
        if self.pushButton.text() == '打开摄像头':
            QMessageBox.warning(self, '警告', '请先打开摄像头', QMessageBox.Yes | QMessageBox.No)
        else:
            input_name = Input_Name()
            input_name.exec_()  # 这两行为调出输入姓名的窗口
            global yourname
            if yourname != '':
                self.yourname = yourname     # 得到录制的人的姓名
                find_dic_name(self.yourname)     # 查看dictionary.xml文件里是否有该人
                self.path = 'Pictures/Photo/' + self.yourname
                if os.path.exists(self.path):
                    shutil.rmtree(self.path)
                os.mkdir(self.path)
                self.label_3.setText('请勿离开摄像头\n人脸录制中......')
                self.begin_take_photo = True

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
