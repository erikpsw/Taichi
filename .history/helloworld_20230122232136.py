import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)
@ti.kernel
def main():
    A=ti.Matrix([[5,2],[2,1]])
    right=ti.Vector([8,3])
    print(ti.solve(A,right))

main()