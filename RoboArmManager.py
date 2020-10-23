from DeviceManagerBase import DeviceManagerBase
import serial_connection as sc

m2 = '090'
m3 = '090'
m4 = '090'
m5 = '090'

class RoboArmManager(DeviceManagerBase):
    def ConnectToDevice(self,ports = sc.serial_ports()):
        self.name = 'RoboArm Arduino'
        super().ConnectToDevice(defPort='/dev/ttyACM0',
        ports=ports, trycount=11)
        self.ser.timeout = 11
        self.ser.write(b'get')
        print('get response: ' + self.ser.readline().decode().rstrip())    

    def SetPosition(self, com, position):
        print('SetPosition com: '+com)
        #make sure that set commands use the right syntax
        if position.M2 < 100:
            m2 = '0'+str(position.M2)
            if position.M2 < 10:
                m2 = '0' + m2
        else:
            m2 = str(position.M2)
        if position.M3 < 100:
            m3 = '0'+str(position.M3)
            if position.M3 < 10:
                m3 = '0' + m3
        else:
            m3 = str(position.M3)
        if position.M4 < 100:
            m4 = '0'+str(position.M4)
            if position.M4 < 10:
                m4 = '0' + m4
        else:
            m4 = str(position.M4)
        if position.M5 < 100:
            m5 = '0'+str(position.M5)
            if position.M5 < 10:
                m5 = '0' + m5
        else:
            m5 = str(position.M5)
        if('set' in com or 'echo' in com):
            command = com+m2+m3+m4+m5
            print('command: ' + command)
            self.SendCommand(command)
        else:
            print('Tried to set position with invalid command')
    
    def SetInitialState(self):
        print('SetInitialState()')

    def Setup(self):
        print('Setup()')

if __name__ == '__main__':
    manager = RoboArmManager()
    manager.ConnectToDevice()
    while True:
        var = input("Please enter a command: ")
        print("entered: "+str(var))
        manager.SendCommand(str(var))