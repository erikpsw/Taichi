import taichi as ti
ti.init(arch=ti.gpu)
import numpy as np

theta=np.pi/4
lmax=15
R=5/lmax
a=8/lmax
b=3/lmax

window_width = 600
window_height = 600
beta=np.arccos(((2*R*np.cos(theta))**2+a**2-b**2)/(2*a*2*R*np.cos(theta)))
alpha=np.arccos((a**2-b**2-(2*R*np.cos(theta))**2)/(2*b*2*R*np.cos(theta)))

gui = ti.GUI("wave", res=(window_width, window_height))


B=[2*R*np.cos(theta)**2,2*R*np.cos(theta)*np.sin(theta)]
A=[0,0]
C=[B[0]+np.cos(alpha+theta)*b,B[1]+np.sin(alpha+theta)*b]
D=[B[0]+np.cos(theta-alpha)*b,B[1]+np.sin(theta-alpha)*b]
while gui.running:
    gui.circle(B,radius=5)
    gui.lines()
    gui.show()