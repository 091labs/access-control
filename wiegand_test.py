import RPi.GPIO as GPIO
from time import sleep
import sys

from userdb import UserDB


class RFidReader(object):
    GPIO_PIN_D0 = 17
    GPIO_PIN_D1 = 22
    GPIO_PIN_DOOR_RELEASE = 23
    GPIO_PIN_SOLENOID = 24

    def __init__(self):
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

    def run(self, testfn):
        # Now, here we go. The trick here is to detect the pulses and the gaps
        # as we're polling the whole damned time.
        while True:
            d0, d1 = [GPIO.input(p) for p in
                      [self.GPIO_PIN_D0, self.GPIO_PIN_D1]]

            # Check if the door release has been pressed...
            door_release_pressed = not GPIO.input(self.GPIO_PIN_DOOR_RELEASE)
            if door_release_pressed:
                print "Door release pressed"
                self.open_door = True

            # If we're not waiting for a bit (i.e. waiting for both lines to
            # go low) and both lines go low, then mark us as ready to read a
            # bit
            if not self.awaiting_bit:
                if not d0 and not d1:
                    self.awaiting_bit = True
                continue

            # If we get to here, it's assumed we're expecting a bit.
            if d0 != d1:    # Sure sign we have a bit...
                if d1:
                    self.number_string = self.number_string + "1"
                else:
                    self.number_string = self.number_string + "0"
                self.awaiting_bit = False

                if len(self.number_string) == 26:
                    # First and last bits are checksum bits, ignoring for now.
                    # TODO: use them to check that the number is valid
                    key_number = int(self.number_string[1:-1], 2)
                    print "Read tag: %d" % key_number

                    if testfn(key_number):
                        print "Key accepted"
                        self.open_door = True
                    else:
                        print "Key not accepted"
                    self.number_string = ""

            if self.open_door:
                GPIO.output(self.GPIO_PIN_SOLENOID, False)
                sleep(2)
                GPIO.output(self.GPIO_PIN_SOLENOID, True)
                self.open_door = False

reader = RFidReader()
db = UserDB()
reader.run(db.authenticate)
