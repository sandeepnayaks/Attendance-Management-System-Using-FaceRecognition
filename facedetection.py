import cv2 as imp
import numpy as np

def main():
    cam_feed = imp.VideoCapture(0)

    if cam_feed.isOpened():
        ret,image = cam_feed.read()
    else:
        ret = False

    while ret:
        ret,image = cam_feed.read()
        face_casecade = imp.CascadeClassifier("haarscasecade_frontalface_default.xml")
        gray_image = imp.cvtColor(image,imp.COLOR_BGR2GRAY)
        faces = face_casecade.detectMultiScale(gray_image,scaleFactor=1.05,minNeighbors=5)
        for a,b,c,d in faces:
            image = imp.rectangle(image,(a,b),((a+c),(a+d)),(0,255,0),3)
        imp.imshow('face',image)
        if imp.waitKey(1) == 27:
            break
    imp.destroyAllWindows()
    cam_feed.release()
        
    

#face_casecade = imp.CascadeClassifier("haarscasecade_frontalface_default.xml")

#image = imp.imread("f://Python1//imageProcessing//opencv//ashvintut//standard_test_images//standard_test_images//lena_color_256.tif")

#gray_image = imp.cvtColor(image,imp.COLOR_BGR2GRAY)

#faces = face_casecade.detectMultiScale(gray_image,scaleFactor=1.05,minNeighbors=5)

#for a,b,c,d in faces:
#    image = imp.rectangle(image,(a,b),((a+c),(a+d)),(0,255,0),3)

#imp.imshow('face',image)
#imp.waitKey(0)
#imp.destoryAllWindows()
if __name__ == '__main__':
    main()
