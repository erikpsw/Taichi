import taichi as ti
import numpy as np
ti.init(ti.cuda)

# 窗口的宽度和高度
window_width = 800
window_height = 600

# 列数和列宽
num_columns = 128
column_width = window_width // num_columns
H=np.ones(num_columns)*0.5


        

# 创建窗口并运行 Taichi 程序
gui = ti.GUI("wave", res=(window_width, window_height))

  

while gui.running:
    gui.clear()
    # 读取用户输入，例如鼠标点击和按键
    for i in range(num_columns):
        gui.rect([i/num_columns,H[i]],[(i+1)/num_columns,0],color=0xFFFFFF,radius=2)
    gui.show()
