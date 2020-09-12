import serial
import serial_connection as sc
import enum

ser = serial.Serial()
ser.port = None
ser.baudrate = 19200
ser.timeout = 1
ser.write_timeout = 1
'''
Note: if pump addresses are somehow reset, this will fuck up
--> addresses need to be set individually via serial_connection.py 
'''
class SyringePumpManager:
    def __init__(self):
            self.connection_status_label = 'not connected'        
        
    def connect_to_controller(self, ports=sc.serial_ports()):
        global ser
        if ser.is_open:
            print('already connected')
        else:
            print('attempting to connect...')
            s = sc.ping_controller(ports, 19200, b'00DIA\r','00S26.59',11,b'\x03')        
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

class RateUnits (enum.Enum):
    UM = 1 #uL/min
    MM = 2 #mL/Min
    UH = 3 #uL/hr
    MH = 4 #mL/hr

class SyringePump:
    def __init__(self, address = 00, volume = 60.0, rate = 11.0, units = RateUnits.MM):
            self.address = address
            self.volume = volume
            self.rate = rate
            self.units = units

if __name__ == '__main__':
    manager = SyringePumpManager()
    manager.connect_to_controller(sc.serial_ports())
    while True:
        var = input("Please enter a command: ")
        print("entered: "+str(var))
        manager.SendCommand(str(var),True)