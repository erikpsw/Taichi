import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)
INF=100
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

@ti.func
def plane_hit_point(start_pos,ray_dir,plane_pos,plane_normal):
    nume=0.
    deno=0.
    for i in ti.static(range(3)):#三个分量
        nume+=(plane_pos[i]-start_pos[i])*plane_normal[i]
        deno+=ray_dir[i]*plane_normal[i]
    return nume/deno

@ti.func
def change_axes(vec,i_hat,j_hat):
    list=[i_hat,j_hat]
    A=ti.Matrix([[0.,0.],[0.,0.]])#三维变二维，要非零，需要试一下
    right=ti.Vector([0.,0.])
    if(list[0][2]==0 and list[1][2]==0):
        for i in ti.static(range(2)):
            for j in ti.static(range(2)):
                A[i,j]+=list[j][i]
        right+=vec[:2]
        
    elif(list[0][1]==0 and list[1][1]==0):
        A[0,0]+=list[0][0]
        A[0,1]+=list[1][0]
        A[1,0]+=list[0][2]
        A[1,1]+=list[1][2]
        right+=ti.Vector([vec[0],vec[2]])
        
    else:
        A[0,0]+=list[0][1]
        A[0,1]+=list[1][1]
        A[1,0]+=list[0][2]
        A[1,1]+=list[1][2]
        right+=vec[1:3]
    return ti.solve(A,right)

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
        self.t=INF
        self.hit_point=ti.Vector([0.,0.,0.])
    
    @ti.func
    def get_t(self,start_pos,ray_dir):
        temp=plane_hit_point(start_pos,ray_dir,self.rect_pos,self.rect_normal)
        if(temp>0):#此时不一定相交
            point_pos=camera_pos+temp*ray_dir
            j_hat=ti.math.cross(self.rect_normal,self.i_hat).normalized()
            vec=point_pos-self.rect_pos
            pos_temp=change_axes(vec,self.i_hat,j_hat)#使用基向量变换
            if(ti.abs(pos_temp[0])<=self.rect_width/2 and ti.abs(pos_temp[1])<=self.rect_height/2):
                self.hit_point=pos_temp
                self.t=temp
                return temp
    
    @ti.func  
    def hit_ray(self):
        return self.color

@ti.func
def build_sence():
    Hierarchy=[]
    #left wall
    Hierarchy.append(rect(ti.Vector([0.,canvas_height/2,wall_distance/2]),LEFT,wall_distance,canvas_height,FRONT,ti.Vector([0.0, 0.6, 0.0])))
    #right wall
    Hierarchy.append(rect(ti.Vector([canvas_width,canvas_height/2,wall_distance/2]),LEFT,wall_distance,canvas_height,FRONT,ti.Vector([0.6, 0.0, 0.0])))          
    #ground
    Hierarchy.append(rect(ti.Vector([canvas_width/2,0,wall_distance/2]),DOWN,canvas_width,wall_distance,RIGHT,ti.Vector([0.8, 0.8, 0.8])))
    #back wall
    Hierarchy.append(rect(ti.Vector([canvas_width/2,canvas_height/2,wall_distance]),FRONT,canvas_width,canvas_height,RIGHT,ti.Vector([0.8, 0.8, 0.8])))
    #light cource
    Hierarchy.append(rect(ti.Vector([canvas_width/2,canvas_height,wall_distance/2]),DOWN,light_width,light_width,RIGHT,ti.Vector([10.0, 10.0, 10.0])))
    return Hierarchy
    
@ti.kernel
def render():
    # hierarchy=build_sence()
    if(cnt<=1):
        for i,j in canvas:
            ray_dir=ti.Vector([i,j,0.])-camera_pos
            obj=rect(ti.Vector([0.,canvas_height/2,wall_distance/2]),LEFT,wall_distance,canvas_height,FRONT,ti.Vector([0.0, 0.6, 0.0]))
     
    
gui = ti.GUI("Ray Tracing", res=(canvas_width, canvas_height))
canvas.fill(0)
cnt = 0

while gui.running:
    #左壁
    cnt += 1
    render()
    
    gui.set_image(np.sqrt(canvas.to_numpy() / cnt))#平滑化
    gui.show()
