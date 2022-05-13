import serial
import struct
import time
import traceback
  
MSG_HEADER_SIZE = 16


def readSerial(serialPort):   
    # Wait until there is data waiting in the serial buffer
    if serialPort.in_waiting > 0:
        try:
            if not readPacket(serialPort):
                pass
        except Exception as e:
            print(traceback.format_exc())
            # Logs the error appropriately.         

        
def readPacket(serialPort):
    header_bytes = serialPort.read(MSG_HEADER_SIZE)

    if len(header_bytes) < MSG_HEADER_SIZE:
        # must be out of messages
        return False
 
    header_data = struct.unpack(">H8sHHH", header_bytes)
    print("Header sentinels: " + str(hex(header_data[0])) + ", " + str(hex(header_data[4])))

    message_type = header_data[1].split(b'\0', 1)[0]  # remove the null characters from the string
    print("Message type: " + message_type.decode("utf-8"))
    print("Message size: " + str(header_data[2]))

    if message_type == b"text":
        text_bytes = serialPort.read(header_data[2])
        print("text message: " + str(text_bytes))
    elif message_type == b"gyro":
        gyro_bytes = serialPort.read(header_data[2])
        gyro_data = struct.unpack(">hhhhH", gyro_bytes)
        print("gyro message: " + str(gyro_data[1]) + ", " + str(gyro_data[2]) + ", " + str(gyro_data[3]) + ", time=" + str(gyro_data[4]))
    elif message_type == b"point":
        point_bytes = serialPort.read(header_data[2])
        point_data = struct.unpack(">iiiIi", point_bytes)
        print("Point message: " + str(point_data[1]) + ", " + str(point_data[2]) + ", " + str(point_data[3]))
    return True


if __name__ == '__main__':
    sp1 = serial.Serial(port="COM1", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    sp2 = serial.Serial(port="COM2", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    msg_point = struct.pack(">iiiIi", 0xAA, 15, 8, 2351, 0xBB)
    header_point = struct.pack(">H8sHHH", 0xABCD, b"point", len(msg_point), 0, 0xDCBA)
    
    for i in range(0,1):
        sp1.write(header_point)
        sp1.write(msg_point)

        readSerial(sp2)
        #time.sleep(0.1)