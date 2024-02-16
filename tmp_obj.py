import machine
import utime


class TemperatureSensor:
    def __init__(self, adc_pin=4, conversion_factor=3.3 / 65535, LPF_en=0):
        self.sensor_temp = machine.ADC(adc_pin)
        self.conversion_factor = conversion_factor
        self.LPF_en = LPF_en
        self.samples = []

    def temperature_capture(self):
        try:
            readings = []
            for _ in range(5):
                reading = self.sensor_temp.read_u16() * self.conversion_factor
                readings.append(reading)

            average_reading = sum(readings) / len(readings)
            temperature = 27 - (average_reading - 0.706) / 0.001721

            if self.LPF_en:
                self.samples.append(temperature)
                if len(self.samples) > 5:
                    self.samples.pop(0)
                filtered_temperature = sum(self.samples) / len(self.samples)
                return filtered_temperature
            else:
                return temperature

        except Exception as e:
            print(f"Error capturing temperature: {e}")


def main():
    temp_sensor = TemperatureSensor(LPF_en=1)

    while True:
        temperature = temp_sensor.temperature_capture()
        print(temperature)
        utime.sleep(2)


if __name__ == "__main__":
    main()
