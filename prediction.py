  # -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import glob
import numpy as np
import argparse
import loadData
import pickle
import cv2
from random import shuffle


'''parser = argparse.ArgumentParser(description='Decide if an image is a picture of a bird')
parser.add_argument('image', type=str, help='The image image file to check')
args = parser.parse_args()'''


# Same network definition as before
img_prep = ImagePreprocessing()
img_prep.add_featurewise_zero_center()
img_prep.add_featurewise_stdnorm()
img_aug = ImageAugmentation()
img_aug.add_random_flip_leftright()
img_aug.add_random_rotation(max_angle=25.)
img_aug.add_random_blur(sigma_max=3.)

network = input_data(shape=[None, 32, 32, 3],
                     data_preprocessing=img_prep,
                     data_augmentation=img_aug)
network = conv_2d(network, 32, 3, activation='relu')
network = max_pool_2d(network, 2)
network = conv_2d(network, 128, 3, activation='relu')
network = conv_2d(network, 128, 3, activation='relu')
network = max_pool_2d(network, 2)
network = fully_connected(network, 512, activation='relu')
network = dropout(network, 0.5)
network = fully_connected(network, 3, activation='softmax')
network = regression(network, optimizer='adam',
                     loss='categorical_crossentropy',
                     learning_rate=0.001)

model = tflearn.DNN(network, tensorboard_verbose=0, checkpoint_path='dataviz-classifier.tfl.ckpt')
model.load("./dataviz-classifier.tfl.ckpt-8160")
shuffle_data = True

#Load the training dataset
with open("dataset.pkl", "rb") as f:
    a,b,c,d, = pickle.load(f)

#Get a list of my testing images paths
addrs = glob.glob("./test/*.jpg")
labels = [[1,0,0] if 'line' in addr else [0,1,0] if 'bar' in addr else [0,0,1] for addr in addrs]  # 0 = Line, 1 = Bar, 2=Scatter
tp=0
print(labels)
for index,addr in enumerate(addrs):
# Scale it to 32x32
    print(addr)
    print(labels[index])
    img = cv2.imread(addr).astype(np.float32, casting='unsafe')
# Predict
    prediction = model.predict([img])
    print(prediction[0])
# Check the result.
    is_line = np.argmax(prediction[0]) == 0
    is_bar = np.argmax(prediction[0]) == 1

    if np.argmax(labels[index]) == np.argmax(prediction[0]):
        print("True positive")
        tp +=1

    if is_line:
        print("That's a Line Chart")
    else:
        if is_bar:
            print("That's a Bar Chart")
        else :
            print("That's a Scatterplot Plot")


print(tp)
print(len(addrs))
#odel.evaluate(e,f,batch_size=1)