from decimal import *

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
