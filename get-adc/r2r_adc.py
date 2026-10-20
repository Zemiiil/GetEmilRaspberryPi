import RPi.GPIO as GPIO
import time


class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")
            return
        if not (0 <= number <= 255):
            print("Число выходит за разрядность ЦАП (8 бит)")
            return
        bits = [int(element) for element in bin(number)[2:].zfill(8)]
        GPIO.output(self.bits_gpio, bits)
        if self.verbose:
            print(f"Число на вход ЦАП: {number}, биты: {bits}")

    def sequential_counting_adc(self):
        for number in range(256):
            self.number_to_dac(number)
            time.sleep(self.compare_time)
            comparator_value = GPIO.input(self.comp_gpio)
            if comparator_value == 1:
                return number
        return 255

    def get_sc_voltage(self):
        number = self.sequential_counting_adc()
        voltage = number / 255 * self.dynamic_range-0.0065

        if self.verbose:
            print(
                f"Код АЦП: {number}, "
                f"измеренное напряжение: {voltage:.3f} В"
            )

        return voltage
    def successive_approximation_adc(self):
        number = 0
        for i in range (8):
            candidate = number | (1 << 7-i)
            self.number_to_dac(candidate)
            time.sleep(self.compare_time)
            comparator_value = GPIO.input(self.comp_gpio)
            if comparator_value == 0:
                number = candidate
            if self.verbose:
                print(
                    f"Проверяем код: {candidate}, "
                    f"текущий результат: {number}, "
                    f"компаратор: {comparator_value}"
                )
        self.number_to_dac(number)
        return number
    def get_sar_voltage(self):
        number = self.successive_approximation_adc()
        voltage = number / 255 * self.dynamic_range

        if self.verbose:
            print(
                f"Код АЦП: {number}, "
                f"измеренное напряжение: {voltage:.3f} В"
            )
        return voltage
if __name__ == "__main__":
    adc = None

    try:
        adc = R2R_ADC(3.333, compare_time=0.0001, verbose=False)
        metod=int(input("Напиши 0 если надо методом sequential_counting или 1 если надо successive_approximation: "))
        if metod == 0:
            while True:
                voltage = adc.get_sc_voltage()
                print(f"Напряжение потенциометра: {voltage:.3f} В")
        if metod==1:
            while True:
                voltage = adc.get_sar_voltage()
                print(f"Напряжение потенциометра: {voltage:.3f} В")
    except KeyboardInterrupt:
        print("\nИзмерение остановлено")

    finally:
        if adc is not None:
            adc.deinit()
