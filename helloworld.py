import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)
b=ti.Vector(3,dt=ti.f32,shape=4)#4个3d的张量
# b[3]=[1,2,3]是错误的，创建后就不可以更改
a = ti.Matrix([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
c=ti.Matrix(2,2,dt=ti.f64,shape=(3,5))#3x5个2x2的矩阵
loss=ti.var(dt=ti.f32,shape=())
loss[None]=3
print(loss[None])
print(a)
@ti.kernel#装饰器函数，用于声明函数
def hello(i: ti.f64):
    a=40
    print('hello world',a+2)#void函数
hello(2)
@ti.kernel
def calc() -> ti.f32:#定义返回值的数据类型
    s=0
    for i in range(20):
        s+=i
    return s
print(calc())
