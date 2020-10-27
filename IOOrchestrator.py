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
        self.xbox.button_press_event += self.HandleButtonPress
        self.xbox.button_release_event += self.HandleButtonRelease
        self.xbox.axis_moved_event += self.HandleAxisMove
        if self.mc.cnc_ma:
            self.mc.cnc_ma.sent_command_event += self.RecordCNCCommand
        if self.mc.ra_ma:
            self.mc.ra_ma.sent_command_event += self.RecordRACommand
        if self.mc.syr_ma:
            self.mc.syr_ma.sent_command_event += self.RecordSYRCommand
        self.ActionsDict = {}    

    def FetchRuns(self):
        print('FetchRuns()')
        runs = self.dbrecord.FetchRuns()
        #at some point we'll be more sophisticated than CLI?

    def ReRunRun(self, runId):
        print('ReRunRun()')
        rrcomms = self.dbrecord.FetchRunData(runId=runId)
        st = time.perf_counter()
        i=0
        while i < len(rrcomms):
            t = time.perf_counter()
            et = t - st
            row = rrcomms[i]
            if row[0] < et:
                print('et: ', str(et))
                print('row[0]: ', str(row[0]))
                if row[1]:
                    print('row[1]: ', str(row[1]))
                    if not self.mc.isEmulating:
                        self.mc.cnc_ma.SendCommand(row[1])
                if row[2]:
                    print('row[2]: ', str(row[2]))
                    if not self.mc.isEmulating:
                        self.mc.ra_ma.SendCommand(row[2])
                if row[3]:
                    print('row[3]: ', str(row[3]))
                    if not self.mc.isEmulating:
                        self.mc.syr_ma.SendCommand(row[3])
                i += 1

    def StartRecordingXbox(self):
        print('RecordXbox()')             
        self.dbrecord.StartRun()

    def StopRecordingXbox(self):
        if self.dbrecord.isRecording:
            self.dbrecord.StopRun()
        else:
            print('already stopped recording, geeeeze')

    def RecordCNCCommand(self, com):
        if self.dbrecord.isRecording:
            self.dbrecord.AddCommandData(cnc=com)

    def RecordRACommand(self, com):
        if self.dbrecord.isRecording:
            self.dbrecord.AddCommandData(ra=com)

    def RecordSYRCommand(self, com):
        if self.dbrecord.isRecording:
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
            #print('Waiting on AxisDelay')
            pass
        else:
            #CNC AXIS
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
                self.mc.RelativeCNCPosition(self.current_cnc_pos)
                #reset positions after sending to avoid  
                #changing the position with other axis input
                self.current_cnc_pos.X = 0
                self.current_cnc_pos.Y = 0
                self.StartDelay()
            #SERVO AXIS
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
                self.mc.RelativeServoPosition(self.current_servo_pos)
                #reset positions after sending to avoid  
                #changing the position with other axis input
                self.current_servo_pos.X = 0
                self.current_servo_pos.Y = 0
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
        elif(button.name == 'button_x'):
            self.StartRecordingXbox()
        if msg:
            print('msg: %s' % msg)
            self.mc.HandleCommand(msg)

    def HandleButtonRelease(self, button):
        msg = None
        if(button.name == 'button_y'):
            msg = 'Stop,0'
        elif(button.name == 'button_b'):
            msg = 'Stop,1'
        elif(button.name == 'button_a'):
            msg = 'Stop,2'
        if msg:
            print('msg: %s' % msg)
            self.mc.HandleCommand(msg)   

    def HandleTerminalInput(self, var):
        if(var in self.ActionsDict.keys()):
            self.ActionsDict[var]()
        else:
            print('unrecognized action')

if __name__ == '__main__':  
    orc = IOOrchestrator()
    #orc.StartRecordingXbox()
    while True:
        orc.FetchRuns()
        var = input('Please enter a command: ')
        print('Entered: ' + var)
        orc.ReRunRun(var)
'''
     ;)
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