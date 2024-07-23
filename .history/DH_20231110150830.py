import taichi as ti
ti.init(arch=ti.gpu)
import numpy as np
from math import *
I=0.25

window_width = 600

DH=np.array([
    [0,0,0,90],
    [45,0.16,-0.4,0],
    [0,-0.14,0,90],
    [0,0.45,0,90],
    [0,0,0,-90],
    [0,]
             ])
x0,y0,z0=0,0,0
pos=np.array([
    [1,0,0,x0],
    [0,1,0,y0],
    [0,0,1,z0],
    [0,0,0,1]
    ])
p_list=[]
for link in DH:
    theta=radians(link[0])
    d=link[1]
    x=link[2]
    alpha=radians(link[3])
    T=np.array([
        [cos(theta),-sin(theta)*cos(theta),sin(theta)*sin(alpha),cos(theta)*x],
        [sin(theta),cos(theta)*cos(alpha),-cos(theta)*sin(alpha),sin(theta)*x],
        [0,sin(alpha),cos(alpha),d]
        [0,0,0,1]
        ])
    pos=pos@T
    p_list.append(pos[:3,3])
p_list=np.array(p_list)

window = ti.ui.Window("Robot", (window_width, window_width))

path=[]
while window.running:

    # print(path)
    window.circles(p_list,radius=5,color=0x51acea)
    window.lines(p_list[:-1],p_list[1:],radius=2,color=0xf87064)
    # path.append(n2.pos)
    # gui.lines(begin=np.array(path[:-1]),end=np.array(path[1:]),radius=2,color=0xffffff)
    window.show()


