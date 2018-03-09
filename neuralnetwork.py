# -*- coding: utf-8 -*-

"""
Based on the tflearn example located here:
https://github.com/tflearn/tflearn/blob/master/examples/images/convnet_cifar10.py
"""
from __future__ import division, print_function, absolute_import

from tflearn.data_utils import shuffle
import pickle
import settings
import reseau as re


def neuralNetwork():
    from tensorflow.python.framework import ops
    ops.reset_default_graph()

    # Load the data set
    with open("dataset.pkl", "rb") as f:
        u = pickle._Unpickler(f)
        u.encoding = 'latin1'
        X, Y, X_test, Y_test = u.load()
        X = X.astype('float32')
        X_test = X_test.astype('float32')

    # Shuffle the data
    X, Y = shuffle(X, Y)

    model = re.getReseau()

    # Train it! We'll do 100 training passes and monitor it as it goes.
    model.fit(X, Y, n_epoch=settings.nb_epoch, shuffle=True, validation_set=(X_test, Y_test),
              show_metric=True, batch_size=settings.batch_size,
              snapshot_epoch=True)
              #run_id='dataviz-classifier')
    # Save model when training is complete to a file
    model.save("dataviz-classifier.tfl")
    print(model.evaluate(X,Y))
    print("Network trained and saved as dataviz-classifier.tfl!")
