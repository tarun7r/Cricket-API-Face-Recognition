import array
import os

import cv2
import face_recognition
import numpy as np

path = 'image'
images = []
classNames = []
myList = os.listdir(path)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])


encodeList = np.loadtxt('train.txt')


imgtest = face_recognition.load_image_file('jasprit_test.jpg')
mgtest = cv2.cvtColor(imgtest, cv2.COLOR_BGR2RGB)
encodetest = face_recognition.face_encodings(imgtest)[0]

matches = face_recognition.compare_faces(encodeList, encodetest)
faceDis = face_recognition.face_distance(encodeList, encodetest)


matchIndex = np.argmin(faceDis)

if matches[matchIndex]:
    name = classNames[matchIndex+1].upper()
    print(name, faceDis[matchIndex])
