import cv2
import numpy as np
from os import listdir
from os.path import isfile, join


def loadImage(filePath):
    image = cv2.imread(filePath)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def resize_image(folderPath, fileName, final_height, final_width):
    image = loadImage(folderPath + '/' + fileName)
    height, width, channels = image.shape
    final_ratio = float(final_width) / final_height
    ratio = float(width / height)
    if ratio < final_ratio:
        wanted_width = round(final_ratio*height)
        border = int(wanted_width - width)
        blank_image = np.zeros((height, border, 3), np.uint8)
        blank_image[:,:] = (255, 255, 255)
        final = np.concatenate((image, blank_image), axis=1)
    elif ratio > final_ratio:
        wanted_height = round(width/final_ratio)
        border = int(wanted_height - height)
        blank_image = np.zeros((border, width, 3), np.uint8)
        blank_image[:, :] = (255, 255, 255)
        final = np.concatenate((image, blank_image), axis=0)
    else:
        final = image
    resized_image = cv2.resize(final, (final_width, final_height))
    # cv2.imshow('Resized Image', resized_image)
    # cv2.waitKey(0)

    return cv2.imwrite('data/' + fileName, resized_image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])


def resize_dataset(folderPath, height, width):
    images = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]
    for image in images:
        if not resize_image(folderPath, image, height, width):
            print(image + ' no success on resize')