import smbus

class MCP3025:
    def __init__(self, dynamic_range,verbose = False):
            self.bus = smbus.SMBus(1)
            self.address = 0x4D
            self.verbose = verbose
            self.dynamic_range = dynamic_range
    def deinit(self):
        self.bus.close()
    def get_number(self):
        data=self.bus.read_word_data(self.address, 0)
        lower_data_byte=data>>8
        upper_data_byte=data&0xFF
        number=(upper_data_byte<<)
if __name__ == "__main__":
    try:
        dac = MCP4725(5.11, verbose=True)

        while True:
            try:
                voltage = float(
                    input("Введите напряжение в Вольтах: ")
                )
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
    except KeyboardInterrupt:
        print("\nПограмма завершилась")
    finally:
        dac.deinit()