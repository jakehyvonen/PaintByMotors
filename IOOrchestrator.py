import movement_coordinator as mover 
from xbox360controller import controller
import XboxController_interface as xbox 
import time
from os.path import expanduser
from PBMSupport import *

#ToDo
#map list of controller button events to sending string commands to mc
#-
home = expanduser('~')
savedir = home + '/SIEData/'

class IOOrchestrator:
    def __init__(self,dbname='test.db'):
        self.dbpath = savedir+dbname
        self.xbox = xbox.Xbox_Interface()
        self.current_pos = mover.SystemPosition(0,0,0,0,0,0,0,0)
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
        self.xbox.button_press_event += self.HandleButtonPress
        self.xbox.button_release_event += self.HandleButtonRelease
        self.xbox.axis_moved_event += self.HandleAxisMove

    def CNCCommand(self):
        print('CNCCommand()')
        
    def HandleButtonPress(self, button):
        msg = 'None'
        if(button.name == 'button_trigger_l'):
            msg = 'Swap'
        elif(button.name == 'button_y'):
            msg = 'Run,0'
        elif(button.name == 'button_b'):
            msg = 'Run,1'
        elif(button.name == 'button_a'):
            msg = 'Run,2'
        elif(button.name == 'button_trigger_r'):
            isActive = False
        print('msg: %s' % msg)
        self.mc.HandleCommand(msg)

    def HandleButtonRelease(self, button):
        msg = 'None'
        if(button.name == 'button_trigger_l'):
            msg = 'None'
        elif(button.name == 'button_y'):
            msg = 'Stop,0'
        elif(button.name == 'button_b'):
            msg = 'Stop,1'
        elif(button.name == 'button_a'):
            msg = 'Stop,2'
        elif(button.name == 'button_trigger_r'):
            isActive = False
        print('msg: %s' % msg)
        self.mc.HandleCommand(msg)

    def HandleAxisMove(self, axis):
        if(axis.name == 'axis_r'):
            if(abs(axis.x) > 0.1):
                self.current_pos.X = MakeDec(axis.x)
            else:
                self.current_pos.X = 0
            if(abs(axis.y) > 0.1):
                self.current_pos.Y = MakeDec(axis.y)
            else:
                self.current_pos.Y = 0
            self.mc.RelativePosition(self.current_pos)
        if(axis.name == 'axis_l'):
            if(abs(axis.x) > 0.1):
                self.current_pos.M4 = MakeDec(axis.x)
            else:
                self.current_pos.M4 = 0
            if(abs(axis.y) > 0.1):
                self.current_pos.M5 = MakeDec(axis.y)
            else:
                self.current_pos.M5 = 0
            self.mc.RelativePosition(self.current_pos)



if __name__ == '__main__':  
    orc = IOOrchestrator()
    orc.RecordXbox()
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