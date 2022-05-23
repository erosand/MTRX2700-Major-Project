import serial
import struct
import traceback
import matplotlib.pyplot as plt
import numpy as np

MSG_SIZE = 14



def readSerial(serialPort):   
    if serialPort.in_waiting:
        try:
            data = readPacket(serialPort)

            return data

            if isinstance(data,list): # If the packet was a point  message
                return data
            elif data: # If the packet was a text or gyro message nothing needs to be returned
                return False
            else:
                print("Error, data = ", data)
                return False
        except Exception as e:
            print(traceback.format_exc())
            # Logs the error appropriately.     
                  
def readPacket(serialPort):
    in_bytes = serialPort.read(1)
    return in_bytes

    # if len(header_bytes) < MSG_HEADER_SIZE:
    #     # must be out of messages
    #     print("Error: Header is ", len(header_bytes), " bytes")
    #     return False
 
    # header_data = struct.unpack(">H8sHH", header_bytes)
    # #print("\nHeader sentinels: " + str(hex(header_data[0])) + ", " + str(hex(header_data[3])))

    # message_type = header_data[1].split(b'\0', 1)[0]  # Remove the null characters from the string
    # # print("Message type: " + str(message_type))
    # # print("Message size: " + str(header_data[2]))

    # if message_type == b"text":
    #     text_bytes = serialPort.read(header_data[2])
    #     #print("Text message: " + str(text_bytes.decode("utf-8")))
    #     return True
    # elif message_type == b"point":
    #     point_bytes = serialPort.read(header_data[2])
    #     point_data = struct.unpack(">HhhIH", point_bytes)
    #     #print("Point message: " + str(point_data[1:4]))
    #     return list(point_data[1:4])
    # else: 
    #     print("Error: Invalid message type: ", message_type,"\n\n")
    #     return False

def sendByte(sp,b):
    sp.write(b)

def randomPoints(n = 200, az_lim = 45, el_lim = 45, dist_lim = [2000, 10000]):
    az = np.random.uniform(low=-az_lim,high=az_lim,size=n)
    el = np.random.uniform(low=-el_lim,high=el_lim,size=n)
    dist = np.random.uniform(low=dist_lim[0],high=dist_lim[1],size=n)
    points = [[az[i],el[i],dist[i]] for i in range(0,len(az))]
    return points

def sphe2cart(data,sensor_pos=[0,0,0]):
    # x = data[2]/1000*np.sin(np.radians(data[0])) + sensor_pos[0] # Side view
    # y = data[2]/1000*np.cos(np.radians(data[0])) + sensor_pos[1]
    # z = data[2]/1000*np.sin(np.radians(data[1])) + sensor_pos[2]
    x = data[2]/1000*np.sin(np.radians(data[0])) + sensor_pos[0] # Top view
    y = data[2]/1000*np.sin(np.radians(data[1])) + sensor_pos[1]
    z = sensor_pos[2] - data[2]/1000*np.cos(np.radians(data[0]))
    return [x,y,z]

def figSetup(fig,params):
    [sensor_pos, win_x, win_y, win_z] = params
    ax = fig.add_subplot(111,projection='3d')    
    plt.show(block=False) # Lets the remaining code keep running
    ax.legend()
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title('Point cloud')
    ax.set(xlim=(sensor_pos[0]-win_x/2, sensor_pos[0]+win_x/2), xticks=np.arange(sensor_pos[0]-win_x/2, sensor_pos[0]+win_x/2+1),
            ylim=(sensor_pos[1]-win_y/2, sensor_pos[1]+win_y/2), yticks=np.arange(sensor_pos[1]-win_y/2, sensor_pos[1]+win_y/2+1),
            zlim=(0, sensor_pos[2]), zticks=np.arange(0, sensor_pos[2]+1))
    return ax

if __name__ == '__main__':
    # sp1 = serial.Serial(port="COM1", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE) # For sending (testing)
    sp2 = serial.Serial(port="COM10", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE) # For receiving
    
    win_x = 10
    win_y = 10
    win_z = 10
    sensor_pos = [win_x/2, win_y/2, win_z]
    ax = figSetup(plt.figure(), [sensor_pos, win_x, win_y, win_z]) # Setup figure and plot sensor position
    ax.scatter(sensor_pos[0],sensor_pos[1],sensor_pos[2],c='r',marker='s',label='LIDAR')

    n_points = 100
    #r_data = randomPoints(n_points, 45, 45, [2000,10000]) # Generate simulated points from the Lidar   
    data_vec = []
    data = 0
    points = []
    p_count = 0
    plt.pause(1) # Needed for contiuous updates of the plot ("animation")

    testdata = b'Point,111,11,12345\nPoint,22,222,12345\n'
    
    in_bytes = b''

    while p_count < n_points:
        # a = testdata[i].to_bytes(1,'big')
        # sp1.write(a)

        if sp2.in_waiting:
            in_bytes = in_bytes + sp2.read(1)
            if in_bytes[-1].to_bytes(1,'big') == b'\n':
                byte_msg = in_bytes
                in_bytes = b''
                datalist = byte_msg.decode('utf-8').strip('\n').split(',')[1:]
                data = [int(el) for el in datalist]
                print(data)

        if data:
            data_vec.append(data)
            [x,y,z] = sphe2cart(data,sensor_pos) # Convert from spherical coordinates to cartesian
            points.append([x,y,z])
            data = 0

            z_n = (sensor_pos[2] - z - 1.4)/(sensor_pos[2] - 1.4) # Normalise y (depth) to [0,1]
            col = [0.5*z_n, 1-z_n, z_n] # Calculate RGB color based on normalised y-value 
            ax.scatter(x,y,z,s=2,depthshade=False,label='Points',color=col)
            ax.legend(['Lidar','Points'])
            ax.set_title('Point cloud, ' + str(p_count+1) + ' points')
            plt.pause(0.1) # Needed for contiuous updates of the plot ("animation")

            p_count = p_count + 1
        print(p_count)

    plt.show(block=True) # Prevents the figure from closing when the program is finished
    