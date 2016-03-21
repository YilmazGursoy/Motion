# -*- coding: utf-8 -*-

import cv2
import numpy as np

def main():
    camera = cv2.VideoCapture(0)
    camera.set(3, 640)
    camera.set(4, 480)

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
            value += 1
            print "Something movedyjnhjnhjnhjnhjnhjnhj", value

        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)

            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Webcam", image)
        cv2.imshow("Thresh", thresh)

        if cv2.waitKey(1) & 0xFF is ord('q'):
            break


if __name__ == '__main__':
    main()
