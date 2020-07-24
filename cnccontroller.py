import serial
import serial_connection as sc

class CNCController:
    def __init__(self):
        self.ser = sc.ping_controller(sc.serial_ports(), 115200, b'ping','start\n')
    
    def WaitForOk(self):
        self.ser.reset_input_buffer()
        SerialBufferIsClear = False
        while(SerialBufferIsClear != True):
            MarlinMessage = self.ser.readline().decode()
            print(MarlinMessage)
            if("ok" in MarlinMessage):
                SerialBufferIsClear = True
                print("got the ok")

    def SendCommandToCNC(self, com):
        print('sending command: ' + com)
        command = str(com)+"\n"
        self.ser.write(command.encode())
        self.WaitForOk()
        self.ser.write('M84\n'.encode())#workaround to trigger busy:processing response from Marlin
        self.WaitForOk()

if __name__ == '__main__':
    controller = CNCController()

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
