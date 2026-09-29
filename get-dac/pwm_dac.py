import RPi.GPIO as GPIO


class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose=False):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0)

        if self.verbose:
            print(
                f"PWM DAC инициализирован:"
                f" GPIO={gpio_pin}, F={pwm_frequency} Гц"
            )

    def deinit(self):
        self.pwm.stop()
        GPIO.cleanup()

        if self.verbose:
            print("PWM DAC остановлен")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} В)")
            print("Устанавливаем 0.0 В")

        duty_cycle = voltage / self.dynamic_range * 100

        self.pwm.ChangeDutyCycle(duty_cycle)

        if self.verbose:
            print(
                f"Напряжение: {voltage:.3f} В, "
                f"скважность: {duty_cycle:.2f}%"
            )


if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 10, 3.298, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()
