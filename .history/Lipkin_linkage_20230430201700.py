import taichi as ti
ti.init(arch=ti.gpu)
import numpy as np

theta=np.pi/4
lmax=15
R=4/lmax
a=8/lmax
b=3/lmax

window_width = 600
window_height = 600

beta=np.arccos(((2*R*np.cos(theta))**2+a**2-b**2)/(2*a*2*R*np.cos(theta)))
alpha=np.arccos((a**2-b**2-(2*R*np.cos(theta))**2)/(2*b*2*R*np.cos(theta)))

gui = ti.GUI("wave", res=(window_width, window_height))


B=[2*R*np.cos(theta)**2,2*R*np.cos(theta)*np.sin(theta)]
A=[0,0]
C=[B[0]+np.cos(alpha+theta)*b,B[1]+np.sin(alpha+theta)*b]
D=[B[0]+np.cos(theta-alpha)*b,B[1]+np.sin(theta-alpha)*b]
E=[B[0]+np.cos(theta)*b*2*np.cos(alpha),B[1]+np.sin(theta)*b*2*np.cos(alpha)]

r0=10
while gui.running:
    mouse_x, mouse_y = gui.get_cursor_pos()
    if (gui.get_event(ti.GUI.LMB) and ((mouse_x-B[0])**2+(mouse_y-B[1])**2)<=(r0/window_height)**2):
        is_move=1
    if (not gui.is_pressed(ti.GUI.LMB)):
        is_move=0
    if(is_move):
        if(mouse_x<2*R):
            ang=np.arccos((mouse_x-R)/R)
            B=[mouse_x,R*np.sin(ang)]
            theta=np.arctan(R*np.sin(ang)/mouse_x)
            if(a<(b+R*2*np.cos(theta))):
                beta=np.arccos(((2*R*np.cos(theta))**2+a**2-b**2)/(2*a*2*R*np.cos(theta)))
                alpha=np.arccos((a**2-b**2-(2*R*np.cos(theta))**2)/(2*b*2*R*np.cos(theta)))
                C=[B[0]+np.cos(alpha+theta)*b,B[1]+np.sin(alpha+theta)*b]
                D=[B[0]+np.cos(theta-alpha)*b,B[1]+np.sin(theta-alpha)*b]
                E=[B[0]+np.cos(theta)*b*2*np.cos(alpha),B[1]+np.sin(theta)*b*2*np.cos(alpha)]
    
    gui.clear()
    gui.circle(np.array([R,0]),radius=R*window_width,color=0x51acea)
    gui.circle(B,radius=r0)
    gui.lines(begin=np.array([A,C,A,D,C,D]),end=np.array([C,E,D,E,B,B]),radius=2)
    gui.show()
    