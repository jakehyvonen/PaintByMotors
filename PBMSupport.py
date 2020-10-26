from decimal import *

class OldSystemPosition:
    def __init__(self, M2=90, M3=90, M4=90, M5=90, X=0, Y=0, Z=0, E=0):
        self.M2 = M2
        self.M3 = M3
        self.M4 = M4
        self.M5 = M5
        self.X = X
        self.Y = Y
        self.Z = Z
        self.E = E

class SystemPosition:
    def __init__(self, M2=90, M3=90, M4=90, M5=90, 
    X=0, Y=0, Z=0, E=0,cnc=None, servo=None):
        self.CNC = cnc
        if cnc:
            self.X = cnc.X
            self.Y = cnc.Y
            self.Z = cnc.Z
            self.E = cnc.E
        else:
            self.X = X
            self.Y = Y
            self.Z = Z
            self.E = E
            self.CNC = CNCPosition(X,Y,Z,E)
        self.Servo = servo
        if servo:
            self.M2 = servo.M2
            self.M3 = servo.M3
            self.M4 = servo.M4
            self.M5 = servo.M5
        else:
            self.M2 = M2
            self.M3 = M3
            self.M4 = M4
            self.M5 = M5
            self.Servo = ServoPosition(M2,M3,M4,M5)


class CNCPosition:
    def __init__(self, X=0, Y=0, Z=0, E=0):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.E = E

class ServoPosition:
    def __init__(self, M2=90, M3=90, M4=90, M5=90):
        self.M2 = M2
        self.M3 = M3
        self.M4 = M4
        self.M5 = M5

def PositionChanged(posA, posB):
    if(
        posA.X == posB.X and
        posA.Y == posB.Y and
        posA.Z == posB.Z and
        posA.E == posB.E and
        posA.M2 == posB.M2 and
        posA.M3 == posB.M3 and
        posA.M4 == posB.M4 and
        posA.M5 == posB.M5
        ):
        print('SystemPosition unchanged')        
        return False
    else:
        print('SystemPosition changed')
        return True

def CNCPositionChanged(posA, posB):
    if(
        posA.X == posB.X and
        posA.Y == posB.Y and
        posA.Z == posB.Z and
        posA.E == posB.E        
        ):
        print('CNCPosition unchanged')        
        return False
    else:
        print('CNCPosition changed')
        return True

def ServoPositionChanged(posA, posB):
    if(        
        posA.M2 == posB.M2 and
        posA.M3 == posB.M3 and
        posA.M4 == posB.M4 and
        posA.M5 == posB.M5
        ):
        print('ServoPosition unchanged')        
        return False
    else:
        print('ServoPosition changed')
        return True

def MakeDec(num,places = 2):
    p = '0.1'
    if(places == 0):
        p = '0'
    else:
        for i in range(1,places) :
            l = p.split('.')[1]
            p = '0.0' + l
    print('p: %s' % p)
    r = Decimal(str(num)).quantize(Decimal(p), rounding=ROUND_HALF_DOWN)
    return r

if __name__ == '__main__':
    print('dec: ' +  str(MakeDec(2.34567,4)))
