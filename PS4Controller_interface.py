from pyPS4Controller.controller import Controller
import movement_coordinator as mc
import time
#https://github.com/ArturSpirin/pyPS4Controllerhttps://github.com/ArturSpirin/pyPS4Controller

zpos = 151

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
    
    def on_x_press(self):
        global zpos
        zpos+=0.1
        command = 'G1 Z'+str(zpos)
        mc.cnc_ma.SendCommand(command)

mc.Setup()
controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()