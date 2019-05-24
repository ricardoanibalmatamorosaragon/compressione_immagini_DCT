import numpy as np
from scipy.fftpack import dct, idct

	
def dct2 (block):
  return dct(dct(block.T, norm = 'ortho').T, norm = 'ortho')

matrix = np.array([[231, 32, 233,161,24,71,140,245],
		  	[247,40,248,245,124,204,36,107],
		  	[234, 202, 245, 167, 9, 217, 239,173],
		  	[193,190,100,167,43,180,8,70],
		  	[11,24,210,177,81,243,8,112],
		  	[97,195,203,47,125,114,165,181],
		  	[193,70,174,167,41,30,127,245],
		  	[87,149,57,192,65,129,178,228]])

#print(dct2(matrix))
#print(matrix)

test_matrix=dct2(matrix)
test_row1=dct(matrix[0], norm= 'ortho')
print('row1: ',matrix[0],' DCT(row1): ',test_row1)


