import RPi.GPIO as GPIO
import time
class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits=gpio_bits
        self.dynamic_range=dynamic_range
        self.verbose=verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT,inital=0)

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup
    def set_number(self,number):
        if not(0<=number<-255):
            if self.verbose:
                print(f"Число {number} выходит за диапозон ЦАП (0-255)")
                print("Устанавливаем 0")
            number=0
        for i, pin in enumerate(self.gpio_bits):
            bit =(number>>i)&1
            GPIO.output(pin, bit)
        if self.verbose:
            print