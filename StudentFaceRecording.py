import Tkinter as tk
from Tkinter import *
import cv2
from PIL import Image, ImageTk
import tkMessageBox
import os


#Global degiskenlerin olusturulma alani
width = 800
height = 600
itemsforlistbox=['Gulme','Kizma','Uzulme','Igrenme','Korkma','Normal']
dictionaryForCheckEmotions = {"Gulme":False, "Kizma":False, "Uzulme": False, "Igrenme": False, "Korkma": False, "Normal":False}

originFolder = os.getcwd()
print originFolder

personNumber = 0
personImageNumber = 0
userID = ''

# Taking the user id
def UserIDDoneButtonPressed():

    global userID
    userID = entryUserID.get()
    
    global personImageNumber
    personImageNumber = 0
    print userID


#Fotograflari cekilen ogrencinin cekimi bitiginde siradaki ogrenciye gececek ve file ismi olarak siradaki ogrenci yazacak olan yapi

def StudentPictureDone():

    untakenEmotionList = ""

    for controlDictionary in dictionaryForCheckEmotions:
        if not dictionaryForCheckEmotions[controlDictionary]:
            untakenEmotionList = untakenEmotionList + ", " + controlDictionary

    if not untakenEmotionList == "":
        tkMessageBox.showinfo("Uyari", "Lutfen %s' duygu fotograflarini cekiniz!"%untakenEmotionList)

    else:
        print untakenEmotionList

        global personNumber

        personNumber += 1

        global personImageNumber

        personImageNumber = 0

        entryUserID.delete(0, 'end')

# Ogrencinin kacinci fotografini cektigini belirten ve bu fotograflari kaydeden fonksiyon
def takePicturePressed():

    if entryUserID.get() == '':
        tkMessageBox.showinfo("Uyari", "Lutfen UserID' yi bos birakmayiniz!")
    else:
        global personImageNumber

        print userID

        checkImageIsNone = cv2.imread('%s/%s_%i.png'%(selectingEmotion,userID,personImageNumber))

        if checkImageIsNone is None:

            cv2.imwrite('%s/%s_%i.png'%(selectingEmotion,userID,personImageNumber),newImage)

            personImageNumber += 1

            if not dictionaryForCheckEmotions[selectingEmotion]:
            
                dictionaryForCheckEmotions[selectingEmotion] = True
        else:

            personImageNumber += 1

            takePicturePressed()
        


def CurSelect(evt):

    global selectingEmotion

    selectingEmotion = str((mylistbox.get(mylistbox.curselection())))



cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)



#Tkinter ile button kurulumu icin gerekli root variable' i



root = tk.Tk()

root.minsize(800,620)

root.resizable(width = False, height = False)

mylistbox = Listbox(root, width = 11, height = 4, font = ('times',13))

mylistbox.bind('<<ListboxSelect>>',CurSelect)

for items in itemsforlistbox:

    mylistbox.insert(END,items)




directoryPath = Entry(root, width=60)
directoryPath.place(x = 80, y = 4)
directoryPath.insert(END, originFolder)

changeDir = tk.Button(root, text = 'Change Direction', command=None )
changeDir.place(x = 586, y = 0)

takeAPictureButton = tk.Button(root, text="Take a Picture", command=takePicturePressed)

passAnotherStudentButton = tk.Button(root, text="Student Picture Done", command=StudentPictureDone)



labelUserID = Label(root, text = "UserID")
labelUserID.place(x = 525,y = 538)

entryUserID = Entry(root, bd = 3)
entryUserID.place(x = 595, y = 536)



userIDDoneButton = Button(root, text = "Tamam", command = UserIDDoneButtonPressed)
userIDDoneButton.place(x = 610, y = 570)





root.bind('<Escape>', lambda e: root.quit())

# images taken by the camera
lmain = tk.Label(root, width = 640, height = 480)
lmain.place(x = 80, y = 30)



#buttonlarin bizim canvasimiza eklenilmesi

mylistbox.place(x = 80, y = 512)

takeAPictureButton.place(x = 321, y = 514)

passAnotherStudentButton.place(x = 301,y = 550)



# Ogrencilerin kendilerini gormelerini saglayan icerisinde imshow metodu yer alan show frame fonksiyonu

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