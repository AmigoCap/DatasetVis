import numpy as np
import glob
from random import shuffle
import loadData
import pickle
import cv2
import shutil
import os
import settings
import loadData as ld

def getUniformDatas(addrs):
    offset_test = settings.offset_test
    test_addrs =[]
    train_val_addrs=[]
    nbLabels = ld.getLabelsNumber()
    Labels = ld.getLabels()

    separated_Classes = [[] for _ in range(nbLabels)]

    for addr in addrs:
        for i in range(nbLabels):
            if Labels[i] in addr :
                separated_Classes[i].append(addr)

    for i in range(nbLabels):
        test_addrs.append(separated_Classes[i][0:int(offset_test * len(separated_Classes[i]))])
        train_val_addrs.append(separated_Classes[i][int(offset_test * len(separated_Classes[i])):])

    test_addrs = [item for sublist in test_addrs for item in sublist]
    train_val_addrs = [item for sublist in train_val_addrs for item in sublist]

    return test_addrs, train_val_addrs


def buildDataSet(path):
    # Building an images dataset with 3 classes : Line chart Bar chart, Scatter plot
    shuffle_data = True

    # Contains images of 3 classes : Line Chart, Bar Chart, Scatter Chart
    # train_path = "./dataset/train-validation/*.jpg"
    offset_test = settings.offset_test
    offset_train_val = settings.offset_train_val

    print("######## Dividing our resized dataset in two parts #######")
    print("Test : " + str(offset_test * 100) + " %")
    print("Train-validation : " + str((1 - offset_test) * 100) + " %")
    print("######## Dividing train-validation dataset in two parts #######")
    print("Train : " + str((offset_train_val) * 100) + " %")
    print("Validation : " + str(int((1 - offset_train_val) * 100)) + " %")

    X = []
    X_val = []
    Y = []
    Y_val = []

    # Get a list of my images paths
    addrs = glob.glob(path)
    test_addrs, train_val_addrs = getUniformDatas(addrs)

    # Get a list of my training images labels
    # labels = [0 if 'line' in addr else 1 if 'bar' in addr else 2 for addr in addrs]  # 0 = Line, 1 = Bar, 2=Scatter
    train_val_labels = [ld.getLabels().index(ld.getLabel(addr)) for addr in train_val_addrs]

    # To shuffle data
    if shuffle_data:
        c = list(zip(train_val_addrs, train_val_labels))
        shuffle(c)
        train_val_addrs, train_val_labels = zip(*c)

    if os.path.isdir('./test'):
        shutil.rmtree('./test')
    os.makedirs('./test')

    dst_dir = "./test"
    for jpgfile in test_addrs:
        shutil.copy(jpgfile, dst_dir)

    # Divide the data into offset% train, offset% validation
    train_addrs = train_val_addrs[0:int(offset_train_val * len(train_val_addrs))]
    train_labels = train_val_labels[0:int(offset_train_val * len(train_val_labels))]
    validation_addrs = train_val_addrs[int(offset_train_val * len(train_val_addrs)):]
    validation_labels = train_val_labels[int(offset_train_val * len(train_val_labels)):]

    # Create a list of image array for the training dataset
    for addr in train_addrs:
        img = cv2.imread(addr)
        X.append(img)

    # Create a list of image labels for the training dataset: [1,0,0] : Line, [0,1,0] : Bar,[0,0,1] : Scatter
    Y = train_labels
    Y_train = []
    nbLabels = ld.getLabelsNumber()
    for i in Y:
        a = [0] * nbLabels
        a[i] = 1
        Y_train.append(a)

    Y_train = np.asarray(Y_train, dtype='float32')

    # Create a list of resized image array for the validation dataset
    for addr in validation_addrs:
        img = cv2.imread(addr)
        X_val.append(img)

    # Create a list of image labels for the validation dataset: [1,0,0] : Line, [0,1,0] : Bar,[0,0,1] : Scatter
    Y_val = validation_labels
    Y_val_resized = []
    for i in Y_val:
        a = [0] * nbLabels
        a[i] = 1
        Y_val_resized.append(a)

    Y_val_resized = np.asarray(Y_val_resized, dtype='float32')

    X_train = np.asarray(X, dtype='float32')
    X_val_resized = np.asarray(X_val, dtype='float32')

    print("######## Pickling Arrays objects for training and testing our CNN model ######")
    print(X_train.shape)
    print(Y_train.shape)
    print(X_val_resized.shape)
    print(Y_val_resized.shape)

    with open('dataset.pkl', 'wb') as f:
        # train_set, valid_set, test_set = pickle.load(f)
        pickle.dump((X_train, Y_train, X_val_resized, Y_val_resized), f)
