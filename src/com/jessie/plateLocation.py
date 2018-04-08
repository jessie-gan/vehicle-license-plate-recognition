#-*-coding:UTF-8 -*-

import cv2
import numpy as np
import os
def preProcess(srcImg,path):
    img = cv2.cvtColor(srcImg,cv2.COLOR_BGR2GRAY)
    
    x = cv2.Sobel(img,cv2.CV_16S,1,0)
    imgSobel = cv2.convertScaleAbs(x)
    path1 = path +'\sobel1.jpg'
    cv2.imwrite(path1, imgSobel) 
    kernel = np.ones((10,10),np.uint8)
    imgDilation = cv2.dilate(imgSobel,kernel,iterations = 1)
    path2 = path +'\dilation1.jpg'
    cv2.imwrite(path2, imgDilation) 
    imgErosion = cv2.erode(imgDilation,kernel,iterations = 1)
    path3 = path +'\erosion1.jpg'
    cv2.imwrite(path3, imgErosion) 
    x2 = cv2.Sobel(imgDilation,cv2.CV_16S,1,0);
    y2 = cv2.Sobel(imgDilation,cv2.CV_16S,0,1);
    imgSobelX = cv2.convertScaleAbs(x2);
    imgSobelY = cv2.convertScaleAbs(y2);
    imgSobel2 = cv2.addWeighted(imgSobelX,0.5,imgSobelY,0.5,0)
    path4 = path +'\sobel2.jpg'
    cv2.imwrite(path4, imgSobel2) 
    kernel2 = np.ones((2,2),np.uint8)
    imgDilation2 = cv2.dilate(imgSobel2,kernel2,iterations = 1)
    path6 = path +'\dilation2.jpg'
    cv2.imwrite(path6, imgDilation2) 
    imgErosion2 = cv2.erode(imgDilation2,kernel2,iterations = 1)
    path5 = path +'\erosion2.jpg'
    cv2.imwrite(path5, imgErosion2) 
    return imgDilation2;
def plateContour(srcImg,img,path):
    imgCopy = srcImg.copy()
    ret,thresh = cv2.threshold(img,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgCopy, contours, -1, (0,255,0), 1)
    path1 = path +'\contour1.jpg'
    cv2.imwrite(path1, imgCopy) 
    #--------****寻找可能的车牌轮廓****----------------#
    rightRegion = []
    rectHeight = 0
    rectWeight = 0
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if area<2000:
            continue
        rect = cv2.minAreaRect(cnt)
        box = cv2.cv.BoxPoints(rect)
        box = np.int0(box)
        #cv2.drawContours(image, [box], 0, (0,0,255), 1)
        #对角线
        rectHeight = abs(box[0][1] - box[2][1])
        rectWeight = abs(box[0][0] - box[2][0])
        
        ratio =float(rectWeight) / float(rectHeight)
        if (ratio > 3.9 or ratio < 2.1):
            continue
        print box
        print box[0][1],box[2][1],box[0][0],box[2][0]
        rightRegion.append(box)
    cv2.drawContours(imgCopy, rightRegion, -1, (0,0,255), 1)
    path2 = path +'\contour2.jpg'
    cv2.imwrite(path2, imgCopy) 
    #cv2.imshow("9",imgCopy)
    #cv2.waitKey(0)
    if len(rightRegion)==0:
        return False,"no plate"
    plateRegion = []
    plateRegion.append(rightRegion[0])
    if len(rightRegion)>1:
        minArea = cv2.contourArea(rightRegion[0])
        print minArea
        for j in range(1,len(rightRegion)):
            if cv2.contourArea(rightRegion[j]) < minArea:
                minArea = cv2.contourArea(rightRegion[j])
                plateRegion[0] = rightRegion[j]
    cv2.drawContours(imgCopy, plateRegion, 0, (255,0,0), 1)
    if len(plateRegion)==0:
        return False,"no suitable plate！"
    return True,plateRegion
def CutPlate(plateRegion,srcImg,path):
    cv2.imshow('2', srcImg)
    cv2.waitKey(0) 
    img = cv2.cvtColor(srcImg,cv2.COLOR_BGR2GRAY)
    box = plateRegion[0]
    #截取车牌
    ys = [box[0, 1], box[1, 1], box[2, 1], box[3, 1]]
    xs = [box[0, 0], box[1, 0], box[2, 0], box[3, 0]]
    ys_sorted_index = np.argsort(ys)
    xs_sorted_index = np.argsort(xs)

    x1 = box[xs_sorted_index[0], 0]
    x2 = box[xs_sorted_index[3], 0]

    y1 = box[ys_sorted_index[0], 1]
    y2 = box[ys_sorted_index[3], 1]

    imgCopy = img.copy()
    plateImg = imgCopy[y1:y2, x1:x2]
    #cv2.imshow('1', plateImg)
    #cv2.waitKey(0)
    path = path +'\plate1_beforR.jpg'
    cv2.imwrite(path, plateImg) 
    return plateImg
    
