from serial_manager_base import SerialManagerBase
import serial_connection as sc

dia60mLsyringe = 'S26.59'
diaquerybytes = b'00DIA\r'
ETXbyte = b'\x03'
'''
Note: if pump addresses are somehow reset, this won't work properly
--> addresses would need to be re-set individually via serial_connection.py 
'''

class SyringePumpManager(SerialManagerBase):
    def __init__(self):
        super.__init__()
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

    def ConnectToDevice(self, ports = sc.serial_ports())

    def SetInitialState(self):
        print('SetInitialState()')