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
    
    def connect_to_controller(self):
        global ser
        if ser.is_open:
            print('already connected')
        else:
            print('attempting to connect...')
            s = sc.ping_controller(sc.serial_ports(), 115200, b'ping','start\n')        
            if s == -1:
                return -1
            else:
                ser.port = s
                ser.open()
                ser.readlines()
    
    def WaitForOk(self):
        ser.reset_input_buffer()
        SerialBufferIsClear = False
        while(SerialBufferIsClear != True):
            MarlinMessage = ser.readline().decode()
            print(MarlinMessage)
            if("ok" in MarlinMessage):
                SerialBufferIsClear = True
                print("got the ok")

    def SendCommand(self, com,shouldwaitforok = True):        
        if ser.is_open:
            print('sending command: ' + com)
            command = str(com)+"\n"
            ser.write(command.encode())
            if shouldwaitforok:
                self.WaitForOk()
                ser.write('M84\n'.encode())#workaround to trigger busy:processing response from Marlin
                self.WaitForOk()
        else:
            print('serial not open')

if __name__ == '__main__':
    manager = CNCManager()
    manager.connect_to_controller()
    manager.SendCommand('M302 P1')

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
