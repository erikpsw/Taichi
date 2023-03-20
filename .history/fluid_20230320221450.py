import taichi as ti
import numpy as np
ti.init(ti.cuda)

# 窗口的宽度和高度
window_width = 800
window_height = 600

# 列数和列宽
num_columns = 128
column_width = window_width // num_columns
H=np.zeros(num_columns)*0.5


        

# 创建窗口并运行 Taichi 程序
gui = ti.GUI("128列GUI", res=(window_width, window_height))
@ti.kernel
def render(H):
    # 绘制每一列的矩形，并设置颜色
    for i in range(num_columns):
        gui.rect([i/num_columns,H[i]],[(i+1)/num_columns,0])

gui.rect()
while gui.running:
    # 读取用户输入，例如鼠标点击和按键
    for e in gui.get_events(ti.GUI.PRESS):
        # 如果用户按下了数字键 1，将第一列的颜色设置为红色
        if e.key == ti.GUI.NUM_1:
            set_color(0, 1.0, 0.0, 0.0)
        # 如果用户按下了数字键 2，将第一列的颜色设置为绿色
        elif e.key == ti.GUI.NUM_2:
            set_color(0, 0.0, 1.0, 0.0)
        # 如果用户按下了数字键 3，将第一列的颜色设置为蓝色
        elif e.key == ti.GUI.NUM_3:
            set_color(0, 0.0, 0.0, 1.0)
    # 绘制 GUI
    render()
    gui.show()
