import serial

def WaitForOk():
    ser.reset_input_buffer()
    SerialBufferIsClear = False
    while(SerialBufferIsClear != True):
        MarlinMessage = ser.readline().decode()
        print(MarlinMessage)
        if("ok" in MarlinMessage):
            SerialBufferIsClear = True
            print("got the ok")

def SendCommandToCNC(com):
    print('sending command: ' + com)
    command = str(com)+"\n"
    ser.write(command.encode())
    WaitForOk()
    ser.write('M84\n'.encode())#dumb workaround to trigger busy:processing response from Marlin
    WaitForOk()

if __name__ == '__main__':
    #setup communication with Arduino Mega CNC controllers
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
    SendCommandToCNC('G1 E111 F2222')
