import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)
@ti.func
def get_reflect_info(j_hat,ray_dir):
    i_hat=ti.Vector([-2*j_hat[1]*j_hat[2],j_hat[0]*j_hat[2],j_hat[1]*j_hat[0]]).normalized()
    k_hat=ti.math.cross(i_hat,j_hat).normalized()
    A=ti.Matrix.zero(ti.f32,3,3)
    list=[i_hat,k_hat,j_hat]
    for i in ti.static(range(3)):
        for j in ti.static(range(3)):
            A[i,j]+=list[j][i]
    ans= ti.solve(A,ray_dir)
    return (ans[0]*i_hat+ans[1]*k_hat-ans[2]*j_hat)#反射
    
@ti.kernel
def main():
    print(get_reflect_info(ti.Vector([1.,0.,1.]),ti.Vector([-1.,0.,0.])))

main()