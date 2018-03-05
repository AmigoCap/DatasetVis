import loadData as ld
import shutil
import os


# Check if data folder exists inside local git and delete it to have a clean folder available
if os.path.isdir('data'):
    shutil.rmtree('data')

ld.resize_dataset()
