import RoboArmManager as r_m
import CNCManager as c_m
import SyringePumpManager as s_m
import serial_connection as s_c
import time
from PBMSupport import *

""" ToDo:
-multithread to allow concurrent movement of roboarm + cnc + pumps?
-abstract base class for serial_device_managers
 """

LowerCoatingLimit = SystemPosition(137,180,11,11,0,0,111,0)
UpperCoatingLimit = SystemPosition(137,180,171,171,33,33,177)

NeutralA = SystemPosition(137,180,33,90,0,0,151,0)
NeutralB = SystemPosition(17,111,1,90,0,0,151,0)
LoadA = SystemPosition(11,111,0,90,48,0,151,0)
LoadB = SystemPosition(11,111,0,90,48,0,7,0)
LoadC = SystemPosition(11,87,0,90,48,0,1,0)
LoadD = SystemPosition(11,87,0,90,48,0,151,0)
UnloadA = SystemPosition(171,71,180,90,39,0,151,0)
UnloadB = SystemPosition(171,71,180,90,39,0,342,0)
UnloadC = SystemPosition(171,71,180,90,39,0,342,-322)


class Movement_Coordinator:    
    def SetupSerialIO(self):
        ports = s_c.serial_ports()  
        if(self.cnc_ma):
            #don't test ports again once they're known
            portToRemove = self.cnc_ma.ConnectToDevice(ports)
            print('removing port: ' + str(portToRemove))
            ports.remove(portToRemove)
            self.cnc_ma.SetInitialState()
            self.cnc_ma.SetPosition(self.PositionsDict['NeutralB'])
        if(self.ra_ma):
            portToRemove = self.ra_ma.ConnectToDevice(ports)
            print('removing port: ' + str(portToRemove))
            ports.remove(portToRemove)
        if(self.syr_ma):
            self.syr_ma.Setup(ports)
        if(self.cnc_ma):
            time.sleep(1.1)
            self.SetPosition(self.PositionsDict['NeutralB'])
            time.sleep(1.1)
            self.SetPosition(self.PositionsDict['NeutralA'])

    def SetPosition(self, pos):
        if self.ra_ma:
            self.ra_ma.SetPosition('set',pos)
        if self.cnc_ma:
            self.cnc_ma.SetPosition(pos)
        self.current_pos = pos

    def RelativePosition(self, diffpos):
        newpos = self.current_pos
        newpos.M2 += diffpos.M2
        newpos.M3 += diffpos.M3
        newpos.M4 += diffpos.M4
        newpos.M5 += diffpos.M5
        newpos.X += diffpos.X
        newpos.Y += diffpos.Y 
        newpos.Z += diffpos.Z
        newpos.E += diffpos.E
        #for property, value in vars(newpos).items():
        #    print('newpos property: ' + str(property) + ' value: ' + str(value))
        if(PositionChanged(newpos, diffpos)):
            self.SetPosition(newpos)

    

    def LoadSubstrateHolder(self):
        self.isBusy = True
        self.SetPosition(self.PositionsDict['LoadA'])
        self.SetPosition(self.PositionsDict['LoadB'])
        self.SetPosition(self.PositionsDict['LoadC'])
        self.SetPosition(self.PositionsDict['LoadD'])
        self.SetPosition(self.PositionsDict['NeutralB'])
        self.SetPosition(self.PositionsDict['NeutralA'])
        self.isBusy = False


    def UnloadSubstrateHolder(self):
        self.isBusy = True
        self.SetPosition(self.PositionsDict['UnloadA'])
        self.SetPosition(self.PositionsDict['UnloadB'])
        self.SetPosition(self.PositionsDict['UnloadC'])
        self.SetPosition(self.PositionsDict['UnloadB'])
        self.SetPosition(self.PositionsDict['UnloadA'])
        self.SetPosition(self.PositionsDict['NeutralA'])
        self.SetPosition(self.PositionsDict['NeutralB'])
        self.isBusy = False

    def SwapNewSubstrate(self):
        self.UnloadSubstrateHolder()
        self.LoadSubstrateHolder()

    def RunPump(self, addr):
        addr = int(addr)
        pump = self.syr_ma.Pumps[addr]
        self.syr_ma.StartPumping(pump)
    
    def StopPump(self, addr):
        addr = int(addr)
        pump = self.syr_ma.Pumps[addr]
        self.syr_ma.StopPumping(pump)

    def HandleCommand(self, com):
        var = com
        data = None
        l = com.split(',')
        if(len(l)==2):
            var = l[0]
            data = l[1]
        if('echo' in var or 'get' in var or 'set' in var):
            self.ra_ma.SendCommand(var)
        elif(var in self.PositionsDict.keys()):
            self.SetPosition(self.PositionsDict[var])
        elif(var in self.ActionsDict.keys()):
            if(data):
                self.ActionsDict[var](data)
            else:
                self.ActionsDict[var]()
        else:
            self.cnc_ma.SendCommand(var)

    def __init__(self, *argv, setupSerial = True, emulating = False):
        #default to initializing all devices
        if(len(argv) == 0):
            argv = ['cnc','ra','syr']
        self.isBusy = False
        self.current_pos = SystemPosition()
        if('cnc' in argv):
            self.cnc_ma = c_m.CNCManager()
            self.cnc_ma.sent_command_event += listenForCommands
            if emulating:
                self.cnc_ma.emulator_mode = True
        else:
            self.cnc_ma = None
        if('ra' in argv):
            self.ra_ma = r_m.RoboArmManager()
            self.ra_ma.sent_command_event += listenForCommands
            if emulating:
                self.ra_ma.emulator_mode = True
        else:
            self.ra_ma = None
        if('syr' in argv):
            self.syr_ma = s_m.SyringePumpManager()
            self.syr_ma.sent_command_event += listenForCommands
            if emulating:
                self.syr_ma.emulator_mode = True
        else:
            self.syr_ma = None
        self.PositionsDict = {'NeutralA':NeutralA,'NeutralB':NeutralB, 
            'LoadA': LoadA, 'LoadB':LoadB,'LoadC':LoadC,'LoadD':LoadD,
            'UnloadA':UnloadA, 'UnloadB':UnloadB,'UnloadC':UnloadC}
        self.ActionsDict = {'Load':self.LoadSubstrateHolder,
            'Unload':self.UnloadSubstrateHolder,'Swap':self.SwapNewSubstrate,
            'Run':self.RunPump,'Stop':self.StopPump}
        if(setupSerial and not emulating):
            self.SetupSerialIO()

def listenForCommands(command):
    print('heard a command: %s' % command)

def SoftLimit(pos):
    for property, value in vars(pos).items():
        print('property: ' + property + ' value: ' + str(value))
        lclval = getattr(LowerCoatingLimit,property)
        print('lclval: ' + str(lclval))

if __name__ == '__main__':  
    SoftLimit(LoadA)
    '''
    mc = Movement_Coordinator(
    'cnc',
    'ra',
    'syr',
    emulating=True
    )  
    while True:
        var = input('Please enter a command: ')
        print('Entered: ' + var)
        mc.HandleCommand(var)
        '''