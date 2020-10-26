from DeviceManagerBase import DeviceManagerBase
import serial_connection as sc
from PositionSupport import *

class CNCManager(DeviceManagerBase):
    def __init__(self):
        super().__init__(name='MarlinCNC Arduino')
        self.lastpos = SystemPosition(cnc=CNCPosition())
        #self.sent_command_event = super().sent_command_event

    def ConnectToDevice(self,ports = sc.serial_ports()):
        return super().ConnectToDevice(defPort='/dev/ttyUSB0',
        ports=ports, baud=115200, retmsg='echo:start')

    def SendCommand(self, com, waitMsg = 'M84\n'):
        super().SendCommand(com,waitMsg)

    def SetPosition(self,pos):
        if CNCPositionChanged(pos,self.lastpos):
            com = 'G1 X'+str(pos.X)+' Y'+str(pos.Y)+' Z'+str(pos.Z)+' E'+str(pos.E)
            self.SendCommand(com)

    def SetInitialState(self):
        self.WaitForResponse('SD card')
        self.SendCommand('G28 X0 Y0 Z0')

    def Setup(self):
        self.ConnectToDevice()
        self.SetInitialState()

def listenForCommands(command):
    print('heard a command: %s' % command)

if __name__ == '__main__':
    manager = CNCManager()
    manager.sent_command_event += listenForCommands
    #manager.ConnectToDevice()
    manager.Setup()
    while True:
        var = input("Please enter a command: ")
        print("entered: "+str(var))
        manager.SendCommand(str(var), False)