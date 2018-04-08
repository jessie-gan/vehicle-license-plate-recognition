#-*- coding: UTF-8 -*-

import cv2
import numpy as np
import Image
def tiltCorrect(img,path):
    plateImg = cv2.GaussianBlur(img,(3,3),0)  
    #cannyImg = cv2.Canny(plateImg, 50, 150)  
    result = plateImg.copy()  
    point = np.column_stack(np.where(result >0))
    angle = cv2.minAreaRect(point)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (rows,cols) = result.shape
    center = (rows // 2,cols //2)
    M = cv2.getRotationMatrix2D(center,angle,1)
    #rotatedImg = cv2.warpAffine(result,M,(cols,rows),
    #                         flags = cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
    rotatedImg = cv2.warpAffine(result,M,(cols,rows))
    path1 = path +'\\rotated1.jpg'
    cv2.imwrite(path1, rotatedImg) 
    #cv2.imshow('r1', rotatedImg)
    #cv2.waitKey(0) 
    rotatedImg = cv2.threshold(rotatedImg,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] 
    #cv2.imshow('r2', rotatedImg)
    #cv2.waitKey(0)
    path2 = path +'\\rotated2.jpg'
    cv2.imwrite(path2, rotatedImg)
    return rotatedImg
def cutBorder(img,path):
    x3 = cv2.Sobel(img,cv2.CV_16S,1,0);
    y3 = cv2.Sobel(img,cv2.CV_16S,0,1);
    imgSobelX3 = cv2.convertScaleAbs(x3);
    imgSobelY3 = cv2.convertScaleAbs(y3);
    imgSobel3 = cv2.addWeighted(imgSobelX3,0.5,imgSobelY3,0.5,0)
    #cv2.imshow('9', imgSobel3)
    #cv2.waitKey(0)
    h,w = imgSobel3.shape 
    print h,w
    allPixs = []
    sum = 0
    #统计每一行的白点数
    for n in range(h):     
        pixs = 0
        for m in range(w):
            pix = imgSobel3[n,m]
            if pix==255:
                pixs = pixs +1
        sum = sum + pixs        
        allPixs.append(pixs)
    avg = sum/(h)
    border = []
    #遍历寻找可能的边界区域
    for i in range(len(allPixs)):   
        rowPixs = allPixs[i]
        if rowPixs<avg and rowPixs !=0:
            border.append(i)
    y2 = border[len(border)-1]
    y1 = 0
    #确定边界截取的像素点坐标
    for i in range(len(border)):    
        if (border[i+1]-border[i]) > 5 and i > 5:
            y1 = border[i]
            break
        elif (border[i+1]-border[i]) == 2:
            y1 = border[i+1]
    
    for j in range(len(border)-1,1,-1):
        if (border[j]-border[j-1]) > 5:
            y2 = border[j-1]
            break
        elif border[j]-border[j-1]==2:
            y2 = border[j]
            break
    print y2,',',y1
    plateImg = img[y1:y2,0:w]
    path = path +'\plateImgNoBorder.jpg'
    cv2.imwrite(path, plateImg) 
    return plateImg
def segment(plateImg,path):
    h2,w2 = plateImg.shape
    print h2,w2
    allPixs2 = []
    sum = 0
    zero = 0
    for m in range(w2):
        pixs = 0
        for n in range(h2):
            pix = plateImg[n,m]
            if pix==255:
                pixs = pixs +1
        if pixs==0:
            zero = zero +1
        sum = sum + pixs        
        allPixs2.append(pixs)
    avg = sum/w2
    print avg
    flags = []
    i=0 
    for i,val in enumerate(allPixs2):
        print i,':',val,';',
    j = 10
    print ''
    while (j < len(allPixs2)):
        pixs = allPixs2[j]
        if pixs <= 5:
            times = 0
            flag = j+1
            while (pixs <= 5):
                times = times+1
                if j + times < len(allPixs2):
                    pixs = allPixs2[j+times]
                else:
                    break;
            j = j + times
            if times >= 3 and j > 15:
                if len(flags)!=0 and flag-flags[len(flags)-1] <=10:
                    flags[len(flags)-1] = (flag+flags[len(flags)-1])/2
                else:
                    flags.append(flag)
        j = j + 1
    print flags,',',len(flags)
    plateCopy = plateImg.copy()
    plates = []
    if len(flags)<7:
        return False,"fail to segment!flags less"
    plates.append(plateCopy[0:h2, 10:flags[0]])
    plates.append(plateCopy[0:h2, flags[0]:flags[1]])
    plates.append(plateCopy[0:h2, flags[1]:flags[2]])
    plates.append(plateCopy[0:h2, flags[2]:flags[3]])
    plates.append(plateCopy[0:h2, flags[3]:flags[4]])
    plates.append(plateCopy[0:h2, flags[4]:flags[5]])
    plates.append(plateCopy[0:h2, flags[5]:flags[6]])                                                                                                                        
    for i in range(7):
        name = str(i)
        #cv2.imshow(name,plates[i]) 
        #cv2.waitKey(0)
        path1 = path +'\\'+name+'.jpg'
        print path1
        cv2.imwrite(path1, plates[i]) 
    return True,"success"