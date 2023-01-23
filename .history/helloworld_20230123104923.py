import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)
a=ti.Vector([5,2])
b=ti.Vector([1,1])
list=[a,b]

@ti.func
def temp():
    A=ti.Matrix.zero(ti.f32,3,2)
    for i in range(3):
        for j in range(2):
            A[i,j]=list[j][i]
    print(A)
    
@ti.kernel
def main():
    temp()
    
main()