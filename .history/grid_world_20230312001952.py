import taichi as ti
import numpy as np

ti.init(ti.cuda)
pixel_size=40
grid_width=10
grid_height=10
width=pixel_size*grid_width
height=pixel_size*grid_height

canvas=np.ones((grid_width*pixel_size,grid_height*pixel_size,3))
line_b=np.array([[x,0] for x in range(pixel_size,width,pixel_size)])/width
line_b1=np.array([[0,y] for y in range(pixel_size,height*grid_height,pixel_size)])/height
line_e=np.array([[x,width-1] for x in range(pixel_size,width,pixel_size)])/width
line_e1=np.array([[height-1,y] for y in range(pixel_size,height,pixel_size)])/height

print(np.concatenate((line_b,line_b1),axis=0))
gui=ti.GUI("grid",(width,height))
while gui.running:
    gui.set_image(canvas)
    gui.lines(begin=np.append(line_b,line_b1), end=np.append(line_e,line_e1), radius=1, color=0x000000)
    gui.show()