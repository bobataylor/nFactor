''' Serial communications via Arduino-passthrough'''

import serial

def establish_conn():
    print 'est. conn...'
    ser = serial.Serial('COM3', 9600, timeout=10)
    print 'finished...'
    return ser

def configure_requestnum(ser):
    print 'conf reqsum...'
    ser.write(chr(0xcc)*64)
    print 'wrote...'
    num = ser.read(size=1)
    return num
