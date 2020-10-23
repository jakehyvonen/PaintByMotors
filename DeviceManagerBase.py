import serial
import serial_connection as sc
#from rx3 import Observable

#ser = serial.Serial()
#ser.port = None
#ser.baudrate = 9600
#ser.timeout = 1
#ser.write_timeout = 1

class DeviceManagerBase():
    def __init__(self,name = None,shouldSetup=False):
        self.connection_status = 'not connected'
        self.ser = serial.Serial(timeout=1,write_timeout=1)
        self.sent_command_event = Event()
        if not name:
            self.name = 'Mysterial Serial Device'
        else:
            self.name = name
        if shouldSetup:
            self.Setup()

    def ConnectToDevice(self, defPort=None, baud = 9600, qrymsg=b'ping', 
    retmsg='pong', trycount=1, ports = sc.serial_ports(), 
    readsequence = '\n'):
        if self.ser.is_open:
            print('already connected')
        else:
            print('attempting to connect to Device: %s' % self.name)
            s = sc.ping_controller(defPort, ports, baud, qrymsg, 
            retmsg, trycount, readsequence)                    
            self.ser.port = s
            self.ser.baudrate = baud
            self.ser.open()
            self.connection_status = 'connected'
            return s

    def WaitForResponse(self, response = 'ok'):
        DeviceNotBusy = False
        while(DeviceNotBusy != True):
            ret = self.ser.readline().decode().rstrip()
            print(ret)
            if(response in ret):
                DeviceNotBusy = True
                print("got the response: " + response)

    def SendCommand(self, com, waitMsg = None):        
        if self.ser.is_open:
            print('Device %s sending command: %s' %(self.name,com))
            self.sent_command_event.notify(com)
            command = str(com)+"\n"
            self.ser.write(command.encode())
            if waitMsg:
                self.WaitForResponse()            
                #workaround to trigger busy:processing response from Marlin
                #'M84\n'
                self.ser.write(waitMsg.encode())
                self.WaitForResponse()
        else:
            print('serial not open')

    def SetInitialState(self):
        raise NotImplementedError()

    def Setup(self):
        raise NotImplementedError()

class Event:
    def __init__(self):
        self.listeners = []

    def __iadd__(self, listener):
        """Shortcut for using += to add a listener."""
        self.listeners.append(listener)
        return self

    def notify(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)

if __name__ == '__main__':
    manager = DeviceManagerBase()
    #manager.Setup()
    while True:
        var = input("Please enter a command: ")
        print("entered: "+str(var))
        manager.SendCommand(var)
