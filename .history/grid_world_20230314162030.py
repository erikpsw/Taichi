import taichi as ti
import numpy as np

ti.init(ti.cuda)
pixel_size=40
grid_width=2
grid_height=2
width=pixel_size*grid_width
height=pixel_size*grid_height
step=1/grid_width
gamma=0.9

#网格图类
class grid:
    def __init__(self,width,height) -> None:
        self.canvas=np.ones((width,height,3))

    def set_color(self,x,y,color):
        self.canvas[x*pixel_size:(x+1)*pixel_size,y*pixel_size:(y+1)*pixel_size,:]=color

#智能体
class agent:
    def __init__(self,x,y) -> None:
        self.pos=[(x+0.5)/grid_width,(y+0.5)/grid_height]

    def move(self,dir):
        if(dir==0):#上
            self.pos[1]+=step
        elif(dir==1):#右
            self.pos[0]+=step  
        elif(dir==2):#下
            self.pos[1]-=step
        elif(dir==3):#左
            self.pos[0]-=step
        elif(dir==4):
            pass
class state:
    def __init__(self,x,y) -> None:
        self.x=x
        self.y=y
        self.reward=[0,0,0,0,0]
        self.kind=0#1为目标，2为障碍
        self.value=0
        self.policy=0
    
    def __repr__(self):
        return f"[{self.x},{self.y},reward{self.reward}]"
    
def init_reward(x,y):
    state=state_list[x][y].kind
    if(state==1):
        return 1
    elif(state==2):
        return -1
    else:
        return 0
    
def next_state(x,y,dir):
    if(dir==4):
        return x,y
    elif(dir==0):
        if(y+1==grid_height):
            return x,y
        else:
            return x,y+1
    #右
    elif(dir==1):
        return (x,y) if x+1==grid_width else (x+1,y)
    
    #下
    elif(dir==2):
        return (x,y) if y==0 else (x,y-1)

    #左
    elif(dir==3):
        return (x,y) if x==0 else (x-1,y)
    

state_list=[]
for i in range(grid_width):
    tmp=[]
    for j in range(grid_height):
        tmp.append(state(i,j))
    state_list.append(tmp)
state_list[1][0].kind=1
state_list[1][1].kind=2

#初始化奖励
v_list=[]
for i in range(grid_width):
    tmp=[]
    for j in range(grid_height):
        obj=state_list[i][j]
        x=obj.x
        y=obj.y
        tmp.append(obj.value)
        #上
        if(y+1==grid_height):
            obj.reward[0]=-1
        else:
            obj.reward[0]=init_reward(x,y+1)
        #右
        if(x+1==grid_width):
            obj.reward[1]=-1
        else:
            obj.reward[1]=init_reward(x+1,y)
        #下
        if(y==0):
            obj.reward[2]=-1
        else:
            obj.reward[2]=init_reward(x,y-1)
        #左
        if(x==0):
            obj.reward[3]=-1
        else:
            obj.reward[3]=init_reward(x-1,y)
        #stay
        obj.reward[4]=init_reward(x,y)
    v_list.append(tmp)
#value iteration
for i in range(grid_width):
    for j in range(grid_height):
        q_list=[]
        obj=state_list[i][j]
        for k in range(5):
            nx,ny=next_state(i,j,k)
            q=obj.reward[k]+gamma*v_list[nx][ny]
            q_list.append(q)
        dir = q_list.index(max(q_list))
        obj.policy=dir
        obj.value=max(q_list)
        v_list[i][j]=obj.value
print(v_list)

line_b=np.array([[x,0] for x in range(pixel_size,width,pixel_size)])/width
line_b1=np.array([[0,y] for y in range(pixel_size,height,pixel_size)])/height
line_e=np.array([[x,width-1] for x in range(pixel_size,width,pixel_size)])/width
line_e1=np.array([[height-1,y] for y in range(pixel_size,height,pixel_size)])/height
grid_world=grid(width,height)
grid_world.set_color(3,2,[0.8,0.9,0.7])
myagent=agent(2,2)


dt=1
N=0

# gui=ti.GUI("grid",(width,height))
# while gui.running:
#     N+=1
#     if(N==dt*60):
#         N=0
#         myagent.move(2)
#     gui.set_image(grid_world.canvas)
#     gui.lines(begin=np.concatenate((line_b,line_b1),axis=0), end=np.concatenate((line_e,line_e1),axis=0), radius=1, color=0x000000)
#     gui.circle(myagent.pos,color=0x000000,radius=5)
#     gui.show()