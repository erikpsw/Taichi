import numpy as np
import taichi as ti
import queue
ti.init(arch=ti.cpu)
g=9.8

class double_p:
    def __init__(self,m1,m2,l1,l2,theta1,theta2,thetad1,thetad2):
        self.m1,self.m2,self.l1,self.l2=m1,m2,l1,l2
        self.theta1=theta1
        self.theta2=theta2
        self.thetad1=thetad1
        self.thetad2=thetad2
        
    def update(self,dt):
        self.theta1+=self.thetad1*dt
        self.theta2+=self.thetad2*dt
        a=(self.m1+self.m2)*self.l1
        b=self.m2*self.l2*np.cos(self.theta1-self.theta2)
        c=-(self.m2*self.l2*np.sin(self.theta1-self.theta2)*(self.thetad2**2)+(self.m1+self.m2)*g*np.sin(self.theta1))
        d=self.l1*np.cos(self.theta1-self.theta2)
        e=self.l2
        f=self.l1*np.sin(self.theta1-self.theta2)*(self.thetad1)**2-g*self.theta2
        ans=np.linalg.solve([[a,b],[d,e]],[c,f])
        self.thetad1+=ans[0]*dt
        self.thetad2+=ans[1]*dt

        return (self.theta1,self.theta2)

m1,m2,l1,l2=1,1,.25,.125
theta1=np.pi/2
theta2=0
thetad1=0.5
thetad2=-0.2
p=double_p(m1,m2,l1,l2,theta1,theta2,thetad1,thetad2)
dt=0.005
window_width = 600
window_height = 600
gui = ti.GUI("double pendulum", res=(window_width, window_height))
q=queue.Queue()
q.put([0.5+l1*np.cos(p.theta1)+l2*np.cos(p.theta2),0.5-l1*np.sin(p.theta1)-l2*np.sin(p.theta2)])

while gui.running:
    p.update(dt)
    A=[0.5+l1*np.sin(p.theta1),0.5-l1*np.cos(p.theta1)]
    B=[0.5+l1*np.sin(p.theta1)+l2*np.sin(p.theta2),0.5-l1*np.cos(p.theta1)-l2*np.cos(p.theta2)]
    gui.lines(begin=np.array([[0.5,0.5],A]),end=np.array([A,B]),radius=2)
    q.put([0.5+l1*np.sin(p.theta1)+l2*np.sin(p.theta2),0.5-l1*np.cos(p.theta1)-l2*np.cos(p.theta2)])
    if(q.qsize()>=100):
        q.get()
    gui.lines(begin=np.array(q.queue)[:-1],end=np.array(q.queue)[1:],radius=2,color=0xf87064)
    gui.show()