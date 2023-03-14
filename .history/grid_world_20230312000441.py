import taichi as ti
import numpy as np

ti.init(ti.cuda)
pixel_size=40
grid_width=10
grid_height=10
canvas=np.ones((grid_width*pixel_size,grid_height*pixel_size,3))
line_X=np.array([[x,0] for x in range(pixel_size,pixel_size*grid_width,pixel_size)])
line_Y=np.array([[0,y] for y in range(pixel_size,pixel_size*grid_height,pixel_size)])

gui=ti.GUI("grid",(grid_width*pixel_size,grid_height*pixel_size))
while gui.running:
    gui.lines(begin=line_X, end=line_Y, radius=0.5, color=0x000000)
    gui.set_image(canvas)
    gui.show()