import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)
INF=100.
LEFT=ti.Vector([1.,0.,0.])
RIGHT=ti.Vector([-1.,0.,0.])
UP=ti.Vector([0.,1.,0.])
DOWN=ti.Vector([0.,-1.,0.])
FRONT=ti.Vector([0.,0.,-1.])
BACK=ti.Vector([0.,0.,1.])


fov=np.pi/3
u=200#一个单位所对应的像素值
camera_distance=5*u#相机距离
canvas_ratio=1#高宽比
canvas_height=round(camera_distance*np.tan(fov/2))
canvas_width=canvas_height*canvas_ratio
camera_pos=ti.Vector([canvas_width/2,canvas_height/2,-camera_distance],ti.f32)
canvas=ti.Vector.field(3, dtype=ti.f32, shape=(canvas_width, canvas_height))#三通道的画布
wall_distance=3*u#后壁的距离
light_width=u
max_depth=1


class rect:
    def __init__(self,rect_pos,rect_normal,rect_width,rect_height,i_hat,color):
        self.rect_pos=rect_pos
        self.rect_normal=rect_normal
        self.rect_width=rect_width
        self.rect_height=rect_height
        self.i_hat=i_hat
        self.color=color
        
@ti.kernel
def main():
    obj=rect(1,LEFT,wall_distance,canvas_height,FRONT,ti.Vector([0.0, 0.6, 0.0]))
    
main()
