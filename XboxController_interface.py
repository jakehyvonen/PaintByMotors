import signal
from time import sleep
import threading
from xbox360controller import Xbox360Controller
from PositionSupport import *
from Events import Event


class Xbox_Interface:
    def __init__(self,delay=1.1):
        self.current_pos = SystemPosition(0,0,0,0,0,0,0,0)
        self.msg = None
        self.isActive = False
        self.axis_threshold = 0.1
        #self.HandleInput()
        self.delay = delay
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
                # Button Trigger R events
                controller.button_trigger_r.when_pressed = self.on_button_pressed
                # Start Button events
                controller.button_start.when_pressed = self.on_button_pressed

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

    def on_button_released(self, button):
        print('Button {0} was released'.format(button.name))
        self.button_release_event.notify(button)

    def on_axis_moved(self, axis):
        #print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))
        if(abs(axis.x)>self.axis_threshold):
            self.axis_moved_event.notify(axis)
        elif(abs(axis.y)>self.axis_threshold):
            self.axis_moved_event.notify(axis)

if __name__ == '__main__':  
    xi = Xbox_Interface()
    while True:
        print('current_pos X: ' + str(xi.get_pos().X))
        print('current_pos Y: ' + str(xi.get_pos().Y))
        sleep(1.1)