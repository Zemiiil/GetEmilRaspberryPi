import smbus
import time
class MCP3021:
    def __init__(self, dynamic_range, verbose=False):
        self.bus = smbus.SMBus(1)
        self.address = 0x4D
        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        self.bus.close()

    def get_number(self):
        data = self.bus.read_word_data(self.address, 0)
        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)
        if self.verbose:
            print(f"Принятые данные: {data}, Старший байт: {upper_data_byte:x}, Младший байт: {lower_data_byte:x}, Число: {number}")
        return number
    def get_voltage(self):
        number = self.get_number()
        voltage = number / 1023 * self.dynamic_range
        if self.verbose:
            print(
                f"Код АЦП: {number}, "
                f"измеренное напряжение: {voltage:.3f} В"
            )
        return voltage

if __name__ == "__main__":
    adc = None
    try:
        adc = MCP3021(5.186, verbose=True)
        while True:
            voltage = adc.get_voltage()
            print(f"Напряжение: {voltage:.3f} В")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nПрограмма завершена")

    finally:
        if adc is not None:
            adc.deinit()
