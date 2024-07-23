import taichi as ti
import numpy as np
ti.init(arch=ti.gpu)


target=0.5
y=0.5
gui = ti.GUI('pid')

kp=1
ki=1
kd=1
x=0.3
err_sum=0
dt=0.001

while gui.running:
    err=target-x
    err_sum+=abs(err)
    v=abs(err)/dt
    F=kp*err-ki*err_sum-kd*v
    print(x)
    x+=F*dt
    gui.circle([target,y], radius=10)
    gui.circle([x,y], radius=10)
    gui.show()