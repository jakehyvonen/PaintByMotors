import sys
import glob
import serial
import time

def serial_ports():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def ping_controller(ports, baud=9600, qrymsg=b'ping', retmsg='pong'):
    for port in ports:
        try:
            s = serial.Serial(port,baud,timeout=1)
            time.sleep(3)
            s.flush()
            s.write(qrymsg)
            ret = s.read(10)
            print(ret)
            if ret == retmsg:
                print(s.name)
                s.close()
                return port
            else:
                s.close()
        except (OSError, serial.SerialException):
            pass
    return -1

def DebugFunc():
    print(serial_ports())
    print('starting serial test')
    ser = serial.Serial(
        port ="/dev/ttyUSB1",
        baudrate=19200,
        )
    command = b'00DIA' + b'\r'
    ser.write(command)
    receivedmsg = False
    trycount = 0
    while (receivedmsg == False and trycount < 111):
        print('in bytes: ' + str(ser.in_waiting) + ' trycount: ' + str(trycount))
        trycount+=1
        if(ser.in_waiting > 0):
            response = ser.read_until(b'\x03')
            print(response)
            print('response: ' + str(response.decode()))
            receivedmsg = True
        else:
            ser.write(command)

    ser.close()
    print('finished')

if __name__ == '__main__':
    DebugFunc()