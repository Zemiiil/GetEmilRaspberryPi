import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
leds=[24,22,23,27,17,25,12,16]
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, 0)