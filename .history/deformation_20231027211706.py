import taichi as ti
import numpy as np


gui=ti.GUI("deformation",(512,512))

for i in np.linspace(0,0.5,5):
    for j in np.linspace(0,0.5,5):
        [i,j]
pos=np.array(pos)

while gui.running:
    gui.circles(pos,color=0xffffff,radius=4)
    gui.show()