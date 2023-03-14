import taichi as ti
import numpy as np

ti.init(ti.cuda)
pixel_size=40
canvas_width=10
canvas_width=10
canvas=np.ones((canvas_width*pixel_size,canvas_width*pixel_size,3))
line_X=
line_Y=

gui=ti.GUI("grid",(canvas_width*pixel_size,canvas_width*pixel_size))
while gui.running:
    gui.lines(begin=line_X, end=line_Y, radius=2, color=0x000000)
    gui.set_image(canvas)
    gui.show()