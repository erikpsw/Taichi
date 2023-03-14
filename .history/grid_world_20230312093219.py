import taichi as ti
import numpy as np

ti.init(ti.cuda)
pixel_size=40
grid_width=10
grid_height=10
width=pixel_size*grid_width
height=pixel_size*grid_height

class grid:
    def __init__(self,width,height) -> None:
        self.canvas=np.ones((width,height,3))

    def set_color(self,x,y,color):
        self.canvas[x*pixel_size:(x+1)*pixel_size,y*pixel_size:(y+1)*pixel_size,:]=color

class agent:
    def __init__(self,x,y) -> None:
        self.pos=[x/grid_width,y/grid_height]


line_b=np.array([[x,0] for x in range(pixel_size,width,pixel_size)])/width
line_b1=np.array([[0,y] for y in range(pixel_size,height,pixel_size)])/height
line_e=np.array([[x,width-1] for x in range(pixel_size,width,pixel_size)])/width
line_e1=np.array([[height-1,y] for y in range(pixel_size,height,pixel_size)])/height
grid_world=grid(width,height)
grid_world.set_color(3,2,[0.8,0.9,0.7])
myagent=agent(2,2)

gui=ti.GUI("grid",(width,height))
while gui.running:
    gui.set_image(grid_world.canvas)
    gui.lines(begin=np.concatenate((line_b,line_b1),axis=0), end=np.concatenate((line_e,line_e1),axis=0), radius=1, color=0x000000)
    gui.circle(myagent.pos,color=0x000000,radius=5)
    gui.show()