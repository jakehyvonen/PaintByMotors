import serial
import serial_connection as sc
import enum

ser = serial.Serial()
ser.port = None
ser.baudrate = 19200
ser.timeout = 1
ser.write_timeout = 1
dia60mLsyringe = 'S26.59'
diaquerybytes = b'00DIA\r'
ETXbyte = b'\x03'
'''
Note: if pump addresses are somehow reset, this won't work properly
--> addresses would need to be re-set individually via serial_connection.py 
'''
class SyringePumpManager:
    def __init__(self):
            self.connection_status_label = 'not connected'     
            pump00 = SyringePump('00')
            pump01 = SyringePump('01')
            pump02 = SyringePump('02')
            self.Pumps = [pump00, pump01, pump02]
            self.PumpNames = []
            for p in self.Pumps:
                print('Created pump with name: ' + p.name)
                self.PumpNames.append(p.name)
            self.Actions = {'volpercent':self.UpdateVolPercent,
            'start':self.StartPumping,'stop':self.StopPumping}      

    def connect_to_controller(self,ports = sc.serial_ports()):
        global ser
        if ser.is_open:
            print('already connected')
        else:
            print('attempting to connect to SyringePumps...')
            s = sc.ping_controller('/dev/ttyUSB1', ports, 19200, diaquerybytes,'00'+dia60mLsyringe,11,ETXbyte)        
            if s == -1:
                return -1
            else:
                ser.port = s
                ser.open()               
                return s

    def RawCommand(self, com, getResponse = True, tryCount = 1):     
        if ser.is_open:
            print('RawCommand(): ' + com)            
            if('echo' in com or 'get' in com):
                getResponse = True
            command = str(com)+"\r"
            ser.write(command.encode())
            if getResponse:
                #strip first and last bytes to accomamodate New Era syntax
                response = ser.read_until(ETXbyte).decode().rstrip()[1:-1]
                print('response: ' + response)              
                return response
        else:
            print('Serial closed. Attempting to open')
            try:
                ser.open()
            except:
                print('oh heavens, there is a connection problem')
                pass    

    def UpdateVolPercent(self, pump):
        print('UpdateVolPercent()')
        command = pump.address + 'VOL'
        maxV = self.RawCommand(command)
        pump.maxVol = maxV
        command = pump.address + 'DIS'
        dis = self.RawCommand(command)
    
    def StartPumping(self, pump):
        print('StartPumping(): ' + str(pump.name))
        command = pump.address + 'RUN'
        self.RawCommand(command)
    
    def StopPumping(self, pump):
        print('StopPumping()' + str(pump.name))    
        command = pump.address + 'STP'
        self.RawCommand(command)

    def SendCommand(self, com):
        print('SendCommand(): '+ com)
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
            manager.RawCommand(str(com),True)

    def PumpIsTalking(self,pump):
        print('PumpIsTalking()')
        ret = self.RawCommand(pump.address+'DIA')       
        if ret == pump.address + dia60mLsyringe:
            return True
        else:
            return False


    def Setup(self,ports):
        print('Setup() SyringePumpManager')            
        self.connect_to_controller(ports)
        for p in self.Pumps:
            if not self.PumpIsTalking(p):
                print('pump with communication issues: ' +p.name)
                if not self.PumpIsTalking(p):
                    print('issues are persistent')
                else:
                    print('issues were resolved')


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
            self.active = False

if __name__ == '__main__':
    manager = SyringePumpManager()
    manager.Setup()
    while True:
        var = input("Please enter a command: ")
        print("entered: "+str(var))
        manager.SendCommand(var)