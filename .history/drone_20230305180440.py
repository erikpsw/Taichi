from socket import *
import taichi as ti
import numpy as np
ti.init(arch=ti.cuda)
import json

host, port = "127.0.0.1", 8888
width=1200
t=0
BUFF=1024#缓冲区大小

listener= socket(AF_INET, SOCK_STREAM)
listener.bind((host,port))
listener.listen(10)
sclient,addr=listener.accept()
print(f"{addr} connected")
sclient.settimeout(3.)

path=[]

while True:
    try:
        recieved=sclient.recv(BUFF)
        if(recieved):
            t+=1
            info=recieved.decode()
            pos=json.loads(info)
            if(t==1):
                path.append(np.array([pos["x"],pos["y"],pos["z"]]))
            else:
                path.append(np.array([pos["x"],pos["y"],pos["z"]]))
                path.append(np.array([pos["x"],pos["y"],pos["z"]]))
    except timeout as e:
        break
    
    except Exception as e:
        break
    
sclient.close()

window = ti.ui.Window("Rotation", (width, width))
canvas = window.get_canvas()
scene = ti.ui.Scene()
camera = ti.ui.Camera()
camera.position(2, 2, 2)
camera.lookat(-1,-1,-1)
pv_point=np.zeros((2,3),dtype=float)
line_points=ti.Vector.field(3,dtype=ti.f32,shape=len(path))
line_points.from_numpy(np.array(path))

while window.running:
    scene.lines(line_points, color = (0.28, 0.68, 0.99), width = 5.0)
    camera.track_user_inputs(window, movement_speed=0.01, hold_key=ti.ui.RMB)
    scene.set_camera(camera)
    canvas.scene(scene)
    window.show()