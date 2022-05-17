import matplotlib.pyplot as plt
import matplotlib as mpl
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

def spiral(n_points,r_max):
       ang = np.linspace(0,8*np.pi,n_points)
       r = np.linspace(0,r_max,n_points)
       x = [r[i]*a for i,a in enumerate(np.sin(ang))]
       y = np.linspace(1,r_max/0.8*2,n_points)
       z = [r[i]*a for i,a in enumerate(np.cos(ang))]
       return [x,y,z]


if __name__ == '__main__':
       cl_width = 10
       cl_depth = 10
       cl_height = 10
       sensor_pos = [0, 0, 0]
       
       # Simulate Lidar data
       az_lim = 45
       el_lim = 45
       dist_lim = 10*1000
       n = 200
       az = np.random.uniform(low=-az_lim,high=az_lim,size=n)
       el = np.random.uniform(low=-el_lim,high=el_lim,size=n)
       dist = np.random.uniform(low=2000,high=dist_lim,size=n)
       points = [[az[i],el[i],dist[i]] for i in range(0,len(az))]
       #points = [[-15, 30, 7435],[10, -20, 5463],[10, -5, 2586]]

       x = [p[2]/1000*np.sin(np.radians(p[0])) + sensor_pos[0] for p in points] 
       y = [p[2]/1000*np.cos(np.radians(p[0])) + sensor_pos[1] for p in points]
       z = [p[2]/1000*np.sin(np.radians(p[1])) + sensor_pos[2] for p in points]
       
       # Plot spiral
       xyz = spiral(n, 0.8*min(cl_height,cl_width)/2)
       for i,vec in enumerate(xyz):
              xyz[i] = [p + sensor_pos[i] for p in vec] 
       [x,y,z] = xyz


       fig = plt.figure()
       ax = fig.add_subplot(111,projection='3d')    

       ax.scatter(sensor_pos[0],sensor_pos[1],sensor_pos[2],c='r',marker='s',label='LIDAR')
       ax.scatter(x,y,z,c=y,s=4,depthshade=False,label='Points')
       ax.legend()
       ax.set_xlabel('Width (x)')
       ax.set_ylabel('Depth (y)')
       ax.set_zlabel('Height (z)')
       ax.set_title('Point cloud')
       ax.set(xlim=(-cl_width/2+sensor_pos[0], cl_width/2+sensor_pos[0]), xticks=np.arange(-cl_width/2+sensor_pos[0], cl_width/2+1+sensor_pos[0]),
              ylim=(sensor_pos[1], cl_depth+sensor_pos[1]), yticks=np.arange(sensor_pos[1], cl_depth+sensor_pos[1]+1),
              zlim=(-cl_height/2+sensor_pos[2], cl_height/2+sensor_pos[2]), zticks=np.arange(-cl_height/2+sensor_pos[2], cl_height/2+1+sensor_pos[2]))

       
       plt.show()
