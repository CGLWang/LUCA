import cv2
import os
import numpy as np
from PIL import Image
import cv2.cv2 as cv22

recognizer = cv2.face.LBPHFaceRecognizer_create()

def get_images_and_labels():
    face_cascade = cv2.CascadeClassifier('facebook/haarcascade_frontalface_default.xml')
    image_paths = []
    path = 'Pictures/Known/'
    face_samples = []
    the_names = []

    for file in os.listdir(path):
        image_paths.append(os.path.join(path, file))
    for image_path in image_paths:
        img = Image.open(image_path).convert('L')
        img_np = np.array(img, 'uint8')
        face = face_cascade.detectMultiScale(img_np)
        for (x, y, w, h) in face:
            face_samples.append(img_np[y:y + h, x:x + w])
            the_names.append(os.path.split(image_path)[1].split('_')[0])
    return face_samples, the_names


print('Trainning...')
ids = []
face_samples, the_names = get_images_and_labels()
read_dictionary_obj = np.load('facebook/dictionary.npy', allow_pickle=True)    # 此时读出的数据是object类型，不能直接用作字典操作
read_dictionary = read_dictionary_obj[()]   # 把object类型转化为字典
for the_name in the_names:
    for key in read_dictionary:
        if the_name == key:
            ids.append(read_dictionary[key])

recognizer.train(face_samples, np.array(ids))
recognizer.save('facebook/trainner.yml')




