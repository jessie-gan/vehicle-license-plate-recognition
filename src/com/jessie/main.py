#-*- coding: UTF-8 -*-

import cv2
import numpy as np
import Image
from sys import argv
import plateLocation as pL
import plateSegment as pS

if __name__ == '__main__':
    path = argv[1]
    imgPath = argv[2]
    print path,imgPath
    srcImg = cv2.imread(imgPath)
    #h,w = srcImg1.size
    #srcImg=srcImg1.resize((h*0.3,w*0.3),Image.ANTIALIAS)
    img = pL.preProcess(srcImg,path) 
    msg,value = pL.plateContour(srcImg,img,path)
    if msg==False: 
        print value
    else:
        plateRegion = value
        img = pL.CutPlate(plateRegion, srcImg,path)
        img = pS.tiltCorrect(img,path)
        img = pS.cutBorder(img,path)
        msg,value = pS.segment(img,path)
        if msg == False:
            print value
        