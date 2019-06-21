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


'''

#verifica richiesta
matrix = np.array([[231, 32, 233,161,24,71,140,245],
		  	       [247,40,248,245,124,204,36,107],
		  	       [234, 202, 245, 167, 9, 217, 239,173],
		  	       [193,190,100,167,43,180,8,70],
		  	       [11,24,210,177,81,243,8,112],
		  	       [97,195,203,47,125,114,165,181],
		  	       [193,70,174,167,41,30,127,245],
		  	       [87,149,57,192,65,129,178,228]])


#verifica della dct per la prima riga
test_row1=dct(matrix[0], norm= 'ortho')

#verifica di my_dct per la prima riga
mydct=dct_one(matrix[0])

#verifica della dct2 per la matrice
matrix_dct2=np.array(dct2(matrix))

print('row1: ',matrix[0])
print('DCT(row1): ',test_row1)
print('My DCT(row1): ',mydct)
print(matrix_dct2)
'''

