import serial_manager_base

class SyringePumpManager(serial_manager_base):
    def SetInitialState(self):
        print('SetInitialState()')