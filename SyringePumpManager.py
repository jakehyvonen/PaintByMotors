from DeviceManagerBase import DeviceManagerBase
import serial_connection as sc
import enum

dia60mLsyringe = 'S26.59'
diaquerybytes = b'00DIA\r'
ETXbyte = b'\x03'
#ToDo
#add rate change functionality 00RAT11.1MM 
#-->sets rate to 11.1 mL/min
'''
Note: if pump addresses are somehow reset, this won't work properly
--> addresses would need to be re-set individually via serial_connection.py 
'''

class SyringePumpManager(DeviceManagerBase):
    def __init__(self):
        super().__init__(name='NewEra Pumps')
        pump00 = SyringePump('00')
        pump01 = SyringePump('01')
        pump02 = SyringePump('02')
        self.Pumps = [pump00, pump01, pump02]
        self.PumpNames = []
        for p in self.Pumps:
            print('Created pump with name: ' + p.name)
            self.PumpNames.append(p.name)
        self.Actions = {'Volpercent':self.UpdateVolPercent,
        'Start':self.StartPumping,'Stop':self.StopPumping}

    def ConnectToDevice(self, ports = sc.serial_ports()):
        super().ConnectToDevice(ports=ports, defPort='/dev/ttyUSB1',
        baud=19200, qrymsg=diaquerybytes,retmsg='00'+dia60mLsyringe,
        trycount=11,readsequence=ETXbyte)

    def UpdateVolPercent(self, pump):
        print('UpdateVolPercent()')
        command = pump.address + 'VOL'
        maxV = self.SendCommand(command)
        pump.maxVol = maxV
        command = pump.address + 'DIS'
        dis = self.SendCommand(command)
    
    def StartPumping(self, pump):
        print('StartPumping(): ' + str(pump.name))
        pump.isPumping = True
        command = pump.address + 'RUN'
        self.SendCommand(command)
    
    def StopPumping(self, pump):
        print('StopPumping()' + str(pump.name))   
        pump.isPumping = False 
        command = pump.address + 'STP'
        self.SendCommand(command)

    def ActivePumps(self):
        active = False
        for p in self.Pumps:
            if p.isPumping:
                active = True
        return active

    def SendCommand(self, com, getResponse = True, tryCount = 1):  
        super().SendCommand(com, term='\r')
        if getResponse and not self.emulator_mode:
            #strip first and last bytes to accommodate New Era syntax
            response = self.ser.read_until(ETXbyte).decode().rstrip()[1:-1]
            print('Pumps response: ' + response)              
            return response
        '''p sure this is silly biz
        if self.ser.is_open:
            print('SendCommand(): ' + com)   
            super().sent_command_event.notify(com)         
            if('echo' in com or 'get' in com):
                getResponse = True
            command = str(com)+"\r"
            self.ser.write(command.encode())
            if getResponse:
                #strip first and last bytes to accommodate New Era syntax
                response = self.ser.read_until(ETXbyte).decode().rstrip()[1:-1]
                print('Pumps response: ' + response)              
                return response
        else:
            print('Serial closed. Attempting to open')
            '''           

    def DoAction(self, com):
        print('DoAction(): '+ com)
        pcom = str(com).split()
        pn = pcom[0]
        for pump in self.Pumps:
            if(pn == pump.name):
                print('pump.name: ' + pn)   
                act = pcom[1]           
                if(act in self.Actions.keys()):
                    print('Action: ' + act)
                    self.Actions[act](pump)
                else:
                    print("Command not found <(0_0)>")
        if pn not in self.PumpNames:
            manager.SendCommand(str(com),True)

    def PumpIsTalking(self,pump):
        print('PumpIsTalking()')
        ret = self.SendCommand(pump.address+'DIA')  
        #ignore status byte
        ret = ret[:2] + ret[3:]     
        if ret == pump.address + dia60mLsyringe[1:]:
            return True
        else:
            return False

    def Setup(self,ports=sc.serial_ports()):
        print('Setup() SyringePumpManager')    
        for p in ports:
            print('remaining port at syr_ma Setup(): ',p)        
        self.ConnectToDevice(ports)
        for p in self.Pumps:
            if not self.PumpIsTalking(p):
                print('pump with communication issues: ' +p.name)
                if not self.PumpIsTalking(p):
                    print('issues are persistent')
                else:
                    print('issues were resolved')

    def SetInitialState(self):
        print('SetInitialState()')

class RateUnits (enum.Enum):
    UM = 1 #uL/min
    MM = 2 #mL/Min
    UH = 3 #uL/hr
    MH = 4 #mL/hr

class SyringePump:
    def __init__(self, address = '00', maxVol = 60.0, 
    volPercent = 0.0, volDispensed = 0.0, rate = 11.0, units = RateUnits.MM):
            self.address = address
            self.name = 'pump' + address
            self.maxVol = maxVol
            self.volPercent = volPercent
            self.volDispensed = volDispensed
            self.rate = rate
            self.units = units
            self.isPumping = False

if __name__ == '__main__':
    manager = SyringePumpManager()
    manager.Setup()
    while True:
        var = input("Please enter a command: ")
        print("entered: "+str(var))
        manager.SendCommand(var)