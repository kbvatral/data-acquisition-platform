# Script to simulate reading analog input from the ADS1x15 and save
# it to a csv file
# Author: Caleb Vatral

import csv
import time
import datetime
import threading
import timeit  # For timing function
from random import randint
import MySQLdb

startTime = time.time()  # Get the time at the start of the program
thread_counter = 0  # A counter to represent the thread ID on the data dumps


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
#       pinNumber - The pin off which to read the data
#       now - The datetime when the save file was instantiated
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
    mydb = MySQLdb.connect(host='10.128.189.163', user='root', passwd='ENCLions', db='sensor_test')
    cursor = mydb.cursor()

    for i in range(4):
        # file is called based on pin number
        fileName = "data/a"+str(i)+"_"+str(time_stamp.year)+"-"+str(time_stamp.month)+"-"+str(time_stamp.day)+"_"+str(time_stamp.hour)+":"+str(time_stamp.minute)+":"+str(time_stamp.second)+".csv"
        # Open the file and write the data to the csv
        with open(fileName) as csv_file:
            reader = csv.reader(csv_file, delimiter=',', lineterminator='\n')
            for row in reader:
                timeStamp = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
                date = timeStamp.date()
                time = timeStamp.time()
                cursor.execute('INSERT INTO test_sensor_data(platform_id, data_date, data_time, numeric_data ) VALUES(%s, %s, %s, %s)', (1, date, time, row[1]))

    mydb.commit()
    cursor.close()
    print("Done")


# ========== Main Function ========== #

now_time = createFiles()  # Initialize the first set of files and store time
intervals = [1, 2, 1, 4, 10]  # Internals (sec) before we get data again
previousTime = [0]*5  # Last time data was taken

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

# Check if we are ready for a data dump
    if (currentTime - previousTime[4] > intervals[4]):
        previousTime[4] = currentTime
        thread_counter += 1
        dataDump(thread_counter, now_time).start()
        now_time = createFiles()
