import numpy as np
import glob
from PIL import Image
import cv2
from resizeimage import resizeimage
from random import shuffle
import loadData

shuffle_data = True
pie_bar_train_path = "./train/*.jpg"

X = []
X_test = []
Y = []
Y_test = []

addrs = glob.glob(pie_bar_train_path)
labels = [0 if 'pie' in addr else 1 for addr in addrs]  # 0 = Pie, 1 = Bar

# to shuffle data
if shuffle_data:
    c = list(zip(addrs, labels))
    shuffle(c)
    addrs, labels = zip(*c)


# Divide the data into 70% train, 30% test
train_addrs = addrs[0:int(0.7*len(addrs))]
train_labels = labels[0:int(0.7*len(labels))]
test_addrs = addrs[int(0.7*len(addrs)):]
test_labels = labels[int(0.7*len(labels)):]

for addr in train_addrs :
    print(addr)
    img = loadData.resize_image(addr,32,32)
    X.append(img)


Y = np.asarray(train_labels)
Y_resize =[]
for a in Y :
    if a==1:
        Y_resize.append([1,0])
    else:
        Y_resize.append([0,1])

print(Y_resize)

for addr in test_addrs :
    img = loadData.resize_image(addr,32,32)
    X_test.append(img)


Y_test = np.asarray(test_labels)
Y_test_resize =[]
for a in Y_test :
    if a==1:
        Y_test_resize.append([1,0])
    else:
        Y_test_resize.append([0,1])

print(Y_test_resize)

X_arr = np.asarray(X)
X_test_arr = np.asarray(X_test)



import pickle

with open('dataset.pkl', 'wb') as f:
    #train_set, valid_set, test_set = pickle.load(f)
    pickle.dump((X_arr,Y_resize,X_test_arr,Y_test_resize),f)

with open("dataset.pkl", "rb") as f:
    a,b,c,d = pickle.load(f)

