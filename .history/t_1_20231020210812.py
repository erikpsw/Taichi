import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

G=6.6743*10**(-11)
m=1.5*1.989*10**30
r_0=10**7
c=3*10**8

v_0=np.sqrt(G*m/r_0/4)
#print(v_0)

#初始量
x_0=r_0
y_0=0

def runge_kutta(y,h,f):
    k1 = h * f(t,x,v_x,y,v_y)
    k2 = h * f(t + 0.5 * h, x + 0.5 * k1, v_x + 0.5 * k1,y + 0.5 * k1, v_y + 0.5 * k1)
    k3 = h * f(t + 0.5 * h, x + 0.5 * k2, v_x + 0.5 * k2,y + 0.5 * k2, v_y + 0.5 * k2)
    k4 = h * f(t + h, x + k3, v_x + k3,y + k3,v_y + k3)
    return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6

def Fun_1(t,x,v_x,y,v_y):
    return A*v_x-x/r*a*dt

def Fun_2(t,x,v_x,y,v_y):
    return A*v_x-x/r*a*dt

def Fun_3(t,x,v_x,y,v_y):
    return A*v_y-y/r*a*dt

def Fun_4(t,x,v_x,y,v_y):
    return A*v_y-y/r*a*dt
x =x_0
y =y_0
v_x =0
v_y =v_0
r=r_0
X=[x_0]
Y=[y_0]
R=[r_0]
V_x=[0]
V_y=[v_0]

dt=0.001
t=0
while R[-1]>=1000:
    r = np.sqrt(x ** 2 + y ** 2)
    a=G*m/r/r/4
    print(r)

    E_v=(V_x[-1]**2+V_y[-1]**2)*m/2
    #print(E_v)
    dE=32*G**4*m**4*2*m*dt/5/r**5/c**5
    #print(dE)
    dE_d=-G*m*m/R[-1]+G*m*m/r
    #print(dE_d)
    E_vn=E_v
    #print(E_vn)
    A=np.sqrt(E_vn/E_v)
    #print(x)

    x=runge_kutta(x,dt,Fun_1)
    v_x=A*v_x-x/r*a*dt
    y=runge_kutta(y,dt,Fun_3)
    v_y=A*v_y-y/r*a*dt

    t=t+dt
    X.append(x)
    Y.append(y)
    V_x.append(v_x)
    V_y.append(v_y)
    R.append(r)
print(t)
plt.plot(X,Y)
plt.show()