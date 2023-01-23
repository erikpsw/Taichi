import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)
a=ti.Vector([5,0,2])
b=ti.Vector([1,0,1])
list=[a,b]
vec=ti.Vector([8,3])

def change_axes(vec,i_hat,j_hat):
    list=[i_hat.to_numpy(),j_hat.to_numpy()]
    A=np.array([[0.,0.],[0.,0.]])#三维变二维，要非零
    if(list[0][2]==0):
        for i in ti.static(range(2)):
            for j in ti.static(range(2)):
                A[i,j]+=list[j][i]
        return np.solve(A,vec[:2])
    elif(list[0][1]==0):
        temp=[0,2]#取非零元素的矩阵
        for i in ti.static(range(2)):
            for j in ti.static(range(2)):
                A[j,i]=list[temp[i]][temp[j]]
        return np.solve(A,vec[[0,2]])
    else:   
        temp=range(1,3)#取非零元素的矩阵
        for i in ti.static(range(2)):
            for j in ti.static(range(2)):
                A[j,i]=list[temp[i]][temp[j]]
        return np.solve(A,vec[[1,2]])
change_axes(vec,a,b)
