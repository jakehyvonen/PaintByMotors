import roboarm_manager as r_m
import cnc_manager as c_m
import serial_connection as s_c

""" ToDo:
-multithread to allow concurrent movement of roboarm + cnc + pumps?
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

current_pos = SystemPosition()

def PopulatePositionsDict():
    global PositionsDict
    Neutral = SystemPosition(11,111,90,90,0,0,151,0)
    LoadA = SystemPosition(9,111,0,90,47,0,151,0)
    LoadB = SystemPosition(9,111,0,90,47,0,7,0)
    LoadC = SystemPosition(9,87,0,90,47,0,1,0)
    LoadD = SystemPosition(9,87,0,90,47,0,151,0)
    UnloadA = SystemPosition(171,77,180,90,39,0,151,0)
    UnloadB = SystemPosition(171,77,180,90,39,0,340,0)
    UnloadC = SystemPosition(171,77,180,90,39,0,340,-322)

    PositionsDict = {'Neutral':Neutral, 'LoadA': LoadA,
    'LoadB':LoadB,'LoadC':LoadC,'LoadD':LoadD,'UnloadA':UnloadA,
    'UnloadB':UnloadB,'UnloadC':UnloadC}


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
    global cnc_ma, ra_ma, 
    ra_ma.SetPosition('set',pos)
    cnc_ma.SetPosition(pos)

def LoadSubstrateHolder():
    global PositionsDict
    SetPosition(PositionsDict['LoadA'])
    SetPosition(PositionsDict['LoadB'])
    SetPosition(PositionsDict['LoadC'])
    SetPosition(PositionsDict['LoadD'])
    SetPosition(PositionsDict['Neutral'])

def UnloadSubstrateHolder():
    global PositionsDict
    SetPosition(PositionsDict['UnloadA'])
    SetPosition(PositionsDict['UnloadB'])
    SetPosition(PositionsDict['UnloadC'])
    SetPosition(PositionsDict['UnloadB'])
    SetPosition(PositionsDict['UnloadA'])
    SetPosition(PositionsDict['Neutral'])

def SwapNewSubstrate():
    UnloadSubstrateHolder()
    LoadSubstrateHolder()

ActionsDict = {'Load':LoadSubstrateHolder,
'Unload':UnloadSubstrateHolder,'Swap':SwapNewSubstrate}

if __name__ == '__main__':    
    Setup()
    while True:
        var = input('Please enter a command: ')
        print('Entered: ' + var)
        if('echo' in var or 'get' in var or 'set' in var):
            ra_ma.SendCommand(var)
        elif(var in PositionsDict.keys()):
            SetPosition(PositionsDict[var])
        elif(var in ActionsDict.keys()):
            ActionsDict[var]()
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
