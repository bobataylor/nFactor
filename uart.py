import time
import RPi.GPIO as RPIO
RPIO.setmode(RPIO.BCM)

class Port():
	def __init__(self, clock, tx, rx, baud=9600):
		self.wait 	= 1.0/float(baud)
		self.clock  = clock
		self.tx     = tx
		self.rx     = rx

		RPIO.setup(self.clock, RPIO.IN)
		RPIO.setup(self.tx, RPIO.OUT)
		RPIO.setup(self.rx, RPIO.IN)
		
	def send(self, msg):
			binary = ''.join(format(ord(x),'b').zfill(8) for x in msg)
			print(binary)
			tick = 0
			for b in binary:
				RPIO.output(self.clock, tick)
				tick = not tick
				print("CLOCK: {}, DATA: {}".format(RPIO.input(self.clock),int(b)))
				RPIO.output(self.tx, int(b))
				time.sleep(self.wait)
				
	def recv(self, timeout=1):
		#TODO get rid of leading bit and pick up trailing bit
		msg = []
		tock = RPIO.input(self.clock)
		start = time.time()
		while( (time.time() - start < timeout) or (timeout < 0) ):
			tick = RPIO.input(self.clock)
			if tick != tock:
				tock = tick
				msg.append(RPIO.input(RX))
				last = time.time()
				print("self.clock: {}, DATA: {}".format(RPIO.input(self.clock),RPIO.input(self.rx)))
			if time.time() - last > 3:
				break # end of message
		print(msg)
		#TODO
		d = ''
		for i in range(0, len(msg), 8):
			d += ''.join(chr(int(msg[i:i+8],2)))
		print(d)
		return d

def main():
	last = Port(13, 19, 26)
	next = Port(16, 20, 21)
    try:
		req = last.recv(timeout=-1)		# Wait for request
		last.send('N+1')				# Send response
		next.send('REQUEST')			# Query the next module
		req = ''
		if(next.recv() == 'N+1'):   	# Wait 1 second for response
			req = next.recv(timeout=-1)	# Wait for nth-factor
		
		
		# Query the next module
		
		
    finally:
        RPIO.cleanup()

if __name__ == "__main__":
    main()

