import roboarm_manager as r_m
import cnc_manager as c_m
import syringepump_manager as s_m
import serial_connection as s_c
import time

""" ToDo:
-multithread to allow concurrent movement of roboarm + cnc + pumps?
-abstract base class for serial_device_managers
 """
class SystemPosition:
    def __init__(self, M2=90, M3=90, M4=90, M5=90, X=0, Y=0, Z=0, E=0):
        self.M2 = M2
        self.M3 = M3
        self.M4 = M4
        self.M5 = M5
        self.X = X
        self.Y = Y
        self.Z = Z
        self.E = E

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
            portToRemove = self.cnc_ma.connect_to_controller(ports)
            print('removing port: ' + portToRemove)
            ports.remove(portToRemove)
            self.cnc_ma.SetInitialState()
            self.cnc_ma.SetPosition(self.PositionsDict['NeutralB'])
        if(self.ra_ma):
            portToRemove = self.ra_ma.connect_to_controller(ports)
            print('removing port: ' + portToRemove)
            ports.remove(portToRemove)
        if(self.syr_ma):
            self.syr_ma.Setup(ports)
        if(self.cnc_ma):
            time.sleep(1.1)
            self.SetPosition(self.PositionsDict['NeutralB'])
            time.sleep(1.1)
            self.SetPosition(self.PositionsDict['NeutralA'])

    def SetPosition(self, pos):
        self.ra_ma.SetPosition('set',pos)
        self.cnc_ma.SetPosition(pos)
        self.current_pos = pos

    def RelativePosition(self, diffpos):
        newpos = self.current_pos
        #loop through properties and sum at some point
        #for property, value in vars(mc.current_pos).items():
        #    property.__setattr__()
        newpos.M2 += diffpos.M2
        newpos.M3 += diffpos.M3
        newpos.M4 += diffpos.M4
        newpos.M5 += diffpos.M5
        newpos.X += diffpos.X
        newpos.Y += diffpos.Y 
        newpos.Z += diffpos.Z
        newpos.E += diffpos.E
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

    def __init__(self, *argv, setupSerial = True):
        #default to initializing all devices
        if(len(argv) == 0):
            argv = ['cnc','ra','syr']
        self.isBusy = False
        self.current_pos = SystemPosition()
        if('cnc' in argv):
            self.cnc_ma = c_m.CNCManager()
        else:
            self.cnc_ma = None
        if('ra' in argv):
            self.ra_ma = r_m.RoboArmManager()
        else:
            self.ra_ma = None
        if('syr' in argv):
            self.syr_ma = s_m.SyringePumpManager()
        else:
            self.syr_ma = None
        self.PositionsDict = {'NeutralA':NeutralA,'NeutralB':NeutralB, 
            'LoadA': LoadA, 'LoadB':LoadB,'LoadC':LoadC,'LoadD':LoadD,
            'UnloadA':UnloadA, 'UnloadB':UnloadB,'UnloadC':UnloadC}
        self.ActionsDict = {'Load':self.LoadSubstrateHolder,
            'Unload':self.UnloadSubstrateHolder,'Swap':self.SwapNewSubstrate,
            'Run':self.RunPump,'Stop':self.StopPump}
        if(setupSerial):
            self.SetupSerialIO()

if __name__ == '__main__':  
    mc = Movement_Coordinator(
    #'cnc',
    #'ra',
    #'syr'
    )  
    while True:
        var = input('Please enter a command: ')
        print('Entered: ' + var)
        mc.HandleCommand(var)

        """
        if('echo' in var or 'get' in var or 'set' in var):
            mc.ra_ma.SendCommand(var)
        elif(var in mc.PositionsDict.keys()):
            mc.SetPosition(mc.PositionsDict[var])
        elif(var in mc.ActionsDict.keys()):
            mc.ActionsDict[var]()
        else:
            mc.cnc_ma.SendCommand(var)

        var = input("Enter c for cnc, r for roboarm command, q to quit: ")
        print("Entered: "+var)
        if(var == 'c'):
            com = input('Please enter CNC command: ')
            cnc_ma.SendCommand(com)
        elif(var == 'r'):
            com = input('Please enter roboarm command: ')
            ra_ma.SendCommand(com)
        elif(var == 'q'):
            break
        else:
            print('Enter one of the valid letters you silly goose') """
