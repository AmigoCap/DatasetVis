  # -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import glob
import json
import os
import numpy as np
import cv2
import settings
import loadData as ld
import reseau as re
import datetime
import result as rs



def prediction():
    from tensorflow.python.framework import ops
    ops.reset_default_graph()

    model = re.getReseau()

    #Take the network previously trained
    model.load("dataviz-classifier.tfl")

    # Get a list of my testing images paths
    addrs = glob.glob("./test/*.jpg")
    # labels = give a number to each category in addrs (ex : line chart = 0 ; bar chart= 1, etc...)
    labels = [ld.getLabels().index(ld.getLabel(addr.replace('\\','/'))) for addr in addrs]


    tp = 0
    label_predicted = []
    paths_images_wrong = []

    #Initialisation of the results.json file
    json_result = rs.init_result()

    for index, addr in enumerate(addrs):
        # Scale it to 32x32
        #print(addr)
        img = cv2.imread(addr).astype(np.float32, casting='unsafe')
        # Predict with the trained model
        prediction = model.predict([img])


        #strictness : assigned to a category only if the prediction is 1.2 better than hazard
        if max(prediction[0]) < settings.strictness_class / len(prediction[0]):
            label_predicted.append(len(prediction[0]))
        #Attribute a class to the highest probability
        else:
            label_predicted.append(np.argmax(prediction[0]))

        prediction_array = []

        #Construction of the array of prediction
        for i, label in enumerate(ld.getLabels()):
            prediction_array.append({
                'label': label,
                'proba': prediction[0][i].item()
            })

        json_result['results'].append({
            'path': addr,
            'predictions': prediction_array
        })

        #Construction of the confusion matrix
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

    #Attribution to each class (uncategorized : if max(prediction)<strictness_class)
    if size == len(prediction[0]):
        print(ld.getLabels() + ['uncategorized'])
        json_result['confusion'] = confusion[:-1].tolist()
        print(confusion[:-1])
    else:
        print(ld.getLabels())
        json_result['confusion'] = confusion.tolist()
        print(confusion)



#Calculation of the recall & precision
    recall =[]
    recall_global=0
    for i in range(0,len(ld.getLabels())):
        recall_bis=0
        sum=0
        if size == len(prediction[0]):
            for j in range(0,ld.getLabelsNumber()+1):
                sum+=confusion[i][j]
                if sum==0:
                    recall_bis=0
                else:
                    recall_bis=(confusion[i][i]/sum)
        else :
            for j in range(0,ld.getLabelsNumber()):
                sum+=confusion[i][j]
                if sum==0:
                    recall_bis=0
                else:
                    recall_bis=(confusion[i][i]/sum)
        recall.append(recall_bis)
    recall_global=np.sum(recall)/len(ld.getLabels())
    print("recall : ")
    print(recall)
    print("Global recall : ")
    print(recall_global)

    precision =[]
    precision_global=0
    for i in range(0,len(ld.getLabels())):
        precis_bis=0
        sum=0
        for j in range(0,len(ld.getLabels())):
            sum+=confusion[j][i]
            if sum==0:
                precis_bis=0
            else:
                precis_bis=(confusion[i][i]/sum)
        precision.append(precis_bis)
    precision_global=np.sum(precision)/len(ld.getLabels())
    print("precision : ")
    print(precision)
    print("Global precision : ")
    print(precision_global)


#create the json result file
    with open('result_' + str(datetime.datetime.now()) + '.json', 'w') as outfile:
        json.dump(json_result, outfile)
