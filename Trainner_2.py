import cv2
import os
import numpy as np
from PIL import Image
import xml.etree.ElementTree as ET
import shutil

recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier('facebook/haarcascade_frontalface_default.xml')

def get_images_and_labels(path):
    image_paths = []
    # face_samples = []
    # the_names = []
    for file in os.listdir(path):
        image_paths.append(os.path.join(path, file))
    for image_path in image_paths:
        img = Image.open(image_path).convert('L')
        img_np = np.array(img, 'uint8')
        face = face_cascade.detectMultiScale(img_np)
        for (x, y, w, h) in face:
            face_sample = img_np[y:y + h, x:x + w]
            # face_samples.append(face_sample)
            the_name = os.path.split(image_path)[1].split('.')[0]
            # the_names.append(the_name.split('_')[0])
            np.savetxt('facebook/txt_file/face_sample_'+the_name+'.txt', face_sample)

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