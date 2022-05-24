import serial
import matplotlib.pyplot as plt
import numpy as np


def sendByte(serialport,testdata,i):
    serialport.write(testdata[i].to_bytes(1,'big'))

def ang2cord(data,sensor_pos=[0,0,0]): # Convert from angles and distance to cartesian coordinates
    [az,el,d] = data
    d = d/1000 # Convert to meters
    x = d*np.sin(np.radians(az)) + sensor_pos[0] # Top view
    y = d*np.sin(np.radians(el)) + sensor_pos[1]
    z = sensor_pos[2] - np.sqrt(d**2 - x**2 - y**2)
    return [x,y,z]

def figSetup():
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')    
    plt.show(block=False) # Lets the remaining code keep running
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title('Point cloud')
    return ax

if __name__ == '__main__':
    print(type(serial.Serial()))
    # sp1 = serial.Serial(port="COM1", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE) # For sending (testing)
    sp2 = serial.Serial(port="COM2", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE) # For receiving
    
    sensor_pos = [0, 0, 10] # Sensor position
    n_points = 1000 # Number of points
    [d_min, d_max] = [0.4, 1] # Points outside of this range are regarded as outliers and get discarded
    [z_min, z_max] = [sensor_pos[2]-d_max, sensor_pos[2]-d_min]
    testdata = b'Point,111,11,12345\nPoint,22,222,6789\n'
    data = 0
    data_vec = []
    points = []
    X = []
    Y = []
    Z = []
    p_count = 0
    buffer = b''
    
    print("Scanning in range ", [d_min,d_max])
    while p_count < n_points:
        #sendByte(sp1,testdata,p_count) # For simulating input through serial
        
        if sp2.in_waiting: # If any bytes are available
            buffer = buffer + sp2.read(1) # Read one byte at a time
            if buffer[-1].to_bytes(1,'big') == b'\n': # If a complete message has been received
                byte_msg = buffer
                buffer = b''
                msg = byte_msg.decode('utf-8').strip('\n').split(',') # Decode byte message
                if msg[0] == 'Point': # If message is a point
                    data = [int(element) for element in msg[1:]] # Extract desired data from message
                    #print("Data: ",data)
                    [x,y,z] = ang2cord(data,sensor_pos) # Convert from angles and distance to cartesian coordinates
                    if z < z_max and z > z_min: # Discard outliers
                        p_count = p_count + 1
                        #print("Point #",p_count," is (",round(x,2),round(y,2),round(z,2),")")
                        data_vec.append(data)
                        points.append([x,y,z])
                        X.append(x)
                        Y.append(y)
                        Z.append(z)
                        data = 0    
                        if p_count % 100 == 0:
                            print(p_count, " out of ", n_points)
                    else: 
                        print("Outlier: ",round(x,2),round(y,2),round(z,2))
                else:
                    print("Error message: ",msg[0])

    print("Done")
    
    ax = figSetup() # Setup figure
    ax.scatter(sensor_pos[0],sensor_pos[1],sensor_pos[2],c='r',marker='s',label='LIDAR') # Plot Lidar position
    ax.scatter(X,Y,Z,s=0.5,depthshade=False,label='Points',c=Z)
    ax.legend(['Lidar','Points'])
    ax.set_title('Point cloud, ' + str(p_count) + ' points')
    ax.legend()
    plt.show(block=True) # Prevents the figure from closing when the program is finished       
    