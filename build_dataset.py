import numpy as np
import glob
from random import shuffle
import loadData
import pickle
import cv2
import shutil
import os
import neuralnetwork as nn

def buildDataSet(path, size):
    #Building an images dataset with 3 classes : Line chart Bar chart, Scatter plot
    shuffle_data = True

    #Contains images of 3 classes : Line Chart, Bar Chart, Scatter Chart
    #train_path = "./dataset/train-validation/*.jpg"
    offset_test = 0.1
    offset_train_val = 0.7
    X = []
    X_val = []
    Y = []
    Y_val = []

    #Get a list of my images paths
    addrs = glob.glob(path)

    #Get a list of my training images labels
    labels = [0 if 'line' in addr else 1 if 'bar' in addr else 2 for addr in addrs]  # 0 = Line, 1 = Bar, 2=Scatter

    #To shuffle data
    if shuffle_data:
        c = list(zip(addrs, labels))
        shuffle(c)
        addrs, labels = zip(*c)

    test_addrs = addrs[0:int(offset_test*len(addrs))]

    dst_dir = "./test"
    for jpgfile in test_addrs:
        shutil.copy(jpgfile, dst_dir)

    train_val_addrs = addrs[int(offset_test*len(addrs)):]
    train_val_labels = labels[int(offset_test*len(addrs)):]


    #Divide the data into offset% train, offset% validation
    train_addrs = train_val_addrs[0:int(offset_train_val*len(addrs))]
    train_labels = train_val_labels[0:int(offset_train_val*len(labels))]
    validation_addrs = train_val_addrs[int(offset_train_val*len(addrs)):]
    validation_labels = train_val_labels[int(offset_train_val*len(labels)):]

    #Create a list of image array for the training dataset
    for addr in train_addrs:
        img = cv2.imread(addr)
        X.append(img)

    #Create a list of image labels for the training dataset: [1,0,0] : Line, [0,1,0] : Bar,[0,0,1] : Scatter
    Y = train_labels
    Y_train =[]
    for a in Y :
        if a==0:
            Y_train.append([1,0,0])
        else:
            if a==1:
                Y_train.append([0,1,0])
            else:
                Y_train.append([0,0,1])

    Y_train = np.asarray(Y_train,dtype='float32')

    #Create a list of resized image array for the validation dataset
    for addr in validation_addrs :
        img = cv2.imread(addr)
        X_val.append(img)

    #Create a list of image labels for the validation dataset: [1,0,0] : Line, [0,1,0] : Bar,[0,0,1] : Scatter
    Y_val = validation_labels
    Y_val_resized =[]
    for a in Y_val :
        if a==0:
            Y_val_resized.append([1,0,0])
        else:
            if a==1:
                Y_val_resized.append([0,1,0])
            else:
                Y_val_resized.append([0,0,1])

    Y_val_resized = np.asarray(Y_val_resized,dtype='float32')

    X_train = np.asarray(X,dtype='float32')
    X_val_resized = np.asarray(X_val,dtype='float32')

    print(X_train)
    print(Y_train)
    print(X_val_resized)
    print(Y_val_resized)

    print(X_train.shape)
    print(Y_train.shape)
    print(X_val_resized.shape)
    print(Y_val_resized.shape)


    with open('dataset.pkl', 'wb') as f:
        #train_set, valid_set, test_set = pickle.load(f)
        pickle.dump((X_train,Y_train,X_val_resized,Y_val_resized),f)

    nn.neuralNetwork(size)

    '''with open("dataset.pkl", "rb") as f:
        a,b,c,d = pickle.load(f)'''
