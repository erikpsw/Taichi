import taichi as ti 

ti.init(arch=ti.gpu)


#浮点精度决定了分辨率
n =720
fix_point=ti.Vector([-1.7488370268237048, 2.83016863723636e-06],ti.f64)
canvas = ti.Vector.field(3, dtype=ti.f64, shape=(n,n))

@ti.func
def complex_sqr(z):
    return ti.Vector([z[0]**2 - z[1]**2, z[1] * z[0] * 2])#复数的平方

@ti.kernel
def paint(lamb:float):
    for i, j in canvas: 
        c = ti.Vector([(i / n -0.5)*lamb+fix_point[0], (j / n -0.5)*lamb+fix_point[1]])#范围从-2到2
        z = ti.Vector([(i / n -0.5)*lamb+fix_point[0], (j / n -0.5)*lamb+fix_point[1]])
        iterations = 0
        while z.norm() <6 and iterations < 128:#迭代深度
            z = complex_sqr(z) + c
            iterations += 1
        canvas[i, j] = ti.Vector([iterations*2 ,255,255])/255
        

gui = ti.GUI("Mandelbrot Set", res=(n , n),fast_gui=True)#使gpu用快速渲染

i=1
while gui.running:
    paint(i)
    gui.set_image(canvas)
    gui.show()
    i/=1.02

