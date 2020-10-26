import RoboArmManager as r_m
import CNCManager as c_m
import SyringePumpManager as s_m
import serial_connection as s_c
import time
from PositionSupport import *

""" ToDo:
-multithreading to allow concurrent movement of roboarm + cnc + pumps?
 """

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
            self.SetPosition(PositionsDict['NeutralB'])
            time.sleep(1.1)
            self.SetPosition(PositionsDict['NeutralA'])

    def SetPosition(self, pos):        
        if self.cnc_ma and pos.CNC:
            self.cnc_ma.SetPosition(pos)
        if self.ra_ma and pos.Servo:
            self.ra_ma.SetPosition('set',pos)
        self.current_pos = pos

    def RelativePosition(self, diffpos):
        oldpos = self.current_pos
        cnc = None
        servo = None
        if diffpos.CNC:
            cnc = self.current_pos.CNC + diffpos.CNC
        if diffpos.Servo:
            servo = self.current_pos.Servo + diffpos.Servo
        newpos = SystemPosition(cnc=cnc, servo=servo)
        #for property, value in vars(newpos).items():
        #    print('newpos property: ' + str(property) + ' value: ' + str(value))
        if(PositionChanged(newpos, oldpos)):
            self.SetPosition(newpos)    

    def LoadSubstrateHolder(self):
        self.isBusy = True
        self.SetPosition(PositionsDict['LoadA'])
        self.SetPosition(PositionsDict['LoadB'])
        self.SetPosition(PositionsDict['LoadC'])
        self.SetPosition(PositionsDict['LoadD'])
        self.SetPosition(PositionsDict['NeutralB'])
        self.SetPosition(PositionsDict['NeutralA'])
        self.isBusy = False

    def UnloadSubstrateHolder(self):
        self.isBusy = True
        self.SetPosition(PositionsDict['UnloadA'])
        self.SetPosition(PositionsDict['UnloadB'])
        self.SetPosition(PositionsDict['UnloadC'])
        self.SetPosition(PositionsDict['UnloadB'])
        self.SetPosition(PositionsDict['UnloadA'])
        self.SetPosition(PositionsDict['NeutralA'])
        self.SetPosition(PositionsDict['NeutralB'])
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
        self.isEmulating = emulating
        self.current_pos = SystemPosition(cnc=CNCPosition(),
        servo=ServoPosition())
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

LowerCoatingLimit = SystemPosition(137,180,11,11,0,0,111,0)
UpperCoatingLimit = SystemPosition(137,180,171,171,33,33,177)

def SoftLimit(pos):
    for property, value in vars(pos).items():
        try:
            #print('property: ' + property + ' value: ' + str(value))
            lclval = getattr(LowerCoatingLimit,property)
            uclval = getattr(UpperCoatingLimit,property)
            if value > uclval:
                pos.__setattr__(property,uclval)
                #print('was greater than uclval: ' + str(uclval))
            elif value < lclval:
                pos.__setattr__(property,lclval)
                #print('was less than lclval: ' + str(lclval))
        except:
            #fucking error handling, how does it work?
            pass
    #for property, value in vars(pos).items():
        #print('property change?: ' + property + ' value: ' + str(value))
    return pos

if __name__ == '__main__':  
    #SoftLimit(LoadA)
    mc = Movement_Coordinator(
    'cnc',
    'ra',
    'syr',
    emulating=False
    )  
    while True:
        var = input('Please enter a command: ')
        print('Entered: ' + var)
        mc.HandleCommand(var)
