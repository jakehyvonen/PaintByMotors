import serial
import serial_connection as sc

ser = serial.Serial()
ser.port = None
ser.baudrate = 9600
ser.timeout = 1
ser.write_timeout = 1

m2 = '090'
m3 = '090'
m4 = '090'
m5 = '090'

class RoboArmManager:
    def __init__(self):
        self.connection_status_label = 'not connected'        
    
    def connect_to_controller(self, ports):
        global ser
        if ser.is_open:
            print('already connected')
        else:
            print('attempting to connect...')
            s = sc.ping_controller(ports, 9600, b'ping','pong',11)        
            if s == -1:
                return -1
            else:
                ser.port = s
                ser.open()
                ser.timeout = 11
                ser.write(b'get')
                print('get response: ' + ser.readline().decode().rstrip())
                return s

    def SendCommand(self, com, getResponse = False):     
        if ser.is_open:
            print('sending command: ' + com)            
            if('echo' in com or 'get' in com):
                getResponse = True
            command = str(com)+"\n"
            ser.write(command.encode())
            if getResponse:
                response = ser.readline().decode().rstrip()
                print('response: ' + response)
        else:
            print('Serial closed. Attempting to open')
            try:
                ser.open()
            except:
                print('oh heavens, there is a connection problem')
                pass

    def SetPosition(self, com, position):
        print('SetPosition com: '+com)
        #make sure that set commands use the right syntax
        if position.M2 < 100:
            m2 = '0'+str(position.M2)
        else:
            m2 = str(position.M2)
        if position.M3 < 100:
            m3 = '0'+str(position.M3)
        else:
            m3 = str(position.M3)
        if position.M4 < 100:
            m4 = '0'+str(position.M4)
        else:
            m4 = str(position.M4)
        if position.M5 < 100:
            m5 = '0'+str(position.M5)
        else:
            m5 = str(position.M5)
        if('set' in com or 'echo' in com):
            command = com+m2+m3+m4+m5
            print('command: ' + command)
            self.SendCommand(command)
        else:
            print('Tried to set position with invalid command')

if __name__ == '__main__':
    manager = RoboArmManager()
    manager.connect_to_controller(sc.serial_ports())
    while True:
        var = input("Please enter a command: ")
        print("entered: "+str(var))
        manager.SendCommand(str(var))