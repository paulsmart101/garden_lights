#import the required modules
import RPi.GPIO as GPIO
import time

def setup_pins():
	print "in setup_pins"

	# set the pins numbering mode
	GPIO.setmode(GPIO.BOARD)

	# Select the GPIO pins used for the encoder K0-K3 data inputs
	GPIO.setup(11, GPIO.OUT)
	GPIO.setup(15, GPIO.OUT)
	GPIO.setup(16, GPIO.OUT)
	GPIO.setup(13, GPIO.OUT)

	# Select the signal to select ASK/FSK
	GPIO.setup(18, GPIO.OUT)

	# Select the signal used to enable/disable the modulator
	GPIO.setup(22, GPIO.OUT)

	# Disable the modulator by setting CE pin lo
	GPIO.output (22, False)

	# Set the modulator to ASK for On Off Keying 
	# by setting MODSEL pin lo
	GPIO.output (18, False)

	# Initialise K0-K3 inputs of the encoder to 0000
	GPIO.output (11, False)
	GPIO.output (15, False)
	GPIO.output (16, False)
	GPIO.output (13, False)
def activate():
	# let it settle, encoder requires this
	time.sleep(0.1)	
	# Enable the modulator
	GPIO.output (22, True)
	# keep enabled for a period
	time.sleep(0.25)
	# Disable the modulator
	GPIO.output (22, False)
def socket_one_on():
	print "sending code 1111 socket 1 on"
	GPIO.output (11, True)
	GPIO.output (15, True)
	GPIO.output (16, True)
	GPIO.output (13, True)
def socket_one_off():
	print "sending code 0111 Socket 1 off"
	GPIO.output (11, True)
	GPIO.output (15, True)
	GPIO.output (16, True)
	GPIO.output (13, False)
def socket_two_on():
	print "sending code 1110 socket 2 on"
	GPIO.output (11, False)
	GPIO.output (15, True)
	GPIO.output (16, True)
	GPIO.output (13, True)
def socket_two_off():
	print "sending code 0110 socket 2 off"
	GPIO.output (11, False)
	GPIO.output (15, True)
	GPIO.output (16, True)
	GPIO.output (13, False)
def socket_all_on():
	print "sending code 1011 ALL on"
	GPIO.output (11, True)
	GPIO.output (15, True)
	GPIO.output (16, False)
	GPIO.output (13, True)
def socket_all_off():
	print "sending code 0011 All off"
	GPIO.output (11, True)
	GPIO.output (15, True)
	GPIO.output (16, False)
	GPIO.output (13, False)

# ----------- MAIN---------------
setup_pins()
try:
	# We will just loop round switching the units on and off
	while True:
		raw_input('hit return key to send socket 1 ON code')
		socket_one_on()
		activate()

		raw_input('hit return key to send socket 1 OFF code')
		socket_one_off()
		activate()

		raw_input('hit return key to send socket 2 ON code')
		socket_two_on()
		activate()

		raw_input('hit return key to send socket 2 OFF code')
		socket_two_off()
		activate()
		
		raw_input('hit return key to send ALL ON code')
		socket_all_on()
		activate()

		raw_input('hit return key to send ALL OFF code')
		socket_all_off()
# Clean up the GPIOs for next time
except KeyboardInterrupt:
	GPIO.cleanup()


