import numpy as np
from scipy.fftpack import dct, idct
import math 
	
def dct2 (block):
  return dct(dct(block.T, norm = 'ortho').T, norm = 'ortho')


def dct_one(vector):
    lista=[]
    size = len(vector)

    for k in range(size):
        ck =0.0
        if k==0:
            alfa_k_N=1.0/math.sqrt(size)
        else :
            alfa_k_N=math.sqrt((2.0/size))
          
        for i in range(size):
            fi=vector[i]
            coseno=math.cos(float(math.pi*(2.0*i+1)*k)/float(2.0*size))
            ck+=float(fi*coseno)
        lista.append(round(float(alfa_k_N*ck),8))        
    return np.array(lista)


def my_dct(block):
    tmp=[]
    for row in block:
        tmp.append(dct_one(row))
    return np.array(tmp)


def my_dct2(block):
    result_row_dct=my_dct(block)
    tras=result_row_dct.T
    result=my_dct(tras)
    return result.T
