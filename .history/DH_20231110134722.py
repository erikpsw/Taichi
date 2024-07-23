import taichi as ti
ti.init(arch=ti.cpu)
import numpy as np
from cmath import *
I=0.25

window_width = 600
window_height = 600

DH=np.array([[]])

# print(p_list[0])
gui = ti.GUI("robot", res=(window_width, window_height))
p_list=[]
path=[]
while gui.running:

    # print(path)
    gui.circles(p_list,radius=5,color=0x51acea)
    gui.lines(p_list[:-1],p_list[1:],radius=2,color=0xf87064)
    # path.append(n2.pos)
    gui.lines(begin=np.array(path[:-1]),end=np.array(path[1:]),radius=2,color=0xffffff)
    gui.show()


