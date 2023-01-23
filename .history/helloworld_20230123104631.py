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
    A=ti.Matrix.zero(ti.f32,3,2)
    right=ti.Vector([8,2])
    for i in range(3):
        for
    print(ti.Matrix(np.ndarray([a.to_list(),b.to_list()])))

main()