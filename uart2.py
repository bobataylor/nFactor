import time
import RPi.GPIO as RPIO
RPIO.setmode(RPIO.BCM)

BRANCH_LEN = 1*8
PK_LEN = 64*8
CONFIGURE_BYTE = 0xcc
DECRYPT_BYTE = 0xff
ACK_BYTE = 0xaa
ACK_LEN = 1*8
PK_FILE = 'nfactorkey'

class Port():
        def __init__(self, name, clock_in, clock_out, tx, rx, baud=9600):
                self.name = name
                self.wait       = 1.0/float(baud)
                self.clock_in  = clock_in
                self.clock_out = clock_out
                self.tx = tx
                self.rx = rx
                RPIO.setup(self.clock_in, RPIO.IN)
                RPIO.setup(self.clock_out, RPIO.OUT)
                RPIO.setup(self.tx, RPIO.OUT)
                RPIO.setup(self.rx, RPIO.IN)
                
                RPIO.output(self.clock_out, 1)
                
        def send(self, bin):
                print 'sending {}'.format(bin)
                bin_str = '{0:b}'.format(bin)
                print bin_str
                tick = 0
                for b in bin_str:
                        RPIO.output(self.clock_out, tick)
                        tick = not tick
                        print 'CLOCK: {}, DATA: {}'.format(RPIO.input(self.clock_out), int(b))
                        RPIO.output(self.tx, int(b))
                        time.sleep(self.wait)
                        
        def recv(self, bits, timeout=1):
                print 'recving {}, {}'.format(bits, timeout)
                #TODO get rid of leading bit and pick up trailing bit
                msg = ''
                count = 0
#                tock = RPIO.input(self.clock_in)
                tock = 1
                start = time.time()
                while (time.time() - start < timeout) or (timeout < 0):
                        tick = RPIO.input(self.clock_in)
                        if tick != tock:
                                tock = tick
                                msg += str(RPIO.input(self.rx))         # build binary value string
                                count += 1
                                last = time.time()
                                print '{} self.clock: {}, DATA: {}'.format(self.name, tick, msg[-1])
                        if count >= bits:
                                break   # end of message
                print 'uart message: {}'.format(msg)
                #TODO
                d = int(msg, 2)
                print 'uart value: {}'.format(d)
                return (d, count)

def decode(req):
        if req is not None:
                # TODO
                pass
        else:
                # TODO
                pass
                
def main_loop():
        print 'running...'
        next = Port(name='next', clock_in=13, 
                                clock_out=6, 
                                tx=19, 
                                rx=26)
        last = Port(name='last', clock_in=12, 
                                clock_out=16,
                                tx=21, 
                                rx=20)
        try:
                while True:
                        (val, num) = last.recv(BRANCH_LEN, timeout=-1)                          # receive decision byte
                        
                        if val == CONFIGURE_BYTE:                               # configure step
                                print 'configure byte: {}'.format(val)
                                last.send(ACK_BYTE)                                             # ack back
                                next.send(CONFIGURE_BYTE)                                       # send forward
                                (val, num) = next.recv(ACK_LEN, timeout=1)      # wait for ack response (1s timeout)
                                if num < ACK_LEN:                                                               # we are the last node
                                        last.send(1)                                                            # send first count value
                                elif val == ACK_BYTE:                                           # we are not the last node
                                        (val, num) = next.recv(ACK_LEN, timeout=-1)     # wait on response
                                        last.send(val+1)                                                        # add self to count and send
                                else:
                                        pass    # ERROR IF THIS IS HIT
                                        
                                private_key = None
                                while private_key is None:
                                        (val, num) = last.recv(PK_LEN, timeout=-1)      # wait for private key
                                        private_key = val                                                       # store private key
                                        last.send(ACK_BYTE)                                                     # ack back
                                        next.send(private_key)                                          # send forward
                                        (val, num) = next.recv(ACK_LEN, timeout=1)      # wait for ack response (1s timeout)
                                        if num < ACK_LEN:                                                       # we are the last node
                                                fp = open(PK_FILE, 'w')                                         # claim private sub-key
                                                fp.write(private_key)                                           #
                                                fp.close()                                                                      #
                                                last.send(private_key)                                          # signal finished
                                        elif val == ACK_BYTE:                                           # we are not the last node
                                                private_key = None                                                      # disown private key
                                                (val, num) = next.recv(PK_LEN, timeout=-1)      # wait on response
                                                last.send(val)                                                          # send back up the chain
                                        else:
                                                pass    # ERROR IF THIS IS HIT
                        
                        elif val == DECRYPT_BYTE:                               # decryption request step
                                print 'decrypt byte: {}'.format(val)
                                pass                    # not yet implemented
                        else:
                                print 'other byte: {}'.format(val)
                                time.sleep(1)   # most likely a private key we want to ignore
        finally:
                RPIO.cleanup()

def main_debug():
        pass
                
if __name__ == "__main__":
        main_loop()

