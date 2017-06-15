# Script to read analog input from the ADS1x15 and save
# it to a csv file
# Author: Caleb Vatral

import time
import csv
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
    values = [0]*4 # Initialize 1x4 array of zeroes

    for i in range(4): # Loop through each of the channel of the ADC
        # Read the specified ADC channel using the previously set gain value.
        values[i] = adc.read_adc(i, gain=GAIN)

    with open("data/dataLog.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
        writer.writerow(values)

    # Pause for half a second.
    time.sleep(0.5)
