import loadData as ld
import sys
import shutil
import os

if os.path.isdir('data'):
    shutil.rmtree('data')

folderPath = sys.argv[1]

# Enter the local folder path of the dataset to convert it into jpeg with the desired height and width, the output will be in the data folder
ld.resize_dataset(folderPath, 32, 32)