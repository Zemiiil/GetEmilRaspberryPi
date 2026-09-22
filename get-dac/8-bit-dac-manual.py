import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
dac_bits=[22,27, 17,26,25,21,20,16]
GPIO.setup(dac_bits, GPIO.OUT)
GPIO.output(dac_bits, 0)
dynamic_range=3.3
def voltage_to_number (voltage):
    if not(0.0<=voltage<=dynamic_range):
        print(f"Напряжение выходит за динамический диапозон ЦАП (0.00 - {dynamic_range: .2f} B")
        print ("Устанавливаем 0.0 В")
        return 0
    return int(voltage/dynamic_range *255)
def number_to_dac(number):
    for i, pin in enumerate(dac_bits):
        bit=(number>>i)&1
        GPIO.output(pin, bit)
    

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)
        except ValueError:
            print("Вы ввели не число попроуйте ещё раз \n")
finally:
    GPIO.output(dac_bits, 0)
    GPIO.cleanup()