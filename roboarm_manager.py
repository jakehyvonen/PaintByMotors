import serial
import serial_connection as sc

ser = serial.Serial()
ser.port = None
ser.baudrate = 9600
ser.timeout = 1
ser.write_timeout = 1

class RoboArmManager:
    def __init__(self):
        self.connection_status_label = 'not connected'        
    
    def connect_to_controller(self):
        global ser
        if ser.is_open:
            print('already connected')
        else:
            print('attempting to connect...')
            s = sc.ping_controller(sc.serial_ports(), 9600, b'ping','pong',11)        
            if s == -1:
                return -1
            else:
                ser.port = s
                ser.open()
                ser.readlines()

    def SendCommand(self, com):     
        if ser.is_open:
            print('sending command: ' + com)
            command = str(com)+"\n"
            ser.write(command.encode())
        else:
            print('serial not open')


if __name__ == '__main__':
    manager = RoboArmManager()
    manager.connect_to_controller()
    manager.SendCommand('servo90909090')
    while True:
        var = input("Please enter a command:")
        print("entered: "+str(var))
        manager.SendCommand(str(var))