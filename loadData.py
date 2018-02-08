import cv2
import math

def loadImage(filePath):
    image = cv2.imread(filePath)
    copyImg = image.copy()
    gray_image = cv2.fastNlMeansDenoising(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))

    # ret, thresh = cv2.threshold(gray_image, 200, 200, 200)
    # ret, thresh = cv2.adaptiveThreshold(gray_image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    thresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 10)

    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    x = 0
    y = 0

    for point in contours[0]:
        x += point[0][0]
        y += point[0][1]

    x = x / len(contours[0])
    y = y / len(contours[0])

    center = [x,y]
    total = 0

    contours.remove(contours[0])
    print(contours)

    for contour in contours:
        x = 0
        y = 0

        for point in contour:
            x += point[0][0]
            y += point[0][1]

        x = x / len(contour)
        y = y / len(contour)

        dist = math.sqrt(math.pow(x - center[0], 2) + math.pow(y - center[1], 2))
        total += dist

    print(total/len(contours))




    cv2.drawContours(copyImg, contours, -1, (0, 255, 0), 3)
    # cv2.imshow('Test', thresh)
    # cv2.imshow('Test 2', copyImg)
    # cv2.imshow('Draw contours', gray_image)
    cv2.waitKey(0)

# def getData(filePath):
#     image = cv2.imread(filePath)
