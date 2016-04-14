import Tkinter as tk
import os
import cv2
from Tkinter import *
from PIL import Image, ImageTk
from tkMessageBox import *



#Global variables
width = 800
height = 600
emotionList=['Angry','Happy','Sad','Fearful','Suprised','Disgusted', 'Normal']
dictionaryForCheckEmotions = {"Angry":False, "Happy":False, "Sad": False, "Fearful": False, "Suprised": False, "Disgusted":False, "Normal":False}
selectingEmotion = ""

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


# directory checking and creating 
def directoryCheckCreate():
    for directoryName in emotionList:
        folderName = os.path.join(originFolder, directoryName)
        if not os.path.isdir(folderName):
            os.mkdir(folderName)
       
def checkPathIsThereIfnCreate():
    if not os.path.isdir(originFolder):
        os.makedirs(originFolder)
        for directoryName in emotionList:
            folderName = os.path.join(originFolder, directoryName)
            os.mkdir(folderName)
    else:
        directoryPath.delete(0, END)
        directoryPath.insert(END, originFolder)
        directoryCheckCreate()
    
        
def changeDirButtonAction():
    r = askyesno(title = 'Do you want to change directory path?', message = 'After change needed directories under this directory will be created if there is not any.')
    if r :
        global originFolder
        originFolder = directoryPath.get()
        checkPathIsThereIfnCreate()
    else:
        showinfo("Information", "We didn't changed any thing")
    os.chdir(originFolder)
    
    
#Fotograflari cekilen ogrencinin cekimi bitiginde siradaki ogrenciye gececek ve file ismi olarak siradaki ogrenci yazacak olan yapi

def StudentPictureDone():

    global dictionaryForCheckEmotions
    global personNumber
    global personImageNumber

    untakenEmotionList = ""

    for controlDictionary in dictionaryForCheckEmotions:
        if not dictionaryForCheckEmotions[controlDictionary]:
            untakenEmotionList = untakenEmotionList + ", " + controlDictionary

    if not untakenEmotionList == "":
        showwarning("Warning", "Please,take pictures of %s' emotion(s)!"%untakenEmotionList)

    else:
        print untakenEmotionList

        personNumber += 1

        personImageNumber = 0

        entryUserID.delete(0, 'end')
        
        dictionaryForCheckEmotions = {"Angry":False, "Happy":False, "Sad": False, "Fearful": False, "Suprised": False, "Disgusted":False, "Normal":False}


# Ogrencinin kacinci fotografini cektigini belirten ve bu fotograflari kaydeden fonksiyon
def takePicturePressed():
    global selectingEmotion
    if entryUserID.get() == '':
        showwarning("User ID is empty", "Please, fill the UserID!")
    else:
        global personImageNumber

        print userID

        checkImageIsNone = cv2.imread('%s/%s_%i.png'%(selectingEmotion,userID,personImageNumber))
        print checkImageIsNone
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
    selectingEmotion = str((emotionListBox.get(emotionListBox.curselection())))
    print selectingEmotion


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


#Tkinter ile button kurulumu icin gerekli root variable' i


root = tk.Tk()

root.minsize(800,620)

root.resizable(width = False, height = False)


# list box view
emotionListBox = Listbox(root, width = 11, height = 4, font = ('times',13))
emotionListBox.bind('<<ListboxSelect>>',CurSelect)
for items in emotionList:
    emotionListBox.insert(END, items)
emotionListBox.place(x = 97, y = 512)


scrollbar = Scrollbar(root)
scrollbar.place(x = 81, y = 512, height = 95)

emotionListBox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=emotionListBox.yview)


directoryPath = Entry(root, width=60)
directoryPath.place(x = 80, y = 4)
directoryPath.insert(END, originFolder)

changeDir = tk.Button(root, text = 'Change Direction', command=changeDirButtonAction)
changeDir.place(x = 586, y = 0)

takePictureButton = tk.Button(root, text="Take a Picture", command=takePicturePressed)
takePictureButton.place(x = 321, y = 514)


passAnotherStudentButton = tk.Button(root, text="Student Picture Done", command=StudentPictureDone)
passAnotherStudentButton.place(x = 301,y = 550)


labelUserID = Label(root, text = "UserID")
labelUserID.place(x = 525,y = 538)

entryUserID = Entry(root, bd = 3)
entryUserID.place(x = 595, y = 536)

userIDDoneButton = Button(root, text = "Done", command = UserIDDoneButtonPressed)
userIDDoneButton.place(x = 610, y = 570)



root.bind('<Escape>', lambda e: root.quit())

# images taken by the camera
lmain = tk.Label(root, width = 640, height = 480)
lmain.place(x = 80, y = 30)



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