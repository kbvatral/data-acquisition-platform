# Script to read analog input from the ADS1x15 and save
# it to a csv file
# Author: Caleb Vatral

import time
import csv
import datetime
# Import the ADS1x15 module.
import Adafruit_ADS1x15


# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1

print('Reading ADS1x15 values, press Ctrl-C to quit...')

# Main loop.
while True:
    # Read all the ADC channel values in a list.
    valuesa0 = [0]*2  # Initialize 1x2 array of zeroes
    valuesa1 = [0]*2
    valuesa2 = [0]*2
    valuesa3 = [0]*2

    # Get the current datetime in a readable string: YYYY-MM-DD HH:mm:SS:ssssss
    valuesa0[0] = str(datetime.datetime.now())
    # Read the specified ADC channel using the previously set gain value
    valuesa0[1] = str(adc.read_adc(0, gain=GAIN))

    valuesa1[0] = str(datetime.datetime.now())
    valuesa1[1] = str(adc.read_adc(1, gain=GAIN))

    valuesa2[0] = str(datetime.datetime.now())
    valuesa2[1] = str(adc.read_adc(2, gain=GAIN))

    valuesa3[0] = str(datetime.datetime.now())
    valuesa3[1] = str(adc.read_adc(3, gain=GAIN))

    with open("data/dataLog0.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
        writer.writerow(valuesa0)
    with open("data/dataLog1.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
        writer.writerow(valuesa1)
    with open("data/dataLog2.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
        writer.writerow(valuesa2)
    with open("data/dataLog3.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
        writer.writerow(valuesa3)

    # Pause for half a second.
    time.sleep(0.5)
