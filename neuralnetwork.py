# -*- coding: utf-8 -*-

"""
Based on the tflearn example located here:
https://github.com/tflearn/tflearn/blob/master/examples/images/convnet_cifar10.py
"""
from __future__ import division, print_function, absolute_import

# Import tflearn and some helpers
import shutil
import tflearn
from tflearn.data_utils import shuffle
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import pickle
import glob
import numpy as np
import argparse
import loadData
import cv2

import settings
import os
import prediction as pr


def neuralNetwork():
    from tensorflow.python.framework import ops
    ops.reset_default_graph()
    size = settings.size

    # Load the data set
    with open("dataset.pkl", "rb") as f:
        u = pickle._Unpickler(f)
        u.encoding = 'latin1'
        X, Y, X_test, Y_test = u.load()
        X = X.astype('float32')
        X_test = X_test.astype('float32')

    # Shuffle the data
    X, Y = shuffle(X, Y)

    # Make sure the data is normalized
    img_prep = ImagePreprocessing()
    img_prep.add_featurewise_zero_center()
    img_prep.add_featurewise_stdnorm()

    # Create extra synthetic training data by flipping, rotating and blurring the
    # images on our data set.
    img_aug = ImageAugmentation()
    img_aug.add_random_flip_leftright()
    img_aug.add_random_rotation(max_angle=25.)
    img_aug.add_random_blur(sigma_max=3.)

    # Define our network architecture:

    # Input is a 32x32 image with 3 color channels (red, green and blue)
    network = input_data(shape=[None, size, size, 3],
                         data_preprocessing=img_prep,
                         data_augmentation=img_aug)

    # Step 1: Convolution
    network = conv_2d(network, size, 3, activation='relu')

    # Step 2: Max pooling
    network = max_pool_2d(network, 2)

    # Step 3: Convolution again
    network = conv_2d(network, size*4, 3, activation='relu')

    # Step 4: Convolution yet again
    network = conv_2d(network, size*4, 3, activation='relu')

    # Step 5: Max pooling again
    network = max_pool_2d(network, 2)

    # Step 6: Fully-connected 512 node neural network
    network = fully_connected(network, size*16, activation='relu')

    # Step 7: Dropout - throw away some data randomly during training to prevent over-fitting
    network = dropout(network, 0.5)

    # Step 8: Fully-connected neural network with three outputs (0=isn't a bird, 1=is a bird) to make the final prediction
    network = fully_connected(network, 3, activation='softmax')

    # Tell tflearn how we want to train the network
    network = regression(network, optimizer='adam',
                         loss='categorical_crossentropy',
                         learning_rate=settings.learning_rate)

    '''if os.path.isdir('data-classifier'):
        shutil.rmtree('data-classifier')

    os.makedirs('data-classifier')'''

    # Wrap the network in a model object
    # model = tflearn.DNN(network, tensorboard_verbose=0, checkpoint_path='dataviz-classifier.tfl.ckpt')
    model = tflearn.DNN(network, tensorboard_verbose=0)#, checkpoint_path='data-classifier/dataviz-classifier.tfl.ckpt')

    # Train it! We'll do 100 training passes and monitor it as it goes.
    model.fit(X, Y, n_epoch=settings.nb_epoch, shuffle=True, validation_set=(X_test, Y_test),
              show_metric=True, batch_size=settings.batch_size,
              snapshot_epoch=True)
              #run_id='dataviz-classifier')
    # Save model when training is complete to a file
    model.save("dataviz-classifier.tfl")
    print(model.evaluate(X,Y))
    pr.prediction()
    print("Network trained and saved as dataviz-classifier.tfl!")

    '''
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

         ''''''if is_line:
             print("That's a Line Chart")
         else:
             if is_bar:
                 print("That's a Bar Chart")
             else:
                 print("That's a Scatterplot Plot")

         if labels[index] == np.argmax(prediction[0]):
            #print("True positive")
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
    print(confusion)'''
