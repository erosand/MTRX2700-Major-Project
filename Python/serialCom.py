import serial
import struct
import traceback
import matplotlib.pyplot as plt
import numpy as np

MSG_HEADER_SIZE = 16

#TODO: Add colorbar on the side

def readSerial(serialPort):   
    # Wait until there is data waiting in the serial buffer
    if serialPort.in_waiting > 0:
        try:
            data = readPacket(serialPort)
            if data:
                return list(data)
            else:
                print("Error, data = ", data)
                return False
        except Exception as e:
            print(traceback.format_exc())
            # Logs the error appropriately.     
                  
def readPacket(serialPort):
    header_bytes = serialPort.read(MSG_HEADER_SIZE)

    if len(header_bytes) < MSG_HEADER_SIZE:
        # must be out of messages
        print("Here 1")
        return False
 
    header_data = struct.unpack(">H8sHHH", header_bytes)
    print("Header sentinels: " + str(hex(header_data[0])) + ", " + str(hex(header_data[4])))

    message_type = header_data[1].split(b'\0', 1)[0]  # remove the null characters from the string
    print(message_type)
    print("Message type: " + message_type.decode("utf-8"))
    print("Message size: " + str(header_data[2]))

    if message_type == b"text":
        text_bytes = serialPort.read(header_data[2])
        print("Text message: " + str(text_bytes.decode("utf-8")))
    elif message_type == b"gyro":
        gyro_bytes = serialPort.read(header_data[2])
        gyro_data = struct.unpack(">hhhhH", gyro_bytes)
        print("Gyro message: " + str(gyro_data[1]) + ", " + str(gyro_data[2]) + ", " + str(gyro_data[3]) + ", time=" + str(gyro_data[4]))
    elif message_type == b"point":
        point_bytes = serialPort.read(header_data[2])
        point_data = struct.unpack(">iiiIi", point_bytes)
        print("Point message: " + str(point_data[1:4]))
        return point_data[1:4]
    else: print("Here 2", message_type,"\n\n")
    return False

def sendPoint(sp,point):
    point = [int(p) for p in point]
    msg_point = struct.pack(">iiiIi", 0xAA, point[0], point[1], point[2], 0xBB)
    header_point = struct.pack(">H8sHHH", 0xABCD, b"point", len(msg_point), 0, 0xDCBA)
    sp.write(header_point)
    sp.write(msg_point)

def randomPoints(n = 200, az_lim = 45, el_lim = 45, dist_lim = [2000, 10000]):
    az = np.random.uniform(low=-az_lim,high=az_lim,size=n)
    el = np.random.uniform(low=-el_lim,high=el_lim,size=n)
    dist = np.random.uniform(low=dist_lim[0],high=dist_lim[1],size=n)
    points = [[az[i],el[i],dist[i]] for i in range(0,len(az))]
    return points

def sphe2cart(data,sensor_pos=[0,0,0]):
    x = data[2]/1000*np.sin(np.radians(data[0])) + sensor_pos[0]
    y = data[2]/1000*np.cos(np.radians(data[0])) + sensor_pos[1]
    z = data[2]/1000*np.sin(np.radians(data[1])) + sensor_pos[2]
    return [x,y,z]

def figSetup(fig,params):
    [sensor_pos, cl_width, cl_depth, cl_height] = params
    ax = fig.add_subplot(111,projection='3d')    
    plt.show(block=False) # Lets the remaining code keep running
    ax.legend()
    ax.set_xlabel('Width (x)')
    ax.set_ylabel('Depth (y)')
    ax.set_zlabel('Height (z)')
    ax.set_title('Point cloud')
    ax.set(xlim=(-cl_width/2+sensor_pos[0], cl_width/2+sensor_pos[0]), xticks=np.arange(-cl_width/2+sensor_pos[0], cl_width/2+1+sensor_pos[0]),
            ylim=(sensor_pos[1], cl_depth+sensor_pos[1]), yticks=np.arange(sensor_pos[1], cl_depth+sensor_pos[1]+1),
            zlim=(-cl_height/2+sensor_pos[2], cl_height/2+sensor_pos[2]), zticks=np.arange(-cl_height/2+sensor_pos[2], cl_height/2+1+sensor_pos[2]))
    return ax

if __name__ == '__main__':
    sp1 = serial.Serial(port="COM1", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE) # For sending (testing)
    sp2 = serial.Serial(port="COM10", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE) # For receiving
    
    sensor_pos = [0, 0, 0]
    cl_width = 10
    cl_depth = 10
    cl_height = 10
    ax = figSetup(plt.figure(), [sensor_pos, cl_width, cl_depth, cl_height]) # Setup figure and plot sensor position
    ax.scatter(sensor_pos[0],sensor_pos[1],sensor_pos[2],c='r',marker='s',label='LIDAR')

    r_data = randomPoints(200, 45, 45, [2000,10000]) # Generate simulated points from the Lidar   
    data_vec = []
    points = []
    plt.pause(1) # Needed for contiuous updates of the plot ("animation")
    while True:
       # sendPoint(sp1,r_data[i]) # Simulates data being sent from Lidar
        
        data = readSerial(sp2) 
        if data:
            data_vec.append(data)

            [x,y,z] = sphe2cart(data,sensor_pos) # Convert from spherical coordinates to cartesian
            points.append([x,y,z])

            y_n = (y-1.4)/(cl_depth-1.4) # Normalise y (depth) to [0,1]
            print(y,y_n)
            col = [0.5*y_n, 1-y_n, y_n] # Calculate RGB color based on normalised y-value 
            ax.scatter(x,y,z,s=4,depthshade=False,label='Points',color=col)
            ax.legend(['Lidar','Points'])
            
            plt.pause(0.1) # Needed for contiuous updates of the plot ("animation")
    plt.show(block=True) # Prevents the figure from closing when the program is finished