'''Note: this class has not yet been incorporated into the rest of the app
 just added as a reminder of what to do'''

class DeviceManagerBase:
    def __init__(self):
        self.connection_status_label = 'not connected'        
    
    def connect_to_controller(self,ports=sc.serial_ports()):
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
    
    def SetInitialState(self):
        self.WaitForResponse('SD card')
        self.SendCommand('G28 X0 Y0 Z0')
        #self.SendCommand('G1 Z151')
    
    def Setup(self):
        self.connect_to_controller()
        self.SetInitialState()