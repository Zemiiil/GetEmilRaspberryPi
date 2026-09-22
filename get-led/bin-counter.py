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
a_b_was=False
a_was=False
b_was=False
while True:
    a=GPIO.input(plus)
    b=GPIO.input(minus)
    if a and b:
        if not a_b_was:
            a_b_was=True
            num=255
            print(num, dec2bin(num))
            time.sleep(sleep_time)
            continue
    else:
        a_b_was=False
        if a:
            if not a_was:
                a_was=True
                num+=1
                if num>255:
                    num=0
                print(num, dec2bin(num))
                time.sleep(sleep_time)
        else:
            a_was=False
        if b:
            if not b_was:
                b_was=True
                num-=1
                if num <0:
                    num=0
                print(num, dec2bin(num))
                time.sleep(sleep_time)
        else:
            b_was=False
    GPIO.output(leds, dec2bin(num))
    