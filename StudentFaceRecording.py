import Tkinter as tk
import cv2
from PIL import Image, ImageTk

#Global degiskenlerin olusturulma alanı
personNumber = 0
personImageNumber = 0

#Fotografları cekilen ogrencinin cekimi bitiginde sıradaki ogrenciye gececek ve file ismi olarak sıradaki ogrenci yazacak olan yapı
def StudentPictureDone():
	global personNumber
	personNumber += 1
	global personImageNumber
	personImageNumber = 0

# Ogrencinin kacıncı fotografını cektigini belirten ve bu fotografları kaydeden fonksiyon
def Pressed():
	global personImageNumber
	cv2.imwrite('Person%iImage%i.png'%(personNumber,personImageNumber),newImage)
	personImageNumber += 1


width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

#Tkinter ile button kurulumu için gerekli root variable' ı

root = tk.Tk()
takeAPictureButton = tk.Button(root, text="Take a Picture", command=Pressed)
passAnotherStudentButton = tk.Button(root, text="Student Picture Done", command=StudentPictureDone)
root.bind('<Escape>', lambda e: root.quit())
#capturing video gosterme alanı
lmain = tk.Label(root)
lmain.pack()

#buttonların bizim canvasımıza eklenilmesi
takeAPictureButton.pack()
passAnotherStudentButton.pack()

# Ogrencilerin kendilerini gormelerini saglayan içerisinde imshow metodu yer alan show frame fonksiyonu
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
