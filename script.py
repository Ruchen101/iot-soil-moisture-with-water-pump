import time
import json
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
#Import GPIO lib
import RPi.GPIO as GPIO
#setup relay for pump
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)



# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)
# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

with open("cap_config.json") as json_data_file:
    config_data = json.load(json_data_file)
# print(json.dumps(config_data))

def percent_translation(raw_val):
    per_val = abs((raw_val- config_data["zero_saturation"])/(config_data["full_saturation"]-config_data["zero_saturation"]))*100
    return round(per_val, 3)

if __name__ == '__main__':
    print("----------  {:>5}\t{:>5}".format("Saturation", "Voltage\n"))
    while True:
        try:
            print("SOIL SENSOR: " + "{:>5}%\t{:>5.3f}".format(percent_translation(chan.value), chan.voltage))
            #If percent translation is below 45 turn on pump
            if (percent_translation(chan.value))<45:
                print("Your soil is dry.")
                GPIO.output(18, 1)
                time.sleep(5)
                GPIO.output(18, 0)
                print("Watering in progress...")
                time.sleep(6)
            #If percent translation is above 45 turn off pump
            else:
                GPIO.output(18, 1)
                print("Your soil has sufficient moisture.")
                time.sleep(6)
        except Exception as error:
            raise error
        except KeyboardInterrupt:
            print('exiting script')

            #Updated listen interval for real-time testing
#time.sleep(15)