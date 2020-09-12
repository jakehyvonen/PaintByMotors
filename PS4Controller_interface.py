from pyPS4Controller.controller import Controller
import movement_coordinator as mc
import cnc_manager as cm
import time
#https://github.com/ArturSpirin/pyPS4Controllerhttps://github.com/ArturSpirin/pyPS4Controller

zpos = 0
manager = cm.CNCManager()

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
    
    def on_x_press(self):
        global zpos, manager
        zpos+=0.1
        command = 'G1 Z'+str(zpos)
        manager.SendCommand(command)

manager.Setup()
controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()