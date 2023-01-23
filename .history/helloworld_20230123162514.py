import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)
@ti.data_oriented
class rect:
    @ti.func
    def __init__(self,rect_pos,rect_normal,rect_width,rect_height,i_hat,color):
        self.rect_pos=rect_pos
        self.rect_normal=rect_normal
        self.rect_width=rect_width
        self.rect_height=rect_height
        self.i_hat=i_hat
        self.color=color
        self.hit_point=ti.Vector([0.,0.,0.])
        
@ti.kernel
def main():
    obj=rect(ti.Vector([0.,10.,10.2]),LEFT,wall_distance,canvas_height,FRONT,ti.Vector([0.0, 0.6, 0.0]))
    
main()
