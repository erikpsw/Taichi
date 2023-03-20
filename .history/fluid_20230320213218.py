import taichi as ti
ti.init(ti.cuda)

# 窗口的宽度和高度
window_width = 800
window_height = 600

# 列数和列宽
num_columns = 128
column_width = window_width // num_columns

# 定义颜色的参数
color_r = ti.var(dt=ti.f32, shape=num_columns)
color_g = ti.var(dt=ti.f32, shape=num_columns)
color_b = ti.var(dt=ti.f32, shape=num_columns)

# Taichi 程序的主函数
@ti.func
def set_color(col_idx, r, g, b):
    # 将指定列的颜色设置为指定的 RGB 值
    color_r[col_idx] = r
    color_g[col_idx] = g
    color_b[col_idx] = b

@ti.kernel
def render():
    # 绘制每一列的矩形，并设置颜色
    for i in range(num_columns):
        ti.fill(ti.vec(color_r[i], color_g[i], color_b[i]),
                (i * column_width, 0), ((i+1) * column_width, window_height))

# 创建窗口并运行 Taichi 程序
gui = ti.GUI("128列GUI", res=(window_width, window_height))
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
