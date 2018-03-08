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

path = sys.argv[1]

fileName = path.split('/')[len(path.split('/'))-1]

folderPath = path[:len(path)-len(fileName)-1]

size = settings.size

ld.resize_image(folderPath, fileName, size, size)

extension = fileName.split('.')[len(fileName.split('.'))-1]

img = cv2.imread('./data/'+fileName[:len(fileName)-len(extension)]+'jpg').astype(np.float32, casting='unsafe')

# Same network definition as before
img_prep = ImagePreprocessing()
img_prep.add_featurewise_zero_center()
img_prep.add_featurewise_stdnorm()
img_aug = ImageAugmentation()
img_aug.add_random_flip_leftright()
img_aug.add_random_rotation(max_angle=25.)
img_aug.add_random_blur(sigma_max=3.)

network = input_data(shape=[None, size, size, 3],
                     data_preprocessing=img_prep,
                     data_augmentation=img_aug)
network = conv_2d(network, size, 3, activation='relu')
network = max_pool_2d(network, 2)
network = conv_2d(network, size*4, 3, activation='relu')
network = conv_2d(network, size*4, 3, activation='relu')
network = max_pool_2d(network, 2)
network = fully_connected(network, size*16, activation='relu')
network = dropout(network, 0.5)
network = fully_connected(network, 3, activation='softmax')
network = regression(network, optimizer='adam',
                     loss='categorical_crossentropy',
                     learning_rate=settings.learning_rate)

model = tflearn.DNN(network, tensorboard_verbose=0) #checkpoint_path='dataviz-classifier.tfl.ckpt')
#print("'./data-classifier/dataviz-classifier.tfl.ckpt-" + str(count))
model.load("dataviz-classifier.tfl")

prediction = model.predict([img])

print(prediction)