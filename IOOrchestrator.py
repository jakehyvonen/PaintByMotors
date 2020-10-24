import movement_coordinator as mover 
import XboxController_interface as xbox 
import time
from os.path import expanduser

#ToDo
#map list of controller button events to sending string commands to mc
#-
home = expanduser('~')
savedir = home + '/SIEData/'

class IOOrchestrator:
    def __init__(self,dbname='test.db'):
        self.dbpath = savedir+dbname
        self.xbox = xbox.Xbox_Interface()
        self.mc = mover.Movement_Coordinator(
            'cnc','ra','syr',emulating=True)

    def Setup(self):
        print('Setup()')

    def GetRuns(self):
        print('GetRuns()')

    def ReRunRun(self):
        print('ReRunRun()')

    def RecordXbox(self):
        print('RecordXbox()')

        ''' ;)
        while True:
            x = self.xbox.get_pos().X
            y = self.xbox.get_pos().Y
            if(not self.mc.isBusy):
                if(abs(x) > 0.1 or abs(y) > 0.1):
                    print('current_pos X: ' + str(x))
                    print('current_pos Y: ' + str(y))
                    self.mc.RelativePosition(self.xbox.current_pos)
            if(self.xbox.get_msg()):
                self.mc.HandleCommand(self.xbox.msg)'''

    def CNCCommand(self):
        print('CNCCommand()')

if __name__ == '__main__':  
    orc = IOOrchestrator()
    orc.RecordXbox()