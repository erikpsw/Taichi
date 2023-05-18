import taichi as ti
ti.init(arch=ti.gpu)
import numpy as np
from scipy.special import comb

window_width = 600
window_height = 600

gui = ti.GUI("wave", res=(window_width, window_height))

P=np.random.rand(3,2)
N=len(P)


t=0.1
for i in range(N):
    for j in range(N-i-1):
        tmp=comb(i+1)
        print(tmp)

while gui.running:
    gui.show()
    