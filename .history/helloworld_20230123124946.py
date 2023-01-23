import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)
a=ti.Vector([0,5,2])
b=ti.Vector([0,1,1])
list=[a,b]
vec=ti.Vector([0,8,2])

@ti.kernel
def change_axes(vec,i_hat,j_hat):
    list=[i_hat,j_hat]
    A=ti.Matrix([[0.,0.],[0.,0.]])#三维变二维，要非零
    right=ti.Vector([0.,0.])
    if(list[0][2]==0):
        for i in ti.static(range(2)):
            for j in ti.static(range(2)):
                A[i,j]+=list[j][i]
        right+=vec[:2]
        
    elif(list[0][1]==0):
        A[0,0]+=list[0][0]
        A[0,1]+=list[1][0]
        A[1,0]+=list[0][2]
        A[1,1]+=list[1][2]
        right+=ti.Vector([vec[0],vec[2]])
        
    else:
        A[0,0]+=list[0][1]
        A[0,1]+=list[1][1]
        A[1,0]+=list[0][2]
        A[1,1]+=list[1][2]
        right+=vec[1:3]
    return ti.solve(A,right)
print(change_axes(vec,a,b))
