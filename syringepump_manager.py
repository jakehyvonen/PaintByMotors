import serial
import serial_connection as sc

ser = serial.Serial()
ser.port = None
ser.baudrate = 19200
ser.timeout = 1
ser.write_timeout = 1

class SyringePumpManager:
    def __init__(self):
            self.connection_status_label = 'not connected'        
        
    def connect_to_controller(self, ports=sc.serial_ports()):
        global ser
        if ser.is_open:
            print('already connected')
        else:
            print('attempting to connect...')
            s = sc.ping_controller(ports, 19200, b'VOL\r','00S0.000ML',11,b'\x03')        
            if s == -1:
                return -1
            else:
                ser.port = s
                ser.open()               
                return s

    def SendCommand(self, com, getResponse = False):     
        if ser.is_open:
            print('sending command: ' + com)            
            if('echo' in com or 'get' in com):
                getResponse = True
            command = str(com)+"\r"
            ser.write(command.encode())
            if getResponse:
                response = ser.read_until(b'\x03').decode().rstrip()
                print('response: ' + response)
        else:
            print('Serial closed. Attempting to open')
            try:
                ser.open()
            except:
                print('oh heavens, there is a connection problem')
                pass

if __name__ == '__main__':
    manager = SyringePumpManager()
    manager.connect_to_controller(sc.serial_ports())
    while True:
        var = input("Please enter a command: ")
        print("entered: "+str(var))
        manager.SendCommand(str(var),True)