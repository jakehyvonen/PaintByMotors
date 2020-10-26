from decimal import *

class SystemPosition:
    def __init__(self, M2=90, M3=90, M4=90, M5=90, X=0, Y=0, Z=0, E=0):
        self.M2 = M2
        self.M3 = M3
        self.M4 = M4
        self.M5 = M5
        self.X = X
        self.Y = Y
        self.Z = Z
        self.E = E

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
