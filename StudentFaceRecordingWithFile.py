import Tkinter as tk
import cv2
from PIL import Image, ImageTk
import argparse

personNumber = 0
personImageNumber = 0

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", help="Path to the imput text")
args = vars(ap.parse_args())

if(args > 1):
    f = open(args["file"],'w+')
    f.write('712_0')
    f.seek(0)
    inputString = f.readline()
    inputList = inputString.split('_')
    lastPersonNumber = int(inputList[0])
    personNumber = lastPersonNumber
    personImageNumber = int(inputList[1])
    
else:
    personNumber = 0
    personImageNumber = 0

def StudentPictureDone():
	global personNumber
	personNumber += 1
	global personImageNumber
	personImageNumber = 0
	f.seek(0)
	f.write(str(personNumber)+'_'+str(personImageNumber))


def Pressed():
	global personImageNumber
	cv2.imwrite('Person%iImage%i.png'%(personNumber,personImageNumber),newImage)
	personImageNumber += 1
	f.seek(0)
	f.write(str(personNumber)+'_'+str(personImageNumber))


width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)



root = tk.Tk()
takeAPictureButton = tk.Button(root, text="Take a Picture", command=Pressed)
passAnotherStudentButton = tk.Button(root, text="Student Picture Done", command=StudentPictureDone)
root.bind('<Escape>', lambda e: root.quit())
lmain = tk.Label(root)
lmain.pack()

takeAPictureButton.pack()
passAnotherStudentButton.pack()


lmain = tk.Label(root)
lmain.pack()

takeAPictureButton.pack()
passAnotherStudentButton.pack()

def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    global newImage
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    newImage = frame
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    imageSaved = cv2image
    lmain.after(100, show_frame)

show_frame()
root.mainloop()
