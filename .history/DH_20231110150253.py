import taichi as ti
ti.init(arch=ti.gpu)
import numpy as np
from math import *
I=0.25

window_width = 600
window_height = 600


DH=np.array([
    [45,0,0.2,0],
    [45,0,0.1,0]
             ])
x0,y0=0.5,0.5
pos=np.array([
    [1,0,x0],
    [0,1,y0],
    [0,0,1]
    ])
p_list=[[x0,y0]]
for link in DH:
    theta=radians(link[0])
    x=link[2]
    T=np.array([
        [cos(theta),-sin(theta),cos(theta)*x],
        [sin(theta),cos(theta),sin(theta)*x],
        [0,0,1]
        ])
    pos=pos@T
    p_list.append(pos[:2,2])
p_list=np.array(p_list)
# print(p_list[0])
window = ti.ui.Window("Rotation", (width, width))

path=[]
while gui.running:

    # print(path)
    gui.circles(p_list,radius=5,color=0x51acea)
    gui.lines(p_list[:-1],p_list[1:],radius=2,color=0xf87064)
    # path.append(n2.pos)
    # gui.lines(begin=np.array(path[:-1]),end=np.array(path[1:]),radius=2,color=0xffffff)
    gui.show()


