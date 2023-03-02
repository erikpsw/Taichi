import numpy as np
import taichi as ti
ti.init(ti.gpu)
canvas_width=100
canvas=ti.Vector.field(3, dtype=ti.f32, shape=(canvas_width, canvas_width))#三通道的画布

gui=ti.GUI("n body problem",(512,512))
while gui.running:
    gui.show()