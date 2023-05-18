import taichi as ti
ti.init(arch=ti.gpu)
import numpy as np

window_width = 600
window_height = 600

gui = ti.GUI("wave", res=(window_width, window_height))

P=np.random.rand(6,2)
N=len(P)

t=0.5
tmp=np.zeros((N-1,2))

def deCastel(t)
    for j in range(N-1):
        tmp[j]=(1-t)*P[j]+t*P[j+1]
    for i in range(1,N-1):
        for j in range(N-i-1):
            tmp[j]=(1-t)*tmp[j]+t*tmp[j+1]
print(tmp[0])

while gui.running:
    gui.show()
    