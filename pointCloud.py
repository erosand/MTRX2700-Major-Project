from math import sin, cos, radians
from turtle import color
import matplotlib.pyplot as plt
import numpy as np

def testPlot():
       np.random.seed(3)
       x = 4 + np.random.normal(0, 2, 24)
       y = 4 + np.random.normal(0, 2, len(x))
       # size and color:
       sizes = np.random.uniform(15, 80, len(x))
       colors = np.random.uniform(15, 80, len(x))

       # plot
       fig, ax = plt.subplots()

       ax.scatter(x, y, s=sizes, c=colors, vmin=0, vmax=100)

       ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
              ylim=(0, 8), yticks=np.arange(1, 8))

       plt.show()




if __name__ == '__main__':
       cl_width = 10
       cl_depth = 10
       cl_height = 10
       sensor_pos = [0, 0, 0]

       points = [-15, 30, 7435]
       
       [az, el, d] = points
       n = 30
       ang = np.linspace(0,4*np.pi,n)
       r = np.linspace(0,min(cl_height,cl_width)/2,n)
       x = [r[i]*a for i,a in enumerate(np.sin(ang))]
       y = np.linspace(0,cl_depth,n)
       z = [r[i]*a for i,a in enumerate(np.cos(ang))]
       points = [x,y,z]
       for i,vec in enumerate([x,y,z]):
              points[i] = [p + sensor_pos[i] for p in vec]
       print(points)
       [x,y,z] = points
       # d = d/1000
       # x = d*sin(radians(az))
       # y = d*cos(radians(az))
       # z = d*sin(radians(el))
       # print(x,y,z)

       fig = plt.figure()
       ax = fig.add_subplot(111, projection='3d')
       ax.scatter(x,y,z,s=6)
       ax.scatter(sensor_pos[0],sensor_pos[1],sensor_pos[2],c='m')


       ax.set(xlim=(-cl_width/2+sensor_pos[0], cl_width/2+sensor_pos[0]), xticks=np.arange(-cl_width/2+sensor_pos[0], cl_width/2+1+sensor_pos[0]),
              ylim=(sensor_pos[1], cl_depth+sensor_pos[1]), yticks=np.arange(sensor_pos[1], cl_depth+sensor_pos[1]+1),
              zlim=(-cl_height/2+sensor_pos[2], cl_height/2+sensor_pos[2]), zticks=np.arange(-cl_height/2+sensor_pos[2], cl_height/2+1+sensor_pos[2]))

       plt.show()

