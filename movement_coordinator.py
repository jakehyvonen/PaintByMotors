import roboarm_manager as r_m
import cnc_manager as c_m
import serial_connection as s_c

""" ToDo:
-multithreading to allow concurrent movement of roboarm + cnc + pumps
-clean up serial connection stuff (roboarm port gets opened multiple times which is annoying)
-calibrate positions for loading and unloading substrate holders
 """
PositionsDict = {}
cnc_ma = c_m.CNCManager()
ra_ma = r_m.RoboArmManager()

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

def PopulatePositionsDict():
    global PositionsDict
    Neutral = SystemPosition(90,90,90,90,0,0,151,0)
    LoadingA = SystemPosition(15,111,0,90,47,0,151,0)
    LoadingB = SystemPosition(15,111,0,90,47,0,11,0)
    LoadingC = SystemPosition(15,97,0,90,47,0,11,0)
    LoadingD = SystemPosition(15,97,0,90,47,0,151,0)

    PositionsDict = {'Neutral':Neutral, 'LoadingA': LoadingA,
    'LoadingB':LoadingB,'LoadingC':LoadingC,'LoadingD':LoadingD}

def Setup():
    global cnc_ma, ra_ma
    ports = s_c.serial_ports()    
    #don't test ports again once they're known
    portToRemove = cnc_ma.connect_to_controller(ports)
    print('removing port: ' + portToRemove)
    ports.remove(portToRemove)
    cnc_ma.SetInitialState()
    portToRemove = ra_ma.connect_to_controller(ports)
    print('removing port: ' + portToRemove)
    ports.remove(portToRemove)
    PopulatePositionsDict()

def SetPosition(pos):
    global cnc_ma, ra_ma
    ra_ma.SetPosition('set',pos)
    cnc_ma.SetPosition(pos)

if __name__ == '__main__':    
    Setup()
    while True:
        var = input('Enter echo get set for roboarm, else CNC: ')
        print('Entered: ' + var)
        if('echo' in var or 'get' in var or 'set' in var):
            ra_ma.SendCommand(var)
        elif(var in PositionsDict.keys()):
            SetPosition(PositionsDict[var])
        else:
            cnc_ma.SendCommand(var)

        """ var = input("Enter c for cnc, r for roboarm command, q to quit: ")
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
