  # -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import tflearn
from os.path import isfile, join
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
import settings
import os




def prediction():
    from tensorflow.python.framework import ops
    ops.reset_default_graph()
    size = settings.size
    #results = [f for f in os.listdir('data-classifier') if isfile(join('data-classifier', f))]
    count = 0
    '''for result in results:
        if len(result.split('-')) > 2 and result.split('-')[1]  == 'classifier.tfl.ckpt':
            if int(result.split('-')[2].split('.')[0]) > count:
                count = int(result.split('-')[2].split('.')[0])'''

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
    # model.load("./data-classifier/dataviz-classifier.tfl.ckpt-" + str(count))

    # Get a list of my testing images paths
    addrs = glob.glob("./test/*.jpg")
    labels = [0 if 'line' in addr else 1 if 'bar' in addr else 2 for addr in addrs]  # 0 = Line, 1 = Bar, 2=Scatter

    tp = 0
    label_predicted = []
    paths_images_wrong = []

    for index, addr in enumerate(addrs):
         # Scale it to 32x32
         #print(addr)
         img = cv2.imread(addr).astype(np.float32, casting='unsafe')
         # Predict
         prediction = model.predict([img])
         label_predicted.append(np.argmax(prediction[0]))
         # Check the result.
         is_line = np.argmax(prediction[0]) == 0
         is_bar = np.argmax(prediction[0]) == 1

         if is_line:
             print("That's a Line Chart")
         else:
             if is_bar:
                 print("That's a Bar Chart")
             else:
                 print("That's a Scatterplot Plot")

         if labels[index] == np.argmax(prediction[0]):
             # print("True positive")
             tp += 1
         else:
             paths_images_wrong.append(addrs[index])

    print(paths_images_wrong)


    size = max(labels + label_predicted)
    confusion = np.zeros((size+1,size+1))

    if len(labels) != len(label_predicted):
        print("Erreur de taille")
    else:
        for i in range(len(labels)):
            confusion[labels[i],label_predicted[i]] += 1

    print("The confusion matrix is : ")
    print(confusion)

