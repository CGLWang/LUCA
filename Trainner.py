import cv2
import os
import numpy as np
from PIL import Image
import time

recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')


def get_images_and_labels():
    '''

    :return: face_samples, ids
    '''
    face_cascade = cv2.CascadeClassifier('facebook/haarcascade_frontalface_default.xml')
    image_paths = []
    path = 'Pictures/Known/'
    face_samples = []
    ids = []

    for file in os.listdir(path):
        image_paths.append(os.path.join(path, file))
    for image_path in image_paths:
        img = Image.open(image_path).convert('L')
        img_np = np.array(img, 'uint8')
        id = os.path.split(image_path)[1].split('_')[0]
        face = face_cascade.detectMultiScale(img_np)
        for (x, y, w, h) in face:
            face_samples.append(img_np[y:y + h, x:x + w])
            ids.append(id)
    return face_samples, ids


print('Trainning...')
face_samples, ids = get_images_and_labels()
t0 = time.time()
ids = np.array([1]*len(face_samples))
recognizer.train(face_samples, ids)

t =( time.time() - t0)*1000
print("time comsumed:%.2fms"%t)
recognizer.save('facebook/trainner.xml')
