import loadData as ld
import sys
import shutil
import os

# Check if data folder exists inside local git and delete it to have a clean folder available
if os.path.isdir('data'):
    shutil.rmtree('data')

# Retrieve dataset folder path
folderPath = sys.argv[1]

# Resize all the dataset and copy it inside the data folder
ld.resize_dataset(folderPath, 32, 32)