import movement_coordinator as mover 
import syringepump_manager as sm 
import XboxController_interface as xbox 
import time

#ToDo
#Translate controller data to movement coordinator + syringepump manager
#-

if __name__ == '__main__':  
    mc = mover.Movement_Coordinator()
    mc.SetupSerialIO()
    xi = xbox.Xbox_Interface()

    while True:
        print('current_pos X: ' + str(xi.get_pos().X))
        print('current_pos Y: ' + str(xi.get_pos().Y))
        mc.RelativePosition(xi.current_pos)
        time.sleep(1.1)