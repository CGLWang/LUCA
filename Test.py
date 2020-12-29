import os
import cv2
from PIL import Image
import numpy as np

# image_paths = []
# path = 'Pictures/Known/'
# for file in os.listdir(path):
#     print(file)
#     image_paths.append(os.path.join(path, file))
#
# for image_path in image_paths:
#     print(image_path)

# print(os.path.split('Pictures/Known/pm_1.jpg')[1].split('_')[0])

# img = Image.open('Pictures/Known/pm_1.jpg').convert('L')
# img_np = np.array(img, 'uint8')
# print(img_np)

# recognizer = cv2.face.LBPHFaceRecognizer_create()
# recognizer.train()

face_cascade = cv2.CascadeClassifier('facebook/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
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
recognizer.train(face_samples, np.array(ids))
