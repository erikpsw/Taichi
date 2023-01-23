import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)
a=ti.Vector([5,2])
b=ti.Vector([1,1])
list=(a,b)
A=ti.Matrix([[0,0],[0,0]])
for i in range(2):
    for j in range(2):
        A[j,i]=list[i][j]
@ti.kernel
def main():

    right=ti.Vector([8,2])
    print(ti.solve(A,right)[:1])

main()