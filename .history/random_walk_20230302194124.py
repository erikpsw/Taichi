import numpy as np
import taichi as ti
ti.init(ti.gpu)
def get_dir:
    ti.random()
canvas_width=100
canvas=ti.Vector.field(3, dtype=ti.f32, shape=(canvas_width, canvas_width))#三通道的画布

gui=ti.GUI("n body problem",(canvas_width,canvas_width))
while gui.running:
    gui.show()