import taichi as ti
import numpy as np

ti.init(ti.cuda)
pixel_size=40
grid_width=10
grid_height=10
canvas=np.ones((grid_width*pixel_size,grid_height*pixel_size,3))
line_b=np.array([[[x,0] for x in range(pixel_size,pixel_size*grid_width,pixel_size)]])/(pixel_size*grid_width)
line_b1=np.array([[0,y] for y in range(pixel_size,pixel_size*grid_height,pixel_size)])/(pixel_size*grid_height)
line_b.ex

gui=ti.GUI("grid",(grid_width*pixel_size,grid_height*pixel_size))
print(line_X)
while gui.running:
    gui.set_image(canvas)
    gui.lines(begin=line_X, end=line_Y, radius=1, color=0x000000)
    gui.show()