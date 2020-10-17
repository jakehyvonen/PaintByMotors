import movement_coordinator as mover 
import XboxController_interface as xbox 
import time

#ToDo
#map list of controller button events to sending string commands to mc
#-

if __name__ == '__main__':  
    mc = mover.Movement_Coordinator('cnc','syr')
    xi = xbox.Xbox_Interface()

    while True:
        x = xi.get_pos().X
        y = xi.get_pos().Y
        if(not mc.isBusy):
            if(abs(x) > 0.1 or abs(y) > 0.1):
                print('current_pos X: ' + str(x))
                print('current_pos Y: ' + str(y))
                mc.RelativePosition(xi.current_pos)
        if(xi.get_msg()):
            mc.HandleCommand(xi.msg)
        #time.sleep(0.1)