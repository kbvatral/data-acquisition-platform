# Script to simulate reading analog input from the ADS1x15 and save
# it to an influx database
# Author: Caleb Vatral

import time
import datetime
import threading
import timeit  # For timing function
from random import randint
import influxdb
from influxdb import InfluxDBClient
import os
from delorean import Delorean

import requests
requests.packages.urllib3.disable_warnings()  # Supress ssl certificate warning

startTime = time.time()  # Get the time at the start of the program
thread_counter = 0  # A counter to represent the thread ID on the data dumps

# Variable Declarations

# Influxdb Connection
host = '10.128.189.163'
port = 8086
ssl = True
user = 'root'
password = 'ENCLions'
dbname = 'mydb'
client = InfluxDBClient(host, port, user, password, dbname, ssl)

# A list of influxdb measurements. The indecies of the list correspond to the
# pin number on the ADC
measurements = []
measurements.append('test_a0')
measurements.append('test_a1')
measurements.append('test_a2')
measurements.append('test_a3')


# Function to initialize data files by the current datetime
def createFiles():
    now = datetime.datetime.now()
    for i in range(4):
        # Generate the file name: a0_YYYY-MM-DD_HH:mm:SS
        file_name_init = "data/a"+str(i)+"_"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"_"+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+".txt"
        # Open and Close the file to create it
        f = open(file_name_init, "w+")
        f.close()
    return now


# Function to read the data and save to the csv
#       pinNumber - The pin off which to read the data
#       now - The datetime when the save file was instantiated
def readValue(pinNumber, now):
    data = [0]*2
    # Get the UTC time in nanoseconds since the epoch
    data[0] = str(int(Delorean().epoch * 1000000000))
    # Read the specified ADC channel using the previously set gain value
    data[1] = str(randint(0, 32767))

    data_string = measurements[pinNumber] + ' ' + 'value=' + data[1] + ' ' + data[0] + '\n'
    # file is called based on pin number
    fileName = "data/a"+str(i)+"_"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"_"+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+".txt"
    # Open the file and write the data
    with open(fileName, "a") as text_file:
        text_file.write(data_string)
    # print(str(data) + ": pin"+str(pinNumber))
    return


# Define the clss for multithreading data dumps
class dataDump(threading.Thread):
    def __init__(self, threadID, time_stamp):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.time_stamp = time_stamp

    def run(self):
        dataDump_function(self.time_stamp)


# Function to do the actual data dump called by the dataDump thread class
#       time_stamp - the time stamp of the file to be proccessed
def dataDump_function(time_stamp):
    # We are looping over all the files in the data folder except the current
    # data dump files. This allows us to upload data from any previous data
    # dump period, if there was a problem trying to upload it the first time
    for fileName in os.listdir("data/"):
        # Filter out the files from the current data dump period
        striped_name = fileName[3:]
        striped_name = striped_name[:-4]
        formatted_time = str(time_stamp.year)+"-"+str(time_stamp.month)+"-"+str(time_stamp.day)+"_"+str(time_stamp.hour)+":"+str(time_stamp.minute)+":"+str(time_stamp.second)
        if striped_name == formatted_time:
            continue

        # Open the file and read the data
        full_file_name = "data/" + fileName
        with open(full_file_name) as text_file:
            reader = text_file.read().splitlines()
            try:
                client.write_points(reader, protocol='line')
                os.remove("data/" + fileName)
                # print(reader)
                # print(type(reader))
            except influxdb.exceptions.InfluxDBServerError:
                continue
    print("Done")


# ========== Main Function ========== #

now_time = createFiles()  # Initialize the first set of files and store time
intervals = [0.01, 2, 1, 4, 10]  # Internals (sec) before we get data again
previousTime = [0]*5  # Last time data was taken

# We run the function in an infinite loop to continually take data
while True:
    # Get the time since the start of the program
    currentTime = round(time.time() - startTime, 2)

    # Loop through each of the pins and check if it has been enough time to
    # take another measurement. If so, take one
    for i in range(4):
        if (currentTime - previousTime[i] > intervals[i]):
            previousTime[i] = round(time.time() - startTime, 3)
            readValue(i, now_time)

# Check if we are ready for a data dump
    if (currentTime - previousTime[4] > intervals[4]):
        previousTime[4] = currentTime
        thread_counter += 1
        now_time = createFiles()
        dataDump(thread_counter, now_time).start()
