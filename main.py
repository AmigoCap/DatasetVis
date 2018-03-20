import loadData as ld
import shutil
import os
import build_dataset as bd
import neuralnetwork as nn
import prediction as pr
import settings as st
import time

# Check if data folder exists inside local git and delete it to have a clean folder available
if os.path.isdir('data'):
    shutil.rmtree('data')

# Initialization of output json
json_result = {
    'timestamp': time.time(),
    'settings': {
        'size': st.size,
        'offset_test': st.offset_test,
        'offset_train_val': st.offset_train_val,
        'nb_epoch': st.nb_epoch,
        'batch_size': st.batch_size,
        'learning_rate': st.learning_rate,
        'nb_filter': st.nb_filter,
        'filter_size': st.filter_size,
        'reseau': st.reseau
    },
    'results': [],
    'confusion': []
}

ld.resize_dataset()

bd.buildDataSet('data/*.jpg')

nn.neuralNetwork()

pr.prediction()
