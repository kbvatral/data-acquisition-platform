# Script to simulate reading analog input from the ADS1x15 and save
# it to a csv file
# Author: Caleb Vatral

import csv
import time
import datetime
import timeit  # For timing function
from random import randint

startTime = time.time()  # Get the time at the start of the program


# Function to initialize data files by the current datetime
def createFiles():
    now = datetime.datetime.now()
    for i in range(4):
        # Generate the file name: a0_YYYY-MM-DD_HH:mm:SS
        file_name_init = "data/a"+str(i)+"_"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"_"+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+".csv"
        # Open and Close the file to create it
        f = open(file_name_init, "w+")
        f.close()
    return now


# Function to read the data and save to the csv
#   pinNumber - The pin off which to read the data
#   now - The datetime when the save file was instantiated
def readValue(pinNumber, now):
    data = [0]*2
    # Get the current datetime in a readable string: YYYY-MM-DD HH:mm:SS:ssssss
    data[0] = str(datetime.datetime.now())
    # Read the specified ADC channel using the previously set gain value
    data[1] = str(randint(0, 32767))

    # file is called based on pin number
    fileName = "data/a"+str(i)+"_"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"_"+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+".csv"
    # Open the file and write the data to the csv
    with open(fileName, "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
        writer.writerow(data)
    print(str(data) + ": pin"+str(pinNumber))
    return


now_time = createFiles()  # Initialize the first set of files and store time
intervals = [1, 2, 1, 4]  # Internals before we get data again
previousTime = [0]*4  # Last time data was taken

# We run the function in an infinite loop to continually take data
while True:
    # Get the time since the start of the program
    currentTime = round(time.time() - startTime, 2)

    # Loop through each of the pins and check if it has been enough time to
    # take another measurement. If so, take one
    for i in range(4):
        if (currentTime - previousTime[i] > intervals[i]):
            previousTime[i] = round(time.time() - startTime, 2)
            readValue(i, now_time)
