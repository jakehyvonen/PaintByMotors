import movement_coordinator as mover 
from xbox360controller import controller
import XboxController_interface as xbox 
from time import sleep
from os.path import expanduser
from PositionSupport import *
from PBMSupport import *
import threading
from RunDBRecorder import *

#ToDo
#implement axis input filtering by time:
#-loop that fetches axis input after a given delay
#
home = expanduser('~')
savedir = home + '/SIEData/'
axisDelay = False

class IOOrchestrator:
    def __init__(self,dbname='test.db'):
        #self.dbpath = savedir+dbname
        self.dbname = dbname
        self.dbrecord = RunDBRecorder(dbname)
        self.xbox = xbox.Xbox_Interface()
        self.delay = 0.1
        self.current_pos = SystemPosition(0,0,0,0,0,0,0,0)
        self.current_cnc_pos = CNCPosition(0,0,0,0)
        self.current_servo_pos = ServoPosition(0,0,0,0)
        self.mc = mover.Movement_Coordinator(
            'cnc','ra','syr',isEmulating=True,isPainting=True)
    
    def SetupRunDBRecorder(self):
        print('SetupRecorder()')
        

    def StartRunDBRecorder(self):
        print('StartRunDBRecorder')

    def GetRuns(self):
        print('GetRuns()')

    def ReRunRun(self):
        print('ReRunRun()')

    def RecordXbox(self):
        print('RecordXbox()')     
        self.xbox.button_press_event += self.HandleButtonPress
        self.xbox.button_release_event += self.HandleButtonRelease
        self.xbox.axis_moved_event += self.HandleAxisMove
        if self.mc.cnc_ma:
            self.mc.cnc_ma.sent_command_event += self.RecordCNCCommand
        if self.mc.ra_ma:
            self.mc.ra_ma.sent_command_event += self.RecordRACommand
        if self.mc.syr_ma:
            self.mc.syr_ma.sent_command_event += self.RecordSYRCommand
        self.dbrecord.StartRun()

    def StopRecordingXbox(self):
        self.dbrecord.StopRun()

    def RecordCNCCommand(self, com):
        self.dbrecord.AddCommandData(cnc=com)

    def RecordRACommand(self, com):
        self.dbrecord.AddCommandData(ra=com)

    def RecordSYRCommand(self, com):
        self.dbrecord.AddCommandData(syr=com)

    #we want to filter the controller input to avoid overloading
    #the MarlinCNC and RoboArm MCUs
    def AxisDelay(self):
        global axisDelay
        axisDelay = True
        sleep(self.delay)
        axisDelay = False

    def StartDelay(self):
        th = threading.Thread(target=self.AxisDelay)
        th.start()

    def HandleAxisMove(self, axis):
        global axisDelay
        if axisDelay:
            print('Waiting on AxisDelay')
            pass
        else:
            if(axis.name == 'axis_r'):
                if(abs(axis.x) > 0.1):
                    self.current_cnc_pos.X = MakeDec(axis.x)
                else:
                    self.current_cnc_pos.X = 0
                if(abs(axis.y) > 0.1):
                    self.current_cnc_pos.Y = MakeDec(axis.y)
                else:
                    self.current_cnc_pos.Y = 0
                self.current_pos.CNC = self.current_cnc_pos
                self.mc.RelativePosition(self.current_pos)
                self.StartDelay()
            if(axis.name == 'axis_l'):
                if(axis.x > 0.1):
                    self.current_servo_pos.M4 = 1
                elif(axis.x < -0.1):
                    self.current_servo_pos.M4 = -1
                else:
                    self.current_servo_pos.M4 = 0
                if(axis.y > 0.1):
                    self.current_servo_pos.M5 = 1
                elif(axis.y < -0.1):
                    self.current_servo_pos.M5 = -1
                else:
                    self.current_servo_pos.M5 = 0
                self.current_pos.Servo = self.current_servo_pos
                self.mc.RelativePosition(self.current_pos)
                self.StartDelay()
        
    def HandleButtonPress(self, button):
        msg = None
        if(button.name == 'button_trigger_l'):
            msg = 'Swap'
        elif(button.name == 'button_y'):
            msg = 'Run,0'
        elif(button.name == 'button_b'):
            msg = 'Run,1'
        elif(button.name == 'button_a'):
            msg = 'Run,2'
        elif(button.name == 'button_trigger_r'):
            self.StopRecordingXbox()
        if msg:
            print('msg: %s' % msg)
            self.mc.HandleCommand(msg)

    def HandleButtonRelease(self, button):
        msg = None
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
        if msg:
            print('msg: %s' % msg)
            self.mc.HandleCommand(msg)   

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