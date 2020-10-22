import serial_manager_base

class RoboArmManager(serial_manager_base):
    def SetInitialState(self):
        print('SetInitialState()')

if __name__ == '__main__':
    manager = RoboArmManager()
    manager.connect_to_controller()
    while True:
        var = input("Please enter a command: ")
        print("entered: "+str(var))
        manager.SendCommand(str(var))