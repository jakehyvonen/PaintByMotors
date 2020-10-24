import signal
import time
import threading
from xbox360controller import Xbox360Controller
from movement_coordinator import SystemPosition
from Events import Event

class Xbox_Interface:
    def __init__(self):
        self.current_pos = SystemPosition(0,0,0,0,0,0,0,0)
        self.msg = None
        self.isActive = False
        #self.HandleInput()
        self.axis_moved_event = Event()
        self.button_press_event = Event()
        self.button_release_event = Event()
        th = threading.Thread(target=self.HandleInput)
        th.start()

    def get_pos(self):
        return self.current_pos

    def get_msg(self):
        return self.msg

    def HandleInput(self):
        try:
            self.isActive = True
            with Xbox360Controller(0, axis_threshold=0.0) as controller:
                # Button A events
                controller.button_a.when_pressed = self.on_button_pressed
                controller.button_a.when_released = self.on_button_released
                # Button B events
                controller.button_b.when_pressed = self.on_button_pressed
                controller.button_b.when_released = self.on_button_released
                # Button Y events
                controller.button_y.when_pressed = self.on_button_pressed
                controller.button_y.when_released = self.on_button_released
                # Button X events
                controller.button_x.when_pressed = self.on_button_pressed
                controller.button_x.when_released = self.on_button_released
                # Button Trigger L events
                controller.button_trigger_l.when_pressed = self.on_button_pressed
                controller.button_trigger_l.when_released = self.on_button_released
                # Button Trigger R events
                controller.button_trigger_r.when_pressed = self.on_button_pressed
                controller.button_trigger_r.when_released = self.on_button_released

                # Left and right axis move event
                controller.axis_l.when_moved = self.on_axis_moved
                controller.axis_r.when_moved = self.on_axis_moved

                signal.pause()
        except KeyboardInterrupt:
            self.isActive = False
            pass

    #button Y:pump0, B:pump1, A:pump2
    def on_button_pressed(self, button):
        print('Button {0} was pressed'.format(button.name))
        self.button_press_event.notify(button)
        #this should all be moved to IOOrchestrator
        if(button.name == 'button_trigger_l'):
            self.msg = 'Swap'
        elif(button.name == 'button_y'):
            self.msg = 'Run,0'
        elif(button.name == 'button_b'):
            self.msg = 'Run,1'
        elif(button.name == 'button_a'):
            self.msg = 'Run,2'
        elif(button.name == 'button_trigger_r'):
            self.isActive = False


    def on_button_released(self, button):
        print('Button {0} was released'.format(button.name))
        self.button_release_event.notify(button)
        #this should all be moved to IOOrchestrator
        self.msg = None
        if(button.name == 'button_trigger_l'):
            self.msg = 'Swap'
        elif(button.name == 'button_y'):
            self.msg = 'Stop,0'
        elif(button.name == 'button_b'):
            self.msg = 'Stop,1'
        elif(button.name == 'button_a'):
            self.msg = 'Stop,2'


    def on_axis_moved(self, axis):
        print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))
        self.axis_moved_event.notify(axis)
        #this should all be moved to IOOrchestrator
        if(axis.name == 'axis_l'):
            if(abs(axis.x) > 0.1):
                self.current_pos.X = axis.x
            else:
                self.current_pos.X = 0
            if(abs(axis.y) > 0.1):
                self.current_pos.Y = axis.y
            else:
                self.current_pos.Y = 0

if __name__ == '__main__':  
    xi = Xbox_Interface()
    while True:
        print('current_pos X: ' + str(xi.get_pos().X))
        print('current_pos Y: ' + str(xi.get_pos().Y))
        time.sleep(1.1)