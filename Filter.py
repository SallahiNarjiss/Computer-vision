# Apply some filtr to your images with Narjiss !
import cv2 
import easygui 
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import *


top=tk.Tk()
top.geometry('400x400')
top.title('Apply a filter with Narjiss!')
top.configure(background='pink')
label=Label(top,background='#CDCDCD', font=('calibri',30,'bold'))

def upload():
    ImagePath=easygui.fileopenbox()
    Filter(ImagePath)


def Filter(ImagePath):

    input_image = cv2.imread(ImagePath)
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
    
    if input_image is None:
        print("Can not find any image. Choose an appropriate file")
        sys.exit()

    Filter1 = cv2.resize(input_image, (960, 940))

    grayScaleImage= cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    Filter2 = cv2.resize(grayScaleImage, (960, 940))

    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    Filter3 = cv2.resize(smoothGrayScale, (960, 940))

    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)

    Filter4 = cv2.resize(getEdge, (960, 940))

    colorImage = cv2.bilateralFilter(input_image, 9, 300, 300)
    Filter5 = cv2.resize(colorImage, (960, 940))

    last_filter = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    Filter6 = cv2.resize(last_filter, (960, 940))

    images=[Filter1, Filter2, Filter3, Filter4, Filter5, Filter6]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    save1=Button(top,text="Save the filtered image !",command=lambda: save(Filter6, ImagePath),padx=30,pady=10)
    save1.configure(background='#364156', foreground='Black',font=('calibri',20,'bold'))
    save1.pack(side=TOP,pady=50)
    
    plt.show()
    
    
def save(Filter6, ImagePath):

    newName="Filtered_Image"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(Filter6, cv2.COLOR_RGB2BGR))
    I= "Narjiss hopes that  you enjoyed the experience and the image is saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)

upload=Button(top,text="Apply the filter",command=upload,padx=20,pady=10)
upload.configure(background='#364156', foreground='black',font=('calibri',20,'bold'))
upload.pack(side=TOP,pady=50)

top.mainloop()

