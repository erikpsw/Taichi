import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)

@ti.kernel
def main():
    a=ti.Vector([5,2])
    b=ti.Vector([1,1])
    list=[a,b]
    A=ti.Matrix([[0,0],[0,0]])
    for i in range(2):
        for j in range(2):
            A[i,j]=list[i]
    right=ti.Vector([8,2])
    print(ti.solve(A,right))

main()