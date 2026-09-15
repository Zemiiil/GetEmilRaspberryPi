import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
plus=9
minus=10
GPIO.setup(plus, GPIO.IN)
GPIO.setup(minus, GPIO.IN)
leds=[16, 12, 25, 17, 27, 23, 22, 24]
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)
num=0
def dec2bin(value):
    return [int(element) for element in bin(value) [2:].zfill(8)]
sleep_time=0.2
while True:
    a=GPIO.input(plus)
    b=GPIO.input(minus)
    if a and b:
        num=255
        print(num, dec2bin(num))
        time.sleep(sleep_time)
        GPIO.output(leds, dec2bin(num))
        continue
    if a:
        num+=1
        if num>255:
            num=0
        print(num, dec2bin(num))
        time.sleep(sleep_time)
    if b:
        num-=1
        if num <0:
            num=0
        print(num, dec2bin(num))
        time.sleep(sleep_time)
    GPIO.output(leds, dec2bin(num))
    