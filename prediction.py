  # -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import tflearn
from os.path import isfile, join
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d, avg_pool_2d
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
import loadData as ld
import os




def prediction():
    from tensorflow.python.framework import ops
    ops.reset_default_graph()
    size = settings.size
    nb_filter = settings.nb_filter
    filter_size = settings.filter_size


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

    reseau = settings.reseau
    if reseau == 1:
        # Step 1: Convolution
        network = conv_2d(network, nb_filter, filter_size, activation='relu')

        # Step 2: Max pooling
        network = max_pool_2d(network, 2)

        # Step 3: Convolution again
        network = conv_2d(network, nb_filter*4, filter_size, activation='relu')

        # Step 4: Convolution yet again
        network = conv_2d(network, nb_filter*4, filter_size, activation='relu')

        # Step 5: Max pooling again
        network = max_pool_2d(network, 2)

        # Step 6: Fully-connected 512 node neural network
        network = fully_connected(network, nb_filter*16, activation='relu')

        # Step 7: Dropout - throw away some data randomly during training to prevent over-fitting
        network = dropout(network, 0.5)
        # Step 8: Fully-connected neural network with three outputs (0=isn't a bird, 1=is a bird) to make the final prediction


    elif reseau == 2:
        network = conv_2d(network, 32, 3, activation='relu')
        network = conv_2d(network, 32, 3, activation='relu')
        network = max_pool_2d(network, 2)
        network = conv_2d(network, 32, 3, activation='relu')
        network = conv_2d(network, 32, 3, activation='relu')
        network = max_pool_2d(network, 2)
        network = fully_connected(network, 512, activation='relu')
        network = fully_connected(network, 512, activation='relu')

    elif reseau == 3:
        network = conv_2d(network, 32, 3, activation='relu')
        network = avg_pool_2d(network, 2)
        network = conv_2d(network, 32, 3, activation='relu')
        network = avg_pool_2d(network, 2)
        network = conv_2d(network, 32, 3, activation='relu')
        network = avg_pool_2d(network, 2)
        network = fully_connected(network, 512, activation='relu')
        network = fully_connected(network, 512, activation='relu')
        network = dropout(network, 0.5)

    elif reseau == 4:
        network = conv_2d(network, 32, 3, activation='relu')
        network = conv_2d(network, 32, 3, activation='relu')
        network = conv_2d(network, 32, 5, padding = 'valid', activation='relu')
        network = conv_2d(network, 32, 3, activation='relu')
        network = conv_2d(network, 32, 3, activation='relu')
        network = conv_2d(network, 32, 5, padding='valid', activation='relu')
        network = fully_connected(network, 512, activation='relu')
        network = dropout(network, 0.5)

    elif reseau == 5:
        network = conv_2d(network, 64, 3, activation='relu')
        network = conv_2d(network, 64, 3, activation='relu')
        network = avg_pool_2d(network, 2)
        network = conv_2d(network, 32, 3, activation='relu')
        network = conv_2d(network, 32, 3, activation='relu')
        network = max_pool_2d(network, 2)
        network = fully_connected(network, 512, activation='relu')
        network = fully_connected(network, 512, activation='relu')

    network = fully_connected(network, ld.getLabelsNumber(), activation='softmax')

    network = regression(network, optimizer='adam',
                         loss='categorical_crossentropy',
                         learning_rate=settings.learning_rate)

    model = tflearn.DNN(network, tensorboard_verbose=0) #checkpoint_path='dataviz-classifier.tfl.ckpt')
    #print("'./data-classifier/dataviz-classifier.tfl.ckpt-" + str(count))
    model.load("dataviz-classifier.tfl")
    # model.load("./data-classifier/dataviz-classifier.tfl.ckpt-" + str(count))

    # Get a list of my testing images paths
    addrs = glob.glob("./test/*.jpg")
    # labels = [0 if 'line' in addr else 1 if 'bar' in addr else 2 for addr in addrs]  # 0 = Line, 1 = Bar, 2=Scatter
    labels = [ld.getLabels().index(ld.getLabel(addr)) for addr in addrs]

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
         # # Check the result.
         # is_line = np.argmax(prediction[0]) == 0
         # is_bar = np.argmax(prediction[0]) == 1

         if labels[index] == np.argmax(prediction[0]):
             # print("True positive")
             tp += 1
         else:
             paths_images_wrong.append(addrs[index])
    print('###### Ensemble des images mal classées :')
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
