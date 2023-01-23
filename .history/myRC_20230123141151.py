import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)
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

@ti.func
def add_rect(rect_pos,rect_normal,rect_width,rect_height,i_hat,color):
    for i,j in canvas:
        ray_dir=ti.Vector([i,j,0.])-camera_pos
        ti.static_print(ray_dir[0])
        t=plane_hit_point(camera_pos,ray_dir,rect_pos,rect_normal)
        point_pos=camera_pos+t*ray_dir
        j_hat=ti.math.cross(rect_normal,i_hat).normalized()
        vec=point_pos-rect_pos
        pos_temp=change_axes(vec,i_hat,j_hat)#使用基向量变换
        if(ti.abs(pos_temp[0])<=rect_width/2 and ti.abs(pos_temp[1])<=rect_height/2):
            canvas[i,j]+= color
        else:
            canvas[i,j]+= ti.Vector([0, 0., 0.])

@ti.kernel
def render():
    #left wall
    add_rect(ti.Vector([0.,canvas_height/2,wall_distance/2]),LEFT,wall_distance,canvas_height,FRONT,ti.Vector([0.0, 0.6, 0.0]))
    #right wall
    add_rect(ti.Vector([canvas_width,canvas_height/2,wall_distance/2]),LEFT,wall_distance,canvas_height,FRONT,ti.Vector([0.6, 0.0, 0.0]))
    #ceil
    add_rect(ti.Vector([canvas_width/2,canvas_height,wall_distance/2]),DOWN,canvas_width,wall_distance,RIGHT,ti.Vector([0.8, 0.8, 0.8]))
    #ground
    add_rect(ti.Vector([canvas_width/2,0,wall_distance/2]),DOWN,canvas_width,wall_distance,RIGHT,ti.Vector([0.8, 0.8, 0.8]))
    #back wall
    add_rect(ti.Vector([canvas_width/2,canvas_height/2,wall_distance]),FRONT,canvas_width,canvas_height,RIGHT,ti.Vector([0.8, 0.8, 0.8]))
    #light cource
    add_rect(ti.Vector([canvas_width/2,canvas_height,wall_distance/2]),DOWN,light_width,light_width,RIGHT,ti.Vector([10.0, 10.0, 10.0]))
    
    
gui = ti.GUI("Ray Tracing", res=(canvas_width, canvas_height))
canvas.fill(0)
cnt = 0

while gui.running:
    #左壁
    render()
    cnt += 1
    gui.set_image(np.sqrt(canvas.to_numpy() / cnt))#平滑化
    gui.show()
