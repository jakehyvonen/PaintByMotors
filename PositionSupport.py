'''
ToDo:
Add functions to sum ServoPositions and CNCPositions (RelativePosition)
'''

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
    def __init__(self, M2=None, M3=None, M4=None, M5=None, 
    X=None, Y=None, Z=None, E=None,cnc=None, servo=None):
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
            #self.CNC = CNCPosition(X,Y,Z,E)
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
            #self.Servo = ServoPosition(M2,M3,M4,M5)

NeutralA = SystemPosition(cnc=CNCPosition(0,0,151,0),
                servo=ServoPosition(137,180,33,90))#
NeutralB = SystemPosition(cnc=CNCPosition(0,0,151,0),
                servo=ServoPosition(17,111,1,90))#
NeutralArm = SystemPosition(servo=ServoPosition(137,180,33,90))

LoadA = SystemPosition(cnc=CNCPosition(48,0,151,0),
                servo=ServoPosition(11,111,0,90))#
LoadB = SystemPosition(cnc=CNCPosition(48,0,7,0),
                servo=ServoPosition(11,111,0,90))#
LoadC = SystemPosition(cnc=CNCPosition(48,0,1,0),
                servo=ServoPosition(11,87,0,90))#
LoadD = SystemPosition(cnc=CNCPosition(48,0,151,0),
                servo=ServoPosition(17,87,0,90))#
UnloadA = SystemPosition(cnc=CNCPosition(39,0,151,0),
                servo=ServoPosition(171,71,180,90))#
UnloadB = SystemPosition(cnc=CNCPosition(39,0,342,0),
                servo=ServoPosition(171,71,180,90))#
UnloadC = SystemPosition(cnc=CNCPosition(39,0,342,-322),
                servo=ServoPosition(171,71,180,90))#
Painting = SystemPosition(cnc=CNCPosition(27,11,272,0),
                servo=ServoPosition(137,180,33,90))#

PositionsDict = {
    'NeutralA':NeutralA,'NeutralB':NeutralB, 'NeutralArm':NeutralArm,
    'LoadA': LoadA, 'LoadB':LoadB,'LoadC':LoadC,'LoadD':LoadD,
    'UnloadA':UnloadA, 'UnloadB':UnloadB,'UnloadC':UnloadC,
    'Painting':Painting}

def PositionChanged(posA, posB):
    cncChanged = False
    servoChanged = False
    if posA.CNC:
        cncChanged = CNCPositionChanged(posA.CNC,posB.CNC)
    if posA.Servo:
        servoChanged = ServoPositionChanged(posA.Servo,posB.Servo)
    if cncChanged or servoChanged:
        return True
    else:
        return False

def CNCPositionChanged(posA, posB):
    if(
        posA.X == posB.X and
        posA.Y == posB.Y and
        posA.Z == posB.Z and
        posA.E == posB.E        
        ):
        #print('CNCPosition unchanged')        
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
        #print('ServoPosition unchanged')        
        return False
    else:
        print('ServoPosition changed')
        
        return True

def PositionSum(posA, posB):
    if type(posA) == CNCPosition:
        newPos = CNCPosition()
    elif type(posA) == ServoPosition:
        newPos = ServoPosition()
    for property, value in vars(posA).items():
        try:
            #print('property: ' + property + ' valueA: ' + str(value))
            posBval = getattr(posB,property)
            #print('property: ' + property + ' valueB: ' + str(posBval))
            newVal = value + posBval
            newPos.__setattr__(property,newVal)
        except:
            pass
    #for property, value in vars(newPos).items():
        #print('property change?: ' + property + ' value: ' + str(value))
    return newPos

if __name__ == '__main__':
    Apos = CNCPosition(1,2,3,4)
    Bpos = CNCPosition(3,3,3,3)
    #Cpos = ServoPosition(4,5,6,7)
    #Dpos = ServoPosition(6,6,6,6)
    PositionSum(Bpos,Apos)
    #PositionSum(Dpos,Cpos)