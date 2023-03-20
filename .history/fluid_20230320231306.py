import taichi as ti
import numpy as np
ti.init(ti.cuda)

# 窗口的宽度和高度
window_width = 600
window_height = 600
beta=1
alpha=0.5

# 列数和列宽
num_columns = 256
column_width = window_width // num_columns
hmax=0.8
H=np.array([0.8*i/num_columns for i in range(num_columns)])
Hold=np.array([0.8*i/num_columns for i in range(num_columns)])
Hnew=np.zeros(num_columns)

# 创建窗口并运行 Taichi 程序
gui = ti.GUI("wave", res=(window_width, window_height))



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
