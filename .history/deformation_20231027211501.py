import taichi as ti
import numpy as np


gui=ti.GUI("deformation",(512,512))

pos=np.array([])

while gui.running:
    gui.circles(pos,color=0xffffff,radius=4)
    gui.show()