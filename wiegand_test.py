import RPi.GPIO as GPIO
from time import sleep
import sys 

# Keys allowed in. This is a bodge.
allowed_keys = [5374009, 3754335, 3791381]

# Use the Broadcom numbering scheme
GPIO.setmode(GPIO.BCM)

# Set GPIOs 17 & 22 to be the D0 and D1 inputs, respectively.
signal_pins = [17, 22]	# D0 and D1, respectively
for pin in signal_pins:
	GPIO.setup(pin, GPIO.IN, GPIO.PUD_OFF)

# Set GPIO 23 as the door release input.
GPIO.setup(23, GPIO.IN, GPIO.PUD_UP)

# Set GPIO 24 as the solenoid driver output, and set it high to ensure the lock
# is "armed"
GPIO.setup(24, GPIO.OUT)
GPIO.output(24, True)

number_string = ""
awaiting_bit = True
open_door = False

# Now, here we go. The trick here is to detect the pulses and the gaps
# as we're polling the whole damned time.
while True:
	d0, d1 = [GPIO.input(p) for p in signal_pins]
	
	# Check if the door release has been pressed...
	door_release_pressed = not GPIO.input(23)
	if door_release_pressed:
		print "Door release pressed"
		open_door = True

	# If we're not waiting for a bit (i.e. waiting for both lines to
	# go low) and both lines go low, then mark us as ready to read a bit.
	if not awaiting_bit:
		if not d0 and not d1:
			awaiting_bit = True
		continue 

	# If we get to here, it's assumed we're expecting a bit.
	if d0 != d1:	# Sure sign we have a bit...
		if d1:
			number_string = number_string + "1"
		else:
			number_string = number_string + "0"
		awaiting_bit = False

		if len(number_string) == 26:
			# First and last bits are checksum bits, ignoring for now.
			# TODO: use them to check that the number is valid
			key_number = int(number_string[1:-1], 2)
			print "Read tag: %d" % key_number

			if key_number in allowed_keys:
				print "Key accepted"
				open_door = True
			else:
				print "Key not accepted"	
			number_string = ""

	if open_door:
		GPIO.output(24, False)
		sleep(2)
		GPIO.output(24, True)
		open_door = False
