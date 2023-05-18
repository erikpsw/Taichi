import taichi as ti
ti.init(arch=ti.gpu)
import numpy as np

window_width = 600
window_height = 600

gui = ti.GUI("wave", res=(window_width, window_height))

# P=np.random.rand(3,2)
P=np.array([[0.1,0.1],[0.5,0.3],[0.9,0.9]])
N=len(P)

t=0.1
tmp=np.zeros((N-1,2))

for j in range(N-1):
        tmp[j]=(1-t)*P[j]+t*P[j+1]
for i in range(1,N-1):
    for j in range(N-i-1):
        tmp[j]=(1-t)*tmp[j]+t*tmp[j+1]
    print(tmp)

while gui.running:
    gui.show()
    