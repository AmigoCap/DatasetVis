  # -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import glob
import numpy as np
import cv2
import settings
import loadData as ld
import reseau as re




def prediction():
    from tensorflow.python.framework import ops
    ops.reset_default_graph()

    model = re.getReseau()

    #print("'./data-classifier/dataviz-classifier.tfl.ckpt-" + str(count))
    model.load("dataviz-classifier.tfl")
    # model.load("./data-classifier/dataviz-classifier.tfl.ckpt-" + str(count))

    # Get a list of my testing images paths
    addrs = glob.glob("./test/*.jpg")
    # labels = [0 if 'line' in addr else 1 if 'bar' in addr else 2 for addr in addrs]  # 0 = Line, 1 = Bar, 2=Scatter
    labels = [ld.getLabels().index(ld.getLabel(addr.replace('\\','/'))) for addr in addrs]

    tp = 0
    label_predicted = []
    paths_images_wrong = []

    for index, addr in enumerate(addrs):
         # Scale it to 32x32
         #print(addr)
         img = cv2.imread(addr).astype(np.float32, casting='unsafe')
         # Predict
         prediction = model.predict([img])
         if max(prediction[0]) < 1.2/len(prediction[0]):
            label_predicted.append(len(prediction[0]))
         else:
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
    if size == len(prediction[0]):
        print(ld.getLabels() + ['uncategorized'])
        print(confusion[:-1])
    else:
        print(ld.getLabels())
        print(confusion)

    recall =[]
    for i in range(0,len(ld.getLabels())):
        recall_bis=0
        sum=0
        for j in range(0,len(ld.getLabels())):
            sum+=confusion[j][i]
            if sum==0:
                recall_bis=0
            else:
                recall_bis=(confusion[i][i]/sum)
        recall.append(recall_bis)
    print("recall : ")
    print(recall)

    prediction =[]
    for i in range(0,len(ld.getLabels())):
        predict_bis=0
        sum=0
        for j in range(0,len(ld.getLabels())):
            sum+=confusion[i][j]
            if sum==0:
                predict_bis=0
            else:
                predict_bis=(confusion[i][i]/sum)
        prediction.append(predict_bis)
    print("prediction : ")
    print(prediction)
