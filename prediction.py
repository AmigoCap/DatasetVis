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
    labels = [ld.getLabels().index(ld.getLabel(addr)) for addr in addrs]

    tp = 0
    label_predicted = []
    paths_images_wrong = []

    json_result = settings.json_result

    for index, addr in enumerate(addrs):
        # Scale it to 32x32
        #print(addr)
        img = cv2.imread(addr).astype(np.float32, casting='unsafe')
        # Predict
        prediction = model.predict([img])

        prediction_array = []

        for i, label in enumerate(ld.getLabels()):
            prediction_array.append({
                'label': label,
                'proba': prediction[0][i].item()
            })

        json_result['results'].append({
            'path': addr,
            'predictions': prediction_array
        })

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

    # json_result['confusion'] = confusion.tolist()

    # json_str = json.dumps(json_result)

    print("The confusion matrix is : ")
    print(ld.getLabels())
    print(confusion)

    with open('result.json', 'w') as outfile:
        json.dump(json_result, outfile)

    # try:
    #     os.stat("result.txt")
    #     with open('result.txt', 'w') as outfile:
    #         json.dump(json_result, outfile)
    # except:
    #     with open('result.txt', 'w') as outfile:
    #         json.dump(json_result, outfile)
