from DeviceManagerBase import DeviceManagerBase
import serial_connection as sc
from PositionSupport import *

m2 = '090'
m3 = '090'
m4 = '090'
m5 = '090'

class RoboArmManager(DeviceManagerBase):
    def __init__(self):
        super().__init__(name='RoboArm Arduino')
        self.lastpos = SystemPosition(servo=ServoPosition())

    def ConnectToDevice(self,ports = sc.serial_ports()):
        p = super().ConnectToDevice(defPort='/dev/ttyACM0',
        ports=ports, trycount=11, baud=9600, retmsg='ok')
        #self.ser.timeout = 11
        #self.SendCommand('ping')
        #self.ser.write(b'get')
        #print('get response: ' + self.ser.readline().decode().rstrip()) 
        self.ser.readlines()
        self.ser.flushInput()
        return p   

    def SendCommand(self, com, msg = 'ok'):
        super().SendCommand(com, waitMsg=msg)
        self.ser.flushInput()


    def SetPosition(self, com, pos, msg = 'ok'):
        #for property, value in vars(newpos).items():
        #    print('newpos property: ' + str(property) + ' value: ' + str(value))
        if(ServoPositionChanged(pos, self.lastpos)):
            print('SetPosition com: '+com)
            #make sure that set commands use the right syntax
            if pos.M2 < 100:
                m2 = '0'+str(pos.M2)
                if pos.M2 < 10:
                    m2 = '0' + m2
            else:
                m2 = str(pos.M2)
            if pos.M3 < 100:
                m3 = '0'+str(pos.M3)
                if pos.M3 < 10:
                    m3 = '0' + m3
            else:
                m3 = str(pos.M3)
            if pos.M4 < 100:
                m4 = '0'+str(pos.M4)
                if pos.M4 < 10:
                    m4 = '0' + m4
            else:
                m4 = str(pos.M4)
            if pos.M5 < 100:
                m5 = '0'+str(pos.M5)
                if pos.M5 < 10:
                    m5 = '0' + m5
            else:
                m5 = str(pos.M5)
            if('set' in com or 'echo' in com):
                command = com+m2+m3+m4+m5
                print('command: ' + command)
                self.SendCommand(command, msg)
            else:
                print('Tried to set pos with invalid command')
            self.lastpos = pos
    
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