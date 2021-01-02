import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from windowQt import Ui_MainWindow
from Input import Ui_Dialog
import cv2 as cv
import xml.etree.ElementTree as ET
import shutil
import numpy as np
from PIL import Image
import time
import os
import _thread

recognizer = cv.face.LBPHFaceRecognizer_create()
face_cascade = cv.CascadeClassifier('facebook/haarcascade_frontalface_default.xml')
font = cv.FONT_HERSHEY_SIMPLEX
names = ['初始']
yourname = ''

def find_dic_name(yourname, window):
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
    _thread.start_new_thread(trainner, (window,))

def trainner(window):
    def get_images_and_labels(path):
        image_paths = []
        for file in os.listdir(path):
            image_paths.append(os.path.join(path, file))
        for image_path in image_paths:
            img = Image.open(image_path).convert('L')
            img_np = np.array(img, 'uint8')
            face = face_cascade.detectMultiScale(img_np)
            for (x, y, w, h) in face:
                face_sample = img_np[y:y + h, x:x + w]
                the_name = os.path.split(image_path)[1].split('.')[0]
                np.savetxt('facebook/txt_file/face_sample_' + the_name + '.txt', face_sample)

    Photo_dirs = 'Pictures/Photo'
    for Photo_dir in os.listdir(Photo_dirs):
        get_images_and_labels(Photo_dirs + '/' + Photo_dir)
        if os.path.exists('Pictures/Known/' + Photo_dir):
            shutil.rmtree('Pictures/Known/' + Photo_dir)
        shutil.copytree(Photo_dirs + '/' + Photo_dir, 'Pictures/Known/' + Photo_dir)
        shutil.rmtree(Photo_dirs + '/' + Photo_dir)

    ids = []
    face_samples = []
    the_names = []
    for file in os.listdir('facebook/txt_file'):
        face_samples.append(np.loadtxt('facebook/txt_file/' + file))
        the_names.append(file.split('_')[2])
    tree = ET.parse('facebook/dictionary.xml')
    root = tree.getroot()
    for the_name in the_names:
        for face in root:
            if the_name == face.attrib['name']:
                ids.append(int(face.attrib['label']))
    recognizer.train(face_samples, np.array(ids))
    recognizer.save('facebook/trainner.xml')
    recognizer.read('facebook/trainner.xml')
    window.label_5.setText('人脸数据训练完成！！！')
    if window.textBrowser.toPlainText().find(window.yourname) == -1:
        window.textBrowser.append(window.yourname)
    window.yourname = ''
    window.pushButton.setEnabled(True)
    window.pushButton_2.setEnabled(True)
    window.pushButton_3.setEnabled(True)
    window.pushButton_4.setEnabled(False)
    window.pushButton_5.setEnabled(False)

def text_browser_add(window):
    if os.path.exists('facebook/dictionary.xml'):
        tree = ET.parse('facebook/dictionary.xml')
        root = tree.getroot()
        for face in root:
            window.textBrowser.append(face.attrib['name'])

class Input_Name(QDialog, Ui_Dialog):
    def __init__(self):
        super(Input_Name, self).__init__()
        self.setupUi(self)
    def Button1_Clicked(self):
        have_hanzi = False
        if self.lineEdit.text() != '':
            global yourname
            yourname = self.lineEdit.text()
            for yourname_c in yourname:
                if '\u4e00' <= yourname_c <= '\u9fa5':
                    have_hanzi = True
            if have_hanzi:
                QMessageBox.warning(self, '警告', '名字里请不要有汉字', QMessageBox.Yes | QMessageBox.No)
            else:
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
        self.take_photo_success = False
        self.path = ''
        self.yourname = ''
        self.num = 1
        self.photo_num = 1
        self.setupUi(self)
        self.slot_ca()
    def slot_ca(self):
        _thread.start_new_thread(text_browser_add, (self, ))
        self.timer_camera.timeout.connect(self.show_camera)
    def show_camera(self):
        success, img = self.camera.read()
        if success:
            show = cv.resize(img, (640, 480))     #把读到的帧的大小重新设置为 640x480
            if self.begin_take_photo:
                if self.radioButton.isChecked():
                    self.photo_num = 20
                elif self.radioButton_2.isChecked():
                    self.photo_num = 50
                else:
                    self.photo_num = 200
                if self.num <= self.photo_num:
                    cv.imwrite(self.path + '/' + self.yourname + '_' + str(self.num) + '.jpg', show)
                    # os.system('Trainner_2.py') # 可以在这里直接训练数据，但是这会导致程序卡住几秒（卡住的这几秒是训练数据要的时间），这会导致程序不友好
                    show = cv.cvtColor(show, cv.COLOR_BGR2RGB)
                    showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
                    self.label_4.setPixmap(QtGui.QPixmap.fromImage(showImage))
                    self.label_5.setText('是否以这张图片作为人脸识别的依据？')
                    self.pushButton.setEnabled(False)
                    self.pushButton_2.setEnabled(False)
                    self.pushButton_3.setEnabled(False)
                    self.pushButton_4.setEnabled(True)
                    self.pushButton_5.setEnabled(True)
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
            self.label_2.setPixmap(QtGui.QPixmap(''))
            self.timer_camera.stop()
            self.pushButton.setText('打开摄像头')
    def Button2_Clicked(self):
        if self.pushButton_2.text() == '识别人脸':
            if self.textBrowser.toPlainText() == '':
                QMessageBox.warning(self, '警告', '数据库里还没有人脸数据，请先输入人脸！！！', QMessageBox.Yes | QMessageBox.No)
            else:
                self.pushButton_2.setText('停止识别')
                tree = ET.parse('facebook/dictionary.xml')
                root = tree.getroot()
                for face in root:
                    names.append(face.attrib['name'])
                recognizer.read('facebook/trainner.xml')
                self.begin_recognize = True
        else:
            self.begin_recognize = False
            self.pushButton_2.setText('识别人脸')
    def Button3_Clicked(self):
        if self.pushButton.text() == '打开摄像头':
            QMessageBox.warning(self, '警告', '请先打开摄像头', QMessageBox.Yes | QMessageBox.No)
        else:
            input_name = Input_Name()
            input_name.exec_()  # 这两行为调出输入姓名的窗口
            global yourname
            if yourname != '':
                self.yourname = yourname     # 得到录制的人的姓名
                self.path = 'Pictures/Photo/' + self.yourname
                if os.path.exists(self.path):
                    shutil.rmtree(self.path)
                os.mkdir(self.path)
                self.label_3.setText('请勿离开摄像头\n人脸录制中......')
                self.begin_take_photo = True
    def Button4_Clicked(self):
        self.label_5.setText('正在训练'+self.yourname+'的人脸数据，请稍后...')
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        if self.yourname != '':
            _thread.start_new_thread(find_dic_name, (self.yourname, self, ))
    def Button5_Clicked(self):
        QMessageBox.warning(self, '警告', '你选择了取消！', QMessageBox.Yes | QMessageBox.No)
        self.label_4.setPixmap(QtGui.QPixmap(''))
        shutil.rmtree('Pictures/Photo/' + self.yourname)
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
    def Button6_Clicked(self):
        QMessageBox.information(self, '帮助', '普通识别：拍20张照片作基准\n\n较精准识别：拍50张照片作基准\n\n精准识别：拍200张照片作基准', QMessageBox.Yes | QMessageBox.No)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
