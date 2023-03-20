import taichi as ti
import numpy as np
ti.init(ti.cuda)

# 窗口的宽度和高度
window_width = 600
window_height = 600

# 列数和列宽
num_columns = 64
column_width = window_width // num_columns
hmax=0.8
H=[0.8*i/num_columns for i in range(num_columns)]
Hold=[0.8*i/num_columns for i in range(num_columns)]

# 创建窗口并运行 Taichi 程序
gui = ti.GUI("wave", res=(window_width, window_height))

while gui.running:
    gui.clear()
    # 读取用户输入，例如鼠标点击和按键
    for i in range(num_columns):
        x=i/num_columns
        xn=(i+1)/num_columns
        gui.triangles(np.array([[x,H[i]],[x,H[i]]]),np.array([[x,0],[xn,H[i]]]),np.array([[xn,0],[xn,0]]),color=0x00aeec)
    gui.show()
