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
            print('found port: '+port)
            #s = serial.Serial(port)
            #s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def ping_controller(ports, defaultPort, baud=9600, 
qrymsg=b'ping', retmsg='pong', trycount = 1, readsequence = '\n'):
    print('pinging serial with qrymsg: ' + qrymsg.decode())
    for port in ports:
        if(ping_single_port)
        except (OSError, serial.SerialException):
            pass
    print('no response to ping')
    return -1

def ping_single_port(port, baud, qrymsg, retmsg, trycount, readsequence):
    print('testing port: ' + port)
    try:
        s = serial.Serial(port,baud,timeout=1,write_timeout=1)
        time.sleep(1)
        s.flush()
        i = 0
        while i <= trycount:
            try:
                i += 1
                s.write(qrymsg)
                ret = ''
                if(readsequence == '\n'):
                    ret = s.readline()
                    ret = ret.decode().rstrip()
                elif(readsequence == b'\x03'):
                    ret = s.read_until(readsequence)
                    #strip first and last bytes to accomamodate New Era syntax
                    ret = ret.decode()[1:-1]
                else:
                    print('unrecognized readsequence')
                print('ret: ' + ret)
                print('retmsg: ' + retmsg)
                if ret == retmsg:
                    print('successfully connected to: '+s.name)
                    #s.close()
                    return True
            except:
                pass
        else:
            s.close()
            return False


def DebugPumps():
    print(serial_ports())
    print('starting serial test')
    ser = serial.Serial(
        port ="/dev/ttyUSB1",
        baudrate=19200,
        )
    command = b'VOL' + b'\r'
    ser.write(command)
    receivedmsg = False
    trycount = 0
    while (receivedmsg == False and trycount < 111):
        print('in bytes: ' + str(ser.in_waiting) + ' trycount: ' + str(trycount))
        trycount+=1
        if(ser.in_waiting > 0):
            response = ser.read_until(b'\x03')
            print(response)
            response = response.decode()[1:-1]#need to strip STX and ETX bytes (FUCKING HELL!!!!!!!)
            print('response: ' + response)
            retmsg = '00S60.00ML'
            print('retmsg: ' + retmsg)

            if(response == retmsg):
                print('yay i am sane')
            else:
                print('wat the fuckkkk')
                print('response type: '+str(type(response)))
                print('response len(): '+str(len(response)))
                for s in response:
                    print('s: ' + s)

                print('retmsg type: '+str(type(retmsg)))
                print('retmsg len(): '+str(len(retmsg)))
                for i in retmsg:
                    print('i: ' + i)
            receivedmsg = True
        else:
            ser.write(command)
    ser.close()
    print('finished')

def DebugRoboArm():
    ser = serial.Serial(        
        port="/dev/ttyACM0",
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1,
        write_timeout=1   
        )
    ser.flush()
    #ser.readlines()
    i = 0
    while i <11:
        if ser.in_waiting == 0:
            ser.write(b'ping')
        print('response: '+ser.readline().decode().rstrip())
        i += 1


def DebugMarlin():
    port = ping_controller(serial_ports(),115200,b'ping','start\n')
    """ ser = serial.Serial(        
        port="/dev/ttyUSB0",
        baudrate=115200       
        )
    ser.get_settings()
    ser.readlines()
    ser.write('M302 P1\n')
    ser.write('G1 E11 F333') """


if __name__ == '__main__':
    DebugPumps()