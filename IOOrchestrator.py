import movement_coordinator as mover 
import XboxController_interface as xbox 
import time

#ToDo
#map list of controller button events to sending string commands to mc
#-

if __name__ == '__main__':  
    mc = mover.Movement_Coordinator()
    mc.SetupSerialIO()
    xi = xbox.Xbox_Interface()

    while True:
        print('current_pos X: ' + str(xi.get_pos().X))
        print('current_pos Y: ' + str(xi.get_pos().Y))
        if(not mc.isBusy):
            mc.RelativePosition(xi.current_pos)
        if(xi.get_msg() != ''):
            mc.HandleCommand(xi.msg)
        #time.sleep(0.1)