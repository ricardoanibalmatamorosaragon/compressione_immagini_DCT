from dct2 import dct2, my_dct2
import numpy as np
import time 

def gen_matrix(start,end,rows,cols):
    a=np.random.randint(start,end, size=(rows,cols))
    return a

def main():
    np.random.seed(33)
    f = open("time_dct2.txt",'w')
    for i in range(1, 11):
        matrix=gen_matrix(1,255,100*i,100*i)
        start_dct2=time.clock()
        dct2(matrix)
        end_dct2=time.clock() - start_dct2
        start_my_dct2=time.clock()
        my_dct2(matrix)
        end_my_dct2=time.clock() - start_my_dct2
        f.write("size matrix "+str(i)+" : "+str(len(matrix))+'\n')
        f.write("time to DCT2 python : "+str(end_dct2)+'\n')
        f.write("time to My_DCT2 python : "+str(end_my_dct2)+'\n')
        f.write('\n')    
        



if __name__=="__main__":
    main()
