import datetime
import cv2
import os
import time
import numpy as np


#Global variables
MAX_CAM_RESOLUTION_WIDTH = 7680
MAX_CAM_RESOLUTION_HEIGHT = 4800
DEFAULT_CAM_RESOLUTION_WIDTH = 0
DEFAULT_CAM_RESOLUTION_HEIGHT = 0

timerStart = time.time()

frameWidth = 640
frameHeight = 480

camWidth = 640
camHeight = 480
frameArea = frameWidth * frameHeight

changeThres = 0.00
areaThresh = 0
zoom = 0

cX = 0
cY = 0
start_x = 0
start_y = 0
end_x = 0
end_y = 0

def trackbar_change(x):
    pass

def zoom_trackbar_change(x):
    pass

def changeCenterArea():
    global cX
    global cY
    global start_x
    global start_y
    global end_x
    global end_y
    cX = camWidth / 2 
    cY = camHeight / 2
    start_y = cY - (frameHeight / 2)
    end_y = cY + (frameHeight / 2)
    start_x = cX - (frameWidth / 2)
    end_x = cX + (frameWidth / 2)

 
def changedCamRatio(camera):
    global camWidth
    global camHeight
    global frameArea
    camWidth = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    camHeight = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
    

def main():
    counter = 0
    global MAX_CAM_RESOLUTION_WIDTH
    global MAX_CAM_RESOLUTION_HEIGHT
    global DEFAULT_CAM_RESOLUTION_WIDTH
    global DEFAULT_CAM_RESOLUTION_HEIGHT
    #capture object creation
    camera = cv2.VideoCapture(0)
    DEFAULT_CAM_RESOLUTION_WIDTH = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    DEFAULT_CAM_RESOLUTION_HEIGTH = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, MAX_CAM_RESOLUTION_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, MAX_CAM_RESOLUTION_HEIGHT)

    MAX_CAM_RESOLUTION_WIDTH = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    MAX_CAM_RESOLUTION_HEIGTH = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

    MAX_ZOOM = MAX_CAM_RESOLUTION_WIDTH / frameWidth

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)
    changedCamRatio(camera)
    
    newMotion = False

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    dateNow = datetime.datetime.now()
    year = str( getattr(dateNow, 'year') )
    month = str( getattr(dateNow, 'month') )
    day = str( getattr(dateNow, 'day') )

    #directory creation
    originFolder = os.getcwd()
    folderName = os.path.join(originFolder, year, month, day)
    if not os.path.isdir(folderName):
        os.makedirs(folderName)

    # Create a window
    cv2.namedWindow('Camera')

    # create trackbars for color change
    cv2.createTrackbar('Threshold','Camera',0,10,trackbar_change)
    cv2.createTrackbar('Zoom','Camera', 0, int(MAX_ZOOM), zoom_trackbar_change)
    track = 0
      
      
    changeCenterArea()
    first_img = camera.read()[1]
    first_img = first_img[start_y:end_y, start_x:end_x]
    initial_frame = cv2.cvtColor(first_img, cv2.COLOR_BGR2GRAY).astype('float')    
    
    while(1):
        ret, image = camera.read() 
        if not ret:
            break
        
        #finding the center and cropping       
        changeCenterArea()
        image = image[start_y:end_y, start_x:end_x]

        ##-------

        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(image_gray, (21, 21), 0)

        cv2.accumulateWeighted(blur, initial_frame, 0.5)
        frame_diff = cv2.absdiff(blur, cv2.convertScaleAbs(initial_frame))

        thresh = cv2.threshold(frame_diff, 10, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    
        changedArea = 0;
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            changedArea += w * h

        changeRatio = float(changedArea) / float(frameArea)
        print changeRatio
         
        if changeRatio >= changeThres:
            if counter is 0:
                newMotion = True
            
            if newMotion:
                dateNow = datetime.datetime.now()
                hour = str( getattr(dateNow, 'hour') )
                minute = str( getattr(dateNow, 'minute') )
                second = str( getattr(dateNow, 'second') )
                name = folderName +'/'+ hour +'-'+ minute +'-'+ second
                out = cv2.VideoWriter("%s.avi" %name,fourcc, 20.0, (640,480))
                newMotion = False
            print "Hareket kaydedildi!!" , counter
            out.write(image)
            counter += 1
            global timerStart
            timerStart = time.time()
        
        else:
            global timerEnd
            timerEnd = time.time()
            hours, rem = divmod(timerEnd - timerStart, 3600)
            minutes, seconds = divmod(rem, 60)
            print "Seconds = ",seconds
            if minutes == 1:
                print "Yeni Resme Gecildi"
                newMotion = True 
        
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
             

        cv2.imshow('Camera',image)
        cv2.imshow("Thresh", thresh)
        
        key = cv2.waitKey(1)
        if key & 0xFF is ord('q') or key & 0xFF is 27:
            break

        # get current positions of four trackbars
        global changeThres
        global areaThresh
        if cv2.getTrackbarPos('Threshold','Camera') != areaThresh :
	    areaThresh = cv2.getTrackbarPos('Threshold','Camera')
            changeThres = float(areaThresh) / 100.0
        global zoom
        if cv2.getTrackbarPos('Zoom','Camera') != track :
            track = cv2.getTrackbarPos('Zoom','Camera')
            zoom = track
            if zoom == 0:
	        zoom = 1
	    elif zoom == 1:
	        zoom = 1.5
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth * zoom)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight * zoom)
            #after changing the zoom we need to change the initial frame
            changedCamRatio(camera)
            changeCenterArea()
            first_img = camera.read()[1]
            first_img = first_img[start_y:end_y, start_x:end_x]
            initial_frame = cv2.cvtColor(first_img, cv2.COLOR_BGR2GRAY).astype('float')
        print zoom
        print changeThres


    camera.release()
    out.release()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    main()