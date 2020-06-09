import imutils
import os
import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import ImageTk,Image
import Preprocess as pp
import Calibration as cal

import DetectChars
import DetectPlates
import PossiblePlate

filename=""
gambar=None
render = None
image = None
orimage = None
render2 = None
render3 = None
def UploadAction(event=None):
    global filename
    global gambar
    global image
    global render
    global orimage
    filename = filedialog.askopenfilename(title = "Select file",filetypes = (("jpeg files","*.jpg *.jpeg"),("all files","*.*")))
    orimage = cv2.imread(filename)
    image = cv2.cvtColor(orimage, cv2.COLOR_BGR2RGB)
    imgScale = 300/image.shape[1]
    image = cv2.resize(image,(int(300),int(150)))
    gambar = Image.fromarray(image)
    render = ImageTk.PhotoImage(gambar)
    img = tk.Label(r,image=render)
    img.place(x=340,y=100)

def ProcessAction(event=None):
    global orimage
    global render2
    global render3
    global textok
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()
    if blnKNNTrainingSuccessful == False:
        print("\nerror: KNN traning was not successful\n")   
    resizedimage  = imutils.resize(orimage, width = 720)
    imgGrayscale, imgThresh = pp.preprocess(resizedimage)
    resizedimage = imutils.transform (resizedimage)
    # imgThresh = imutils.transform (imgThresh)
    resizedimage,license,gambarlicense = searching(resizedimage,False)
    if(gambarlicense==None):
        textok.set(value="Tidak ditemukan TNKB")
        return
    gambarlicense.imgPlate = cv2.cvtColor(gambarlicense.imgPlate, cv2.COLOR_BGR2RGB)
    imgScale = 300/gambarlicense.imgPlate.shape[1]
    gambarlicense.imgPlate = cv2.resize(gambarlicense.imgPlate,(int(gambarlicense.imgPlate.shape[1]*imgScale),int(gambarlicense.imgPlate.shape[0]*imgScale)))
    gambar2 = Image.fromarray(gambarlicense.imgPlate)
    render2 = ImageTk.PhotoImage(gambar2)
    # gambar3 = Image.fromarray(imgThresh)
    # render3=ImageTk.PhotoImage(gambar3)
    img2 = tk.Label(image=render2)
    img2.place(x=340,y=350)
    # img2 = tk.Label(image=render3)
    # img2.place(x=640,y=100)
    textok.set(value=license)
    

def searching(imgOriginalScene,loop):
    licenses = ""
    if imgOriginalScene is None:                            # if image was not read successfully
        print("error: image not read from file \n")      # print error message to std out
        os.system("pause")                                  # pause so user can see error message
        return
        # end if
    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)           # detect plates
    #time.sleep(0.02)
    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        # detect chars in plates
    #time.sleep(0.05)

    if len(listOfPossiblePlates) == 0:
        if (loop == False):                          # if no plates were found
            print("no license plates were detected\n")             # inform user no plates were found
            return None,None,None
    else:                                                       # else
                    # if we get in here list of possible plates has at leat one plate

                    # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)
                    # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
        licPlate = listOfPossiblePlates[0]

        if len(licPlate.strChars) == 0:                     # if no chars were found in the plate
            if (loop == False):
                print("no characters were detected\n")
                return       # show message
            # end if
        licenses = licPlate.strChars
        # if ((licenses[0] and licenses[len(licenses)-1])  == ('0' or '1' or '2' or '3' or '4' or  '5' or '6' or '7' or '8' or '9')):
        #     licenses = ""
        #     print("license plate False !! \n and ")
                          # draw red rectangle around plate
        #print (licenses)
        #print(licPlate)
        if (loop == False):
            print("license plate read from image = " + licPlate.strChars + "\n")       # write license plate text to std out
                  # write license plate text on the image


    return imgOriginalScene, licenses, licPlate

r = tk.Tk()
r.title('UAS PACD')
button = tk.Button(r, text='Buka Gambar', width = 25, command = UploadAction)
button.place(x=50, y=100)
button = tk.Button(r, text='Proses Gambar', width = 25, command = ProcessAction)
button.place(x=50, y=200)
label = tk.Label(r, text='Tulisan TNKB')
label.place(x=50, y=350)
textok = tk.StringVar()
textbox = tk.Entry(r, width=10, textvariable=textok)
textbox.place(x=50, y=370)
r.geometry("1000x500")
r.mainloop()