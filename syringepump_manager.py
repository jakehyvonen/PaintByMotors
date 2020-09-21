import serial
import serial_connection as sc
import enum

ser = serial.Serial()
ser.port = None
ser.baudrate = 19200
ser.timeout = 1
ser.write_timeout = 1
'''
Note: if pump addresses are somehow reset, this will fuck up
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

    def connect_to_controller(self, ports=sc.serial_ports()):
        global ser
        if ser.is_open:
            print('already connected')
        else:
            print('attempting to connect...')
            s = sc.ping_controller(ports, 19200, b'00DIA\r','00S26.59',11,b'\x03')        
            if s == -1:
                return -1
            else:
                ser.port = s
                ser.open()               
                return s

    def RawCommand(self, com, getResponse = True):     
        if ser.is_open:
            print('RawCommand(): ' + com)            
            if('echo' in com or 'get' in com):
                getResponse = True
            command = str(com)+"\r"
            ser.write(command.encode())
            if getResponse:
                response = ser.read_until(b'\x03').decode().rstrip()
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
        print('StartPumping(): ' + str(pump))
    
    def StopPumping(self, pump):
        print('StopPumping()' + str(pump))    

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

    def Setup(self):
            print('PopulateDicts() SyringePumpManager')
            
            self.connect_to_controller(sc.serial_ports())

class RateUnits (enum.Enum):
    UM = 1 #uL/min
    MM = 2 #mL/Min
    UH = 3 #uL/hr
    MH = 4 #mL/hr

class SyringePump:
    def __init__(self, address = '00', maxVol = 60.0, 
    volPercent = 0.0, rate = 11.0, units = RateUnits.MM):
            self.address = address
            self.name = 'pump' + address
            self.maxVol = maxVol
            self.volPercent = volPercent
            self.rate = rate
            self.units = units

if __name__ == '__main__':
    manager = SyringePumpManager()
    manager.Setup()
    while True:
        var = input("Please enter a command: ")
        print("entered: "+str(var))
        manager.SendCommand(var)