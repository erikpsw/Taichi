import taichi as ti
import numpy as np

@ti.func
def temp():
    a=ti.Vector([5,2])
    b=ti.Vector([1,1])
    arr=np.ndarray(a.to_numpy().T,b.to_numpy().T)
    return arr

ti.init(arch=ti.gpu)
@ti.kernel
def main():

    print(temp)
    A=ti.Matrix([[5,1],[2,1]])
    right=ti.Vector([8,2])
    print(ti.solve(A,right))

main()