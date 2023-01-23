import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)
@ti.kernel
def main():
    a=ti.Vector([5,2])
    b=ti.Vector([1,1])
    A=ti.Matrix([[5,1],[2,1]])
    right=ti.Vector([8,2])
    print(ti.solve(A,right))

main()