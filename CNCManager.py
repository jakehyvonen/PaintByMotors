from DeviceManagerBase import DeviceManagerBase
import serial_connection as sc

class CNCManager(DeviceManagerBase):
    def ConnectToDevice(self,ports = sc.serial_ports()):
        self.name('MarlinCNC Arduino')
        super().ConnectToDevice(defPort='/dev/ttyUSB0',
        ports=ports, baud=115200, retmsg='echo:start')

    def SendCommand(self, com, waitMsg = 'M84\n'):
        super().SendCommand(com,waitMsg)

    def SetPosition(self,pos):
        com = 'G1 X'+str(pos.X)+' Y'+str(pos.Y)+' Z'+str(pos.Z)+' E'+str(pos.E)
        super().SendCommand(com)

    def SetInitialState(self):
        self.WaitForResponse('SD card')
        self.SendCommand('G28 X0 Y0 Z0')

    def Setup(self):
        self.ConnectToDevice()
        self.SetInitialState()

if __name__ == '__main__':
    manager = CNCManager()
    #manager.ConnectToDevice()
    manager.Setup()
    while True:
        var = input("Please enter a command: ")
        print("entered: "+str(var))
        manager.SendCommand(str(var), False)