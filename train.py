import json
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


def findEncoding(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img)[0]
    return encode


encodeList = []
for i in range(len(classNames)):
    try:
        encoded = findEncoding(images[i])
        encodeList.append(encoded)
    except:
        print(classNames[i])


file = np.array(encodeList)
np.savetxt('train.txt', file)
