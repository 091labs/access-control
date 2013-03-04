import RPi.GPIO as GPIO
from time import sleep
import sys


def dummy_test_keys(key):
    allowed_keys = [5374009, 3754335, 3791381]
    return key in allowed_keys


class RFidReader(object):
    GPIO_PIN_D0 = 17
    GPIO_PIN_D1 = 22
    GPIO_PIN_DOOR_RELEASE = 23
    GPIO_PIN_SOLENOID = 24

    def __init__():
        # Use the Broadcom numbering scheme
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.GPIO_PIN_D0, GPIO.IN, GPIO.PUD_OFF)
        GPIO.setup(self.GPIO_PIN_D1, GPIO.IN, GPIO.PUD_OFF)

        GPIO.setup(self.GPIO_PIN_DOOR_RELEASE, GPIO.IN, GPIO.PUD_UP)

        GPIO.setup(self.GPIO_PIN_SOLENOID, GPIO.OUT)
        # Set high so we lock on powerup
        GPIO.output(self.GPIO_PIN_SOLENOID, True)

        self.number_string = ""
        self.awaiting_bit = True
        self.open_door = False

    def run(testfn):
        # Now, here we go. The trick here is to detect the pulses and the gaps
        # as we're polling the whole damned time.
        while True:
            d0, d1 = [GPIO.input(p) for p in
                      [self.GPIO_PIN_D0, self.GPIO_PIN_D1]]

            # Check if the door release has been pressed...
            door_release_pressed = not GPIO.input(self.GPIO_PIN_DOOR_RELEASE)
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
        if d0 != d1:    # Sure sign we have a bit...
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

                if testfn(key_number):
                    print "Key accepted"
                    open_door = True
                else:
                    print "Key not accepted"
                number_string = ""

        if open_door:
            GPIO.output(self.GPIO_PIN_SOLENOID, False)
            sleep(2)
            GPIO.output(self.GPIO_PIN_SOLENOID, True)
            open_door = False

reader = RFidReader()
reader.run(dummy_test_keys)
