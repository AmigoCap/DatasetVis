import loadData as ld
import shutil
import os
import build_dataset as bd
import neuralnetwork as nn
import prediction as pr

# Check if data folder exists inside local git and delete it to have a clean folder available
if os.path.isdir('data'):
    shutil.rmtree('data')

ld.resize_dataset()

bd.buildDataSet('data/*.jpg')

nn.neuralNetwork()

pr.prediction()
