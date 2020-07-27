import roboarm
import cnc_manager

PositionsDict = {}

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


if __name__ == '__main__':
    ra_ma = roboarm.roboarm_manager.RoboArmManager()
    ra_ma.connect_to_controller()
    cnc_ma = cnc_manager.CNCManager()
    cnc_ma.connect_to_controller()