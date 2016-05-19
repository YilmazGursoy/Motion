import datetime
import os
import cv2
import time
import numpy as np

global timerStart
timerStart = time.time()


def main():
    counter = 0
    camera = cv2.VideoCapture(0)
    camera.set(3, 640)
    camera.set(4, 480)
    
    newMotion = False

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    dateNow = datetime.datetime.now()
    year = str( getattr(dateNow, 'year') )
    month = str( getattr(dateNow, 'month') )
    day = str( getattr(dateNow, 'day') )
    
    originFolder = os.getcwd()
    folderName = os.path.join(originFolder, year, month, day)
    if not os.path.isdir(folderName):
        os.makedirs(folderName)
        
    initial_frame = cv2.cvtColor(camera.read()[1], cv2.COLOR_BGR2GRAY).astype('float')
    value = 0
    while True:
        ret, image = camera.read()

        if not ret:
            break

        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(image_gray, (21, 21), 0)

        cv2.accumulateWeighted(blur, initial_frame, 0.5)
        frame_diff = cv2.absdiff(blur, cv2.convertScaleAbs(initial_frame))

        thresh = cv2.threshold(frame_diff, 10, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        if cnts:
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

        cv2.imshow("Webcam", image)
        cv2.imshow("Thresh", thresh)

        if cv2.waitKey(1) & 0xFF is ord('q') or cv2.waitKey(1) & 0xFF is 27:
            break
    # Release everything if job is finished
    camera.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()