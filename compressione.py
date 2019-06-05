#!/usr/bin/env python
from Tkinter import *
import Tkinter
import Tkinter, Tkconstants, tkFileDialog
import tkMessageBox as messagebox
from PIL import Image, ImageTk
import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct
import scipy.misc
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def dct2 (block):
  return dct(dct(block.T, norm = 'ortho').T, norm = 'ortho')

def idct2 (block):
  return idct(idct(block.T, norm = 'ortho').T, norm = 'ortho')

def stampa():
    window = Toplevel(ventana)
    window.title("Help")
    #window.geometry("400x200")
    S = Scrollbar(window)
    T = Text(window, height=30, width=75)
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=LEFT, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    quote = """
    Questo script e' stato sviluppato per eseguire la compressione
    di immagini in formato bmp.
    
    I parametri in input:
    parametro F: 
    Indica la dimensione dei blocchi nei quali sara' frammentata 
    l'immagine in input.

    Parametro d: 
    Indica la qualita' con cui l'immagine sara' compressa, a valori
    grandi corrispondono un numero di frequenze tagliate
    minore, quindi la compressione sara' bassa.

    Start process:
    Apre una schermata che permette di selezionare l'immagine da
    comprimere e successivamente inizia il processo di compressione.
    
    Output: 
    Genera un'immagine compressa con il nome outfile.bmp nella 
    stessa cartella dalla quale e' stata selezionata l'immagine 
    in input.
    
    Plot: 
    Genera un plot contenente l'immagine iniziale a sinistra e
    l'immagine compressa a destra, con l'obiettivo di rendere piu'
    facile il confronto.

    Messaggi di Error:
    "Wrong parameter F":
    Indica che il parametro F e' minore di 0.

    "F parameter > Size of image":
    Indica che il parametro F e' piu' grande della dimensione 
    dell'immagine.
    
    "Wrong parameter d":
    Indica che il parametro non e' compresso nell'intervallo 
    2*F - 2.
    """
    T.insert(END, quote)

    
def split_list(my_list,n):
    n=n/len(my_list[0])
    final = [my_list[i * n:(i + 1) * n] for i in range((len(my_list) + n - 1) // n )]
    return final 

def blockshaped(arr, nrows, ncols):
    """
    Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array should look like n subblocks with
    each subblock preserving the "physical" layout of arr.
    """
    h, w = arr.shape
    assert h % nrows == 0, "{} rows is not evenly divisble by {}".format(h, nrows)
    assert w % ncols == 0, "{} cols is not evenly divisble by {}".format(w, ncols)
    return (arr.reshape(h//nrows, nrows, -1, ncols)
               .swapaxes(1,2)
               .reshape(-1, nrows, ncols))


def message(x):
    if(x==1):
		messagebox.showinfo("Error","Wrong parameter F")
    if(x==2):
        messagebox.showinfo("Error","F parameter > Size of image")
    if(x==3):
        messagebox.showinfo("Error","Wrong parameter d")
  
def process():
    flag=True
    if parameter_F.get() <= 0:
        message(1)
        flag=False

    if parameter_d.get() < 0 or parameter_d.get() > (2*parameter_F.get() - 2):
        message(3)
        flag=False
    return flag
   
def delete_frequence(block):
    if parameter_d.get()==0:
        for i in range(len(block)):
            for j in range(len(block)):
                block[i][j]=0
        

    elif parameter_d.get()== (2*parameter_F.get()-2):
        block[-1][-1]=0
        
    else:
        for i in range(len(block)):
            for j in range(len(block)):
                if i+j >= parameter_d.get():
                    block[i][j]=0
    return block


def idct2_process(block):
    block=idct2(block)
    for i in range(len(block)):
        for j in range(len(block)):
            if(block[i][j] < 0):
                block[i][j]=0
            if(block[i][j] > 255):
                block[i][j]=255
            tmp=round(block[i][j])
            block[i][j]=int(tmp)
    return block

def build_final_image(blocks,size_rows,size_cols):
    blocks=split_list(blocks,size_cols)
    rows=[]
    for block in blocks:
        tmp= np.concatenate(block, axis=1)
        rows.append(tmp)
   
    image=np.concatenate(rows, axis=0)
    #print(image)
    scipy.misc.imsave('./immagini/outfile.bmp', image) 
    

def DCT_process(image):
    size_rows, size_cols = image.shape
    #print(image)
    dim_blocco=parameter_F.get()
    size_rows = size_rows - (size_rows%dim_blocco)
    size_cols = size_cols - (size_cols%dim_blocco)
    image_new=image[0:size_rows,0:size_cols]
    #print(image_new)
    sub_matrixs= blockshaped(image_new, dim_blocco,dim_blocco)
    mtxs_dct2=[]
    for i in range(len(sub_matrixs)):
        mtxs_dct2.append(dct2(sub_matrixs[i]))
    ff_m=[]
    for i in range(len(mtxs_dct2)):
        ff_m.append(delete_frequence(mtxs_dct2[i]))
 
    idct2_mtx=[]
    for i in range(len(ff_m)): 
        idct2_mtx.append(idct2_process(ff_m[i]))
    
    build_final_image(idct2_mtx,size_rows,size_cols)
    
def plot_image(original):
    f = plt.figure()
    original=mpimg.imread(original)
    mod=mpimg.imread('/home/ricardo/Scrivania/compressione_immagini_DCT/immagini/outfile.bmp')
    plt.axis("off") 
    f.add_subplot(1,2, 1)
    plt.title('original image')
    plt.imshow(original,cmap='gray',aspect='auto')
    plt.axis("off") 
    f.add_subplot(1,2, 2)
    plt.title('compressed image')
    plt.imshow(mod,cmap='gray',aspect='auto')
    plt.axis("off") 
    plt.suptitle('image comparison', fontsize=16)
    plt.show(block=True)

def openImage():
    control=True
    if process():
        ventana.filename = tkFileDialog.askopenfilename(initialdir = "./Scrivania",title = "Select file",filetypes = (("bmp  files","*.bmp"),("all files","*.*")))
        im = Image.open(ventana.filename)
        p = np.array(im)
        nrow, ncol= p.shape
        if parameter_F.get() > nrow or parameter_F.get() > ncol:
            message(2)
            control=False
    if control:
        DCT_process(p)
        plot_image(ventana.filename)
    


ventana = Tk()
parameter_F= IntVar()
parameter_d= IntVar()
parameter_F.set(8)


ventana.title("Compressore di immagini")
ventana.geometry("400x200")
ventana.configure(background= "#006")
readF = Label(ventana, text="Insert parameter F : ",bg="#006",fg="#FFF").place(x=10,y=10)
entry_F=Entry(ventana,textvariable=parameter_F).place(x=150,y=10)
read_d = Label(ventana, text="Insert parameter d : ",bg="#006",fg="#FFF").place(x=10,y=40)
entry_d=Entry(ventana,textvariable=parameter_d).place(x=150,y=40)


#tasto1= Button(ventana,text="read file.bmp",  command=openImage,bg="#009",fg="white").place(x=10,y=150)
tasto2= Button(ventana,text="Start Process", command=openImage,bg="#009",fg="white").place(x=10,y=150)
tasto3= Button(ventana,text="help", command=stampa,bg="#009",fg="white").place(x=325,y=150)


ventana.mainloop()
