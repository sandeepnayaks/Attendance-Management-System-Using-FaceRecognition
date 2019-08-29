import cv2
import numpy as np

face_casecade = cv2.CascadeClassifier('haarscasecade_frontalface_default.xml')
eye_casecade = cv2.CascadeClassifier('haarcascade_eye.xml')

cam_feed = cv2.VideoCapture(0)

while True:
    ret,frame = cam_feed.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    print(gray)
    faces = face_casecade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5)
    for x,y,w,h in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),4)
        roi_gray = gray[y:y+h,x:x+w]
        roi_color = frame[y:y+h,x:x+w]
        eyes = eye_casecade.detectMultiScale(roi_gray)
        for ex,ey,ew,eh in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    cv2.imshow('detect',frame)
    if cv2.waitKey(1) == 27:
        break

cam_feed.release()
cv2.destroyAllWindows()
