''' Serial communications via Arduino-passthrough'''

import serial

def establish_conn():
    print 'est. conn...'
    ser = serial.Serial('COM3', 9600, timeout=10)
    raw_input()
    print 'finished...'
    return ser

def configure_requestnum(ser):
    print 'conf reqsum...' 
    msg = chr(0xcc)*64
    ser.write(msg)
    print 'wrote...'
    num = ser.read(size=64)
    return num
