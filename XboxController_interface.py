import signal
import time
import threading
from xbox360controller import Xbox360Controller
from movement_coordinator import SystemPosition

class Xbox_Interface:
    def __init__(self):
        self.current_pos = SystemPosition(0,0,0,0,0,0,0,0)
        self.msg = ''
        #self.HandleInput()
        th = threading.Thread(target=self.HandleInput)
        th.start()

    def get_pos(self):
        return self.current_pos

    def get_msg(self):
        return self.msg

    def HandleInput(self):
        try:
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

                # Left and right axis move event
                controller.axis_l.when_moved = self.on_axis_moved
                controller.axis_r.when_moved = self.on_axis_moved

                signal.pause()
        except KeyboardInterrupt:
            pass

    def on_button_pressed(self, button):
        print('Button {0} was pressed'.format(button.name))
        if(button.name == 'button_trigger_l'):
            self.msg = 'Swap'


    def on_button_released(self, button):
        print('Button {0} was released'.format(button.name))
        self.msg = ''


    def on_axis_moved(self, axis):
        #print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))
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