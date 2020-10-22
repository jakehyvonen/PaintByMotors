import serial_manager_base

class CNCManager(serial_manager_base):
    def SendCommand(self, com, waitMsg = 'M84\n'):
        super().SendCommand(com,waitMsg)

    def SetPosition(self,pos):
        com = 'G1 X'+str(pos.X)+' Y'+str(pos.Y)+' Z'+str(pos.Z)+' E'+str(pos.E)
        super().SendCommand(com)

    def SetInitialState(self):
        self.WaitForResponse('SD card')
        self.SendCommand('G28 X0 Y0 Z0')

if __name__ == '__main__':
    manager = CNCManager()
    manager.connect_to_controller()
    #manager.Setup()
    while True:
        var = input("Please enter a command: ")
        print("entered: "+str(var))
        manager.SendCommand(str(var), False)