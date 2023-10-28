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
EPS=0.1
fov=np.pi/3
u=200#一个单位所对应的像素值
camera_distance=5.1*u#相机距离
canvas_ratio=1#高宽比
canvas_height=round(camera_distance*np.tan(fov/2))
canvas_width=canvas_height*canvas_ratio
camera_pos=ti.Vector([canvas_width/2,canvas_height/2,-camera_distance],ti.f32)
canvas=ti.Vector.field(3, dtype=ti.f32, shape=(canvas_width, canvas_height))#三通道的画布
wall_distance=3*u#后壁的距离
light_width=u
max_depth=2
sample_per_pixel=5
proportion=0.2
p_RR = 0.8#轮盘赌概率
p=0.8
light_pos=ti.Vector([canvas_width/2,canvas_height+1,wall_distance/2])


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
    def __init__(self,rect_pos,rect_normal,rect_width,rect_height,i_hat,color,is_light,material):
        self.rect_pos=rect_pos
        self.rect_normal=rect_normal
        self.rect_width=rect_width
        self.rect_height=rect_height
        self.i_hat=i_hat
        self.color=color
        self.is_light=is_light#0为任意物体，1为光源
        self.material=material#0漫反射，1镜面
    
    @ti.func
    def get_hit_info(self,start_pos,ray_dir):
        temp=plane_hit_point(start_pos,ray_dir,self.rect_pos,self.rect_normal)
        t=INF
        point_pos=ti.Vector([0.,0.,0.])
        j_hat=ti.Vector([0.,0.,0.])
        
        if(temp>0):#此时不一定相交
            point_pos=start_pos+temp*ray_dir
            j_hat+=ti.math.cross(self.rect_normal,self.i_hat).normalized()
            vec=point_pos-self.rect_pos
            pos_temp=change_axes(vec,self.i_hat,j_hat)#使用基向量变换
            if(ti.abs(pos_temp[0])<=self.rect_width/2 and ti.abs(pos_temp[1])<=self.rect_height/2):
                t=temp
        return t,point_pos,j_hat#得到t和击中点
    
    
    @ti.func
    def hit_cos(self,ray_dir,j_hat):#获取视线的颜色
        cos=ti.math.dot(ray_dir,self.rect_normal)/(ray_dir.norm())
        return ti.abs(cos)#视角要乘上cos
    
    @ti.func
    def get_reflect_info(self,j_hat,ray_dir):
        A=ti.Matrix.zero(ti.f32,3,3)
        list=[self.i_hat,j_hat,self.rect_normal]
        for i in ti.static(range(3)):
            for j in ti.static(range(3)):
                A[i,j]+=list[j][i]
        ans= ti.solve(A,ray_dir)
        return (ans[0]*self.i_hat+ans[1]*j_hat-ans[2]*self.rect_normal)#反射
        
    @ti.func
    def get_diffuse_info(self,j_hat):
        theta=ti.math.acos(2*ti.random(ti.f32)-1)
        phi=ti.random()*ti.math.pi*2
        x=ti.cos(phi)*ti.sin(theta)
        y=ti.sin(phi)*ti.sin(theta)
        z=ti.cos(theta)
        return(x*self.i_hat+y*j_hat+z*self.rect_normal)
    
    @ti.func
    def light_cos(self,light_dir,j_hat):#获取视线的颜色
        cos=ti.math.dot(light_dir,self.rect_normal)/(light_dir.norm())
        return ti.abs(cos)#视角要乘上cos

@ti.data_oriented
class Sphere:
    def __init__(self,center_pos,radius,color,is_light,material):
        self.center_pos=center_pos
        self.radius=radius
        self.color=color
        self.is_light=False
        self.is_light=is_light
        self.material=material
    
    @ti.func
    def get_hit_info(self,start_pos,ray_dir):
        M=start_pos-self.center_pos
        t=INF
        a=0.
        b=0.
        c=-self.radius**2
        j_hat=ti.Vector([0.,0.,0.])
        hit_pos=ti.Vector([0.,0.,0.])
        for i in range(3):
            a+=ray_dir[i]**2
            b+=2*ray_dir[i]*M[i]
            c+=M[i]**2
        t1=(-b+ti.sqrt(b**2-4*a*c))/(2*a)
        t2=(-b-ti.sqrt(b**2-4*a*c))/(2*a)
        if(not(t1<=0 and t2<=0)):
            if((t1>0 and t2>0)):
                t=min(t1,t2)
            else:
                t=max(t1,t2)
        if(t!=INF):
            hit_pos=start_pos+t*ray_dir
            j_hat=(hit_pos-self.center_pos).normalized()#连接球心得到方向
        return t,hit_pos,j_hat

    @ti.func
    def get_diffuse_info(self,j_hat):#散射光线
        i_hat=ti.Vector([-2*j_hat[1]*j_hat[2],j_hat[0]*j_hat[2],j_hat[1]*j_hat[0]]).normalized()
        k_hat=ti.math.cross(i_hat,j_hat).normalized()
        theta=ti.math.acos(2*ti.random(ti.f32)-1)
        phi=ti.random()*ti.math.pi*2
        x=ti.cos(phi)*ti.sin(theta)
        y=ti.sin(phi)*ti.sin(theta)
        z=ti.cos(theta)
        return(x*i_hat+y*k_hat+z*j_hat)
    
    @ti.func
    def get_reflect_info(self,j_hat,ray_dir):#反射
        i_hat=ti.Vector([-2*j_hat[1]*j_hat[2],j_hat[0]*j_hat[2],j_hat[1]*j_hat[0]]).normalized()
        k_hat=ti.math.cross(i_hat,j_hat).normalized()
        A=ti.Matrix.zero(ti.f32,3,3)
        list=[i_hat,k_hat,j_hat]#注意还有(0,0,1)
        for i in ti.static(range(3)):
            for j in ti.static(range(3)):
                A[i,j]+=list[j][i]
        ans= ti.solve(A,ray_dir)
        return (ans[0]*i_hat+ans[1]*k_hat-ans[2]*j_hat)#反射

    @ti.func
    def hit_cos(self,ray_dir,j_hat):#获取视线的颜色
        cos=ti.math.dot(ray_dir,j_hat)/(ray_dir.norm())
        return ti.abs(cos)#视角要乘上cos
    
    @ti.func
    def light_cos(self,light_dir,j_hat):#获取视线的颜色
        cos=ti.math.dot(light_dir,j_hat)/(light_dir.norm())
        return ti.abs(cos)#视角要乘上cos

@ti.func
def build_sence():
    Hierarchy=[]
    temp_d1=(canvas_width-light_width)/4
    temp_d2=(wall_distance-light_width)/4
    #light cource
    Hierarchy.append(rect(light_pos,DOWN,light_width,light_width,RIGHT,ti.Vector([10.0, 10.0, 10.0]),True,0))
    #left wall
    Hierarchy.append(rect(ti.Vector([0.,canvas_height/2,wall_distance/2]),RIGHT,wall_distance,canvas_height,FRONT,ti.Vector([0.0, 0.6, 0.0]),False,0))
    #right wall,
    Hierarchy.append(rect(ti.Vector([canvas_width,canvas_height/2,wall_distance/2]),LEFT,wall_distance,canvas_height,FRONT,ti.Vector([0.6, 0.0, 0.0]),False,0))          
    #ceil
    Hierarchy.append(rect(ti.Vector([temp_d1,canvas_height,wall_distance/2]),DOWN,2*temp_d1,wall_distance,RIGHT,ti.Vector([0.8, 0.8, 0.8]),False,0)) 
    Hierarchy.append(rect(ti.Vector([canvas_width/2,canvas_height,temp_d2]),DOWN,light_width,2*temp_d2,RIGHT,ti.Vector([0.8, 0.8, 0.8]),False,0))          
    Hierarchy.append(rect(ti.Vector([canvas_width-temp_d1,canvas_height,wall_distance/2]),DOWN,2*temp_d1,wall_distance,RIGHT,ti.Vector([0.8, 0.8, 0.8]),False,0)) 
    Hierarchy.append(rect(ti.Vector([canvas_width/2,canvas_height,wall_distance-temp_d2]),DOWN,light_width,2*temp_d2,RIGHT,ti.Vector([0.8, 0.8, 0.8]),False,0))                  

    #ground
    Hierarchy.append(rect(ti.Vector([canvas_width/2,0,wall_distance/2]),UP,canvas_width,wall_distance,RIGHT,ti.Vector([0.8, 0.8, 0.8]),False,0))
    #back wall
    Hierarchy.append(rect(ti.Vector([canvas_width/2,canvas_height/2,wall_distance]),FRONT,canvas_width,canvas_height,RIGHT,ti.Vector([0.8, 0.8, 0.8]),False,1))
    
    Hierarchy.append(Sphere(ti.Vector([u,u/2,0.8*u]),u/2,ti.Vector([0.6, 0.8, 0.8]),False,1))
    Hierarchy.append(Sphere(ti.Vector([2*u,0.4*u,u]),0.4*u,ti.Vector([0.8, 0.6, 0.2]),False,0))
    Hierarchy.append(Sphere(ti.Vector([1.5*u,0.2*u,0.5*u]),0.2*u,ti.Vector([0.4, 0.6, 0.4]),False,2))
    
    return Hierarchy
    

@ti.kernel
def render():
    hierarchy=build_sence()
    for i,j in canvas:  
        for c in range(sample_per_pixel):#多次采样
            color=ti.Vector([0.,0.,0.])
            hit_times=0
            start_pos=camera_pos
            ray_dir=ti.Vector([i+ti.random(),j+ti.random(),0.])-start_pos
            hit_light=False
            # cos=1.
            light_factor=0.9
            while(hit_times<=max_depth and not hit_light):
                
                if(ti.random()>p_RR):
                    break
                else:
                    hit_times+=1
                    t_min=INF
                    index=len(hierarchy)
                    j_hat=ti.Vector([0.,0.,0.])
                    hit_pos=ti.Vector([0.,0.,0.])
                    for k in ti.static(range(len(hierarchy))):#对所有物体求交
                        ans=hierarchy[k].get_hit_info(start_pos,ray_dir)
                        if(ans[0]<t_min):
                            j_hat=ans[2]
                            t_min=ans[0]
                            hit_pos=ans[1]
                            index=k
                            hit_light=hierarchy[k].is_light
                    is_block=False
                    light_dir=light_pos-hit_pos 
                    for k in ti.static(range(1,len(hierarchy))):#对所有物体求交(跳过灯光)
                        ans=hierarchy[k].get_hit_info(hit_pos,light_dir)
                        if(ans[0]<INF):
                            is_block=True
                    if(index!=len(hierarchy)):#击中了
                        for k in ti.static(range(len(hierarchy))):
                            if(k==index):#小技巧来得到击中物体的索引
                                
                                if(not hierarchy[k].is_light and not is_block):
                                    light_factor+=-(light_factor-light_factor**2)
                                    light_cos=hierarchy[k].light_cos(light_dir,j_hat)
                                    color+=hierarchy[k].color*hierarchy[k].hit_cos(ray_dir,j_hat)*light_factor
                                elif(hierarchy[k].is_light):
                                    # light_factor=1
                                    color+=hierarchy[k].color*hierarchy[k].hit_cos(ray_dir,j_hat)
                                else:
                                    color+=hierarchy[k].color*light_factor*0.5*hierarchy[k].hit_cos(ray_dir,j_hat)
                                if(hierarchy[k].material==2):#都有
                                    if(ti.random()>proportion):
                                        ray_dir=hierarchy[k].get_diffuse_info(j_hat)
                                    else:
                                        ray_dir=hierarchy[k].get_reflect_info(j_hat,ray_dir)    
                                
                                elif(hierarchy[k].material==1):#镜面
                                    ray_dir=hierarchy[k].get_reflect_info(j_hat,ray_dir) 
                                    
                                else:
                                    ray_dir=hierarchy[k].get_diffuse_info(j_hat)
                    else:
                        color=ti.Vector([0.,0.,0.])
                        break#虚空
                    start_pos=hit_pos
            if(not hit_light):
                canvas[i,j]+=color/(sample_per_pixel*p_RR)#抗锯齿
                # canvas[i,j]+=ti.Vector([0.,0.,0.])
            else:
                canvas[i,j]+=color/(sample_per_pixel*p_RR)#抗锯齿
                    
    
gui = ti.GUI("Ray Tracing", res=(canvas_width, canvas_height))
canvas.fill(0)

# 细化

cnt = 0
while gui.running:
    cnt += 1
    render()
    gui.set_image(np.sqrt(canvas.to_numpy() / cnt))#平滑化
    gui.show()

#一次渲染

# render()
# while gui.running:
#     gui.set_image(canvas.to_numpy())
#     gui.show()