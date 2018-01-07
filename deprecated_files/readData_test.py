# Script to simulate reading analog input from the ADS1x15 and save
# it to a csv file
# Author: Caleb Vatral

import csv
import time
import datetime
from random import randint

while True:
    # Read all the ADC channel values in a list.
    valuesa0 = [0]*2  # Initialize 1x2 array of zeroes
    valuesa1 = [0]*2
    valuesa2 = [0]*2
    valuesa3 = [0]*2

    # Get the current datetime in a readable string: YYYY-MM-DD HH:mm:SS:ssssss
    valuesa0[0] = str(datetime.datetime.now())
    # Read the specified ADC channel using the previously set gain value
    valuesa0[1] = str(randint(0, 32767))

    valuesa1[0] = str(datetime.datetime.now())
    valuesa1[1] = str(randint(0, 32767))

    valuesa2[0] = str(datetime.datetime.now())
    valuesa2[1] = str(randint(0, 32767))

    valuesa3[0] = str(datetime.datetime.now())
    valuesa3[1] = str(randint(0, 32767))

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
    time.sleep(1)
