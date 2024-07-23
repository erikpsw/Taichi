import taichi as ti
import numpy as np
ti.init(arch=ti.gpu)


target=0.5
y=0.5
gui = ti.GUI('pid')

kp=0.1
ki=0.001
kd=0.01
x=0.3
err_sum=0
dt=0.5

while gui.running:
    err=target-x
    err_sum+=err
    v=err/(1e4*dt)
    F=kp*err+ki*err_sum+kd*v
    print('x={} F={}'.format(x,F))
    x+=F*dt
    gui.circle([target,y], radius=5)
    gui.circle([x,y], radius=5)
    gui.show()