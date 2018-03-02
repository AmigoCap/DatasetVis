import loadData as ld
import sys
import shutil
import os
import build_dataset as bd


# Check if data folder exists inside local git and delete it to have a clean folder available
if os.path.isdir('data'):
    shutil.rmtree('data')

ld.resize_dataset()


# Retrieve dataset folder path
# folderPath = sys.argv[1]

# Retrieve size
# size = int(sys.argv[2])
