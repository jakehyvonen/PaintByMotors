import roboarm_manager as r_m
import cnc_manager as c_m
import serial_connection as s_c

PositionsDict = {}
cnc_ma = c_m.CNCManager()
ra_ma = r_m.RoboArmManager()

class SystemPosition:
    def __init__(self, M2, M3, M4, M5, X, Y, Z, E):
        self.M2 = 90
        self.M3 = 90
        self.M4 = 90
        self.M5 = 90
        self.X = 0
        self.Y = 0
        self.Z = 0
        self.E = 0

def PopulatePositionsDict():
    global PositionsDict
    NeutralPosition = SystemPosition(45,45,45,45,11,11,11,0)
    PositionsDict = {'Neutral': NeutralPosition,}

def EstablishConnections():
    global cnc_ma, ra_ma
    ports = s_c.serial_ports()    
    portToRemove = cnc_ma.connect_to_controller(ports)
    ports.remove(portToRemove)
    print('removing port: ' + portToRemove)
    portToRemove = ra_ma.connect_to_controller(ports)
    print('removing port: ' + portToRemove)
    ports.remove(portToRemove)

if __name__ == '__main__':    
    EstablishConnections()
    while True:
        var = input("Enter c for cnc and r for roboarm command: ")
        print("Entered: "+var)
        if(var == 'c'):
            com = input('Please enter CNC command: ')
            cnc_ma.SendCommand(com)
        elif(var == 'r'):
            com = input('Please enter roboarm command: ')
            ra_ma.SendCommand(com)
        else:
            print('Enter one of the valid letters you silly goose')
