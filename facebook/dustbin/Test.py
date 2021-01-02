import os
import cv2
from PIL import Image
import numpy as np
import xml.etree.ElementTree as ET
import shutil

camera = cv2.VideoCapture(0)
success, img = camera.read()
if success:
    cv2.imwrite('彭敏.jpg', img)

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

# face_cascade = cv2.CascadeClassifier('facebook/haarcascade_frontalface_default.xml')
# recognizer = cv2.face.LBPHFaceRecognizer_create()
# image_paths = []
# path = 'Pictures/Known/'
# face_samples = []
# ids = []
#
# for file in os.listdir(path):
#     image_paths.append(os.path.join(path, file))
# for image_path in image_paths:
#     img = Image.open(image_path).convert('L')
#     img_np = np.array(img, 'uint8')
#     id = os.path.split(image_path)[1].split('_')[1].split('.')[0]
#     face = face_cascade.detectMultiScale(img_np)
#     for (x, y, w, h) in face:
#         face_samples.append(img_np[y:y + h, x:x + w])
#         ids.append(id)
# print(list(map(int, ids)))


# cc = np.load('facebook/dictionary.npy', allow_pickle=True)
# ccs = cc[()]
# for key in ccs:
#     print(ccs[key])

# thename = []
# thename.append(1)
# thename.append(2)
# thename.append(1)
# thename.append(3)
# thename.append(2)
# print(thename)
# print(np.array(thename))

# yourname = input('Please input your name:')
# name_exist = False
# m = 1
# if os.path.exists('facebook/dictionary.xml'):
#     tree = ET.parse('facebook/dictionary.xml')
#     root = tree.getroot()
#     for face in root:
#         print(face.attrib['name'])

# shutil.rmtree('Pictures/pm')
# shutil.rmtree('Pictures/pm2')

# for listdir in os.listdir('Pictures/'):
#     if 'Untrainned' in listdir:
#         print(listdir.split('_')[0])

# face_cascade = cv2.CascadeClassifier('facebook/haarcascade_frontalface_default.xml')
# image_path = 'Pictures/Known/pm2_1.jpg'
# img = Image.open(image_path).convert('L')
# img_np = np.array(img, 'uint8')
# face_sample = img_np
# face = face_cascade.detectMultiScale(img_np)
# for (x, y, w, h) in face:
#     face_sample = img_np[y:y + h, x:x + w]
#     print(face_sample)
#     np.savetxt('facebook/pm2.txt', face_sample)
#
# b = np.loadtxt('facebook/pm2.txt')
# print(b)
#
# for i in range(np.size(b, 0)):
#     for j in range(np.size(b, 1)):
#         if face_sample[i][j] != b[i][j]:
#             print('false')

# rootdir = 'Pictures/Photo'
# for llistdir in os.listdir(rootdir):
#     print(llistdir)

# for parent, dirnames, filenames in os.walk(rootdir):
#     # Case1: traversal the directories
#     for dirname in dirnames:
#         print("Parent folder:", parent)
#         print("Dirname:", dirname)
#     # Case2: traversal the files
#     for filename in filenames:
#         print("Parent folder:", parent)
#         print("Filename:", filename)

# recognizer = cv2.face.LBPHFaceRecognizer_create()
# face_cascade = cv2.CascadeClassifier('facebook/haarcascade_frontalface_default.xml')
# ids = []
# face_samples = []
# the_names = []
# for file in os.listdir('../txt_file'):
#     face_samples.append(np.loadtxt('facebook/txt_file/' + file))
#     the_names.append(file.split('_')[2])
# tree = ET.parse('../dictionary.xml')
# root = tree.getroot()
# for the_name in the_names:
#     for face in root:
#         if the_name == face.attrib['name']:
#             ids.append(int(face.attrib['label']))
# recognizer.train(face_samples, np.array(ids))
# recognizer.save('facebook/trainner.xml')