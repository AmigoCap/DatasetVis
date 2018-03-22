import cv2
import numpy as np
import os
from os.path import isfile, join
import build_dataset as bd
import settings

globalLabels = []

def loadImage(filePath):
    image = cv2.imread(filePath)
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

def getLabels():
    return globalLabels

def getLabel(filePath):
    fileName = filePath.split('/')[len(filePath.split('/'))-1]
    label = ''
    for i in range(0, len(fileName.split('_')) - 1):
        label += fileName.split('_')[i] + '_'
    return label[:-1]

def getLabelsNumber():
    return len(getLabels())

def resize_image(folderPath, fileName, final_height, final_width):
    image = loadImage(folderPath + '/' + fileName)
    if getLabel(folderPath + '/' + fileName) not in globalLabels:
        globalLabels.append(getLabel(folderPath + '/' + fileName))

    height, width, channels = image.shape
    final_ratio = float(final_width) / final_height
    ratio = float(width / height)
    if ratio < final_ratio:
        wanted_width = round(final_ratio * height)
        border = int(wanted_width - width)
        blank_image = np.zeros((height, border, 3), np.uint8)
        blank_image[:, :] = (255, 255, 255)
        final = np.concatenate((image, blank_image), axis=1)
    elif ratio > final_ratio:
        wanted_height = round(width / final_ratio)
        border = int(wanted_height - height)
        blank_image = np.zeros((border, width, 3), np.uint8)
        blank_image[:, :] = (255, 255, 255)
        final = np.concatenate((image, blank_image), axis=0)
    else:
        final = image
    resized_image = cv2.resize(final, (final_width, final_height))
    # cv2.imshow('Resized Image', resized_image)
    # cv2.waitKey(0)

    if not os.path.isdir('data'):
        os.makedirs('data')
    return cv2.imwrite('data/' + fileName.split('.')[0] + '.jpg', resized_image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])


def resize_dataset():
    folderPath = settings.databasePath
    height = settings.size
    width = settings.size
    images = [f for f in os.listdir(folderPath) if isfile(join(folderPath, f))]
    print("########### Resizing all the dataset images to " + str(height) + " x " + str(
        height) + " in format .jpg #########")
    for i, image in enumerate(images):
        if image.split('.')[len(image.split('x'))] == 'png' or image.split('.')[len(image.split('x'))] == 'jpg' or \
                image.split('.')[len(image.split('x'))] == 'jpeg':
            if not resize_image(folderPath, image, height, width):
                print(image + ' no success on resize')
