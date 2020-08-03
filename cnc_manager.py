import serial
import serial_connection as sc

ser = serial.Serial()
ser.port = None
ser.baudrate = 115200
ser.timeout = 1
ser.write_timeout = 1

class CNCManager:
    def __init__(self):
        self.connection_status_label = 'not connected'        
    
    def connect_to_controller(self,ports):
        global ser
        if ser.is_open:
            print('already connected')
        else:
            print('attempting to connect...')
            s = sc.ping_controller(ports, 115200, b'ping','echo:start')        
            if s == -1:
                return -1
            else:
                ser.port = s
                ser.open()
                ser.readlines()
                return s
    
    def WaitForResponse(self,response = 'ok'):
        ser.reset_input_buffer()
        SerialBufferIsClear = False
        while(SerialBufferIsClear != True):
            MarlinMessage = ser.readline().decode().rstrip()
            print(MarlinMessage)
            if(response in MarlinMessage):
                SerialBufferIsClear = True
                print("got the response: " + response)

    def SendCommand(self, com,shouldwaitforok = True):        
        if ser.is_open:
            print('sending command: ' + com)
            command = str(com)+"\n"
            ser.write(command.encode())
            if shouldwaitforok:
                self.WaitForResponse()
                ser.write('M84\n'.encode())#workaround to trigger busy:processing response from Marlin
                self.WaitForResponse()
        else:
            print('serial not open')

    def SetupMarlin(self):
        #set max feedrate to 11 (default is 5)
        self.SendCommand('M203 Z11')
        #enable cold extrusion (allow usage of E axis)
        self.SendCommand('M302 P1')
        
    def SetInitialState(self):
        self.WaitForResponse('SD card')
        self.SendCommand('G28 X0 Z0')
        self.SetupMarlin()
        self.SendCommand('G1 Z151')
    
    def SetPosition(self,pos):
        com = 'G1 X'+str(pos.X)+' Y'+str(pos.Y)+' Z'+str(pos.Z)+' E'+str(pos.E)
        self.SendCommand(com)

if __name__ == '__main__':
    manager = CNCManager()
    manager.connect_to_controller(sc.serial_ports())
    manager.SendCommand('M302 P1')
    while True:
        var = input("Please enter a command: ")
        print("entered: "+str(var))
        manager.SendCommand(str(var))
    """ #setup communication with Arduino Mega CNC controllers
    ser = serial.Serial(
        
        port="/dev/ttyUSB0",
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        dsrdtr=True,
        rtscts=True,
        timeout=1
        )
    ser.get_settings()
    ser.readlines()
    SerialBufferIsClear = True
    SystemHasBeenInitialized = False
    SendCommandToCNC('M302 P1')#Allow cold extrusion to use E motor
    SendCommandToCNC('G1 E111 F2222') """
