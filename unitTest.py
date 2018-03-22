import cv2
import sys
import tflearn
import settings
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import numpy as np
import loadData as ld
import reseau as re

path = sys.argv[1]

fileName = path.split('/')[len(path.split('/'))-1]

folderPath = path[:len(path)-len(fileName)-1]

size = settings.size

ld.resize_image(folderPath, fileName, size, size)

extension = fileName.split('.')[len(fileName.split('.'))-1]

img = cv2.imread('./data/'+fileName[:len(fileName)-len(extension)]+'jpg').astype(np.float32, casting='unsafe')

model = re.getReseau()

model.load("dataviz-classifier.tfl")

prediction = model.predict([img])

print(prediction)