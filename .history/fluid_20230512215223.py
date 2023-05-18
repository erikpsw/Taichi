import taichi as ti
import numpy as np
ti.init(ti.cuda)

# 窗口的宽度和高度
window_width = 600
window_height = 600
beta=0.987#阻尼
alpha=0.5

# 列数和列宽
num_columns = 256
column_width = window_width // num_columns
hmax=0.8
H=np.array([np.abs(np.sin(3*i/num_columns))/2 for i in range(num_columns)])
Hold=np.array([np.abs(np.sin(3*i/num_columns))/2 for i in range(num_columns)])
Hnew=np.zeros(num_columns)


while gui.running:
    Hnew=H+beta*(H-Hold)
    gui.clear()
    for i in range(num_columns):
        if(i>0):
            Hnew[i]+=alpha*(H[i-1]-H[i])
        if(i<num_columns-1):
            Hnew[i]+=alpha*(H[i+1]-H[i])
    Hold=H
    H=Hnew

    for i in range(num_columns):
        x=i/num_columns
        xn=(i+1)/num_columns
        gui.triangles(np.array([[x,H[i]],[x,H[i]]]),np.array([[x,0],[xn,H[i]]]),np.array([[xn,0],[xn,0]]),color=0x00aeec)
    gui.show()
