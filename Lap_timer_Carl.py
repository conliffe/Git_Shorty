#!/usr/bin/env python3
########################################################################
# Filename    : lapTimer_Carl.py
# Description : Reports on the time lapsed between detections of a sensor.
# For this test code a push button will be the sensor for the lap in
# adition to the two types of IR sensor configuration.  The circuit will
# flash an LED on each lap detection, and green LED to #  indicate the
# fastest lap.  The schematic name that coresponds to this code is
# "Lap_Timer_Counter.sch" drans in KiCad
# 2 Buttons - one to reset timings and one to display fastest lap.
# There is a countdown christmas tree to start the race.
# Does not use adafruit library to display lap times on 7 segment, 4 digit
#  display yet
#
# Author      : Carl Conliffe based on Scalextric Timer code
# Modification: 2 Febuary 2020
########################################################################

###### List of variables ###########
# fastestLap
# channel
# countDown1, 2, 3, 4, 5
# currentTime
# fastestLapInString
# getFastestLap
# greenled
# i
# lapNumber
# lapSensor1
# lapSensor2
# lapSensorTest
# lapTime
# lapTimeInString
# previousTime
# raceFinishTime
# raceFinishTimeFormatted
# raceStartTime
# raceStartTimeFormatted
# redLed
# reset
# startRace
# time
####################################

###### List of funcions ############
# display(time)
# displayFastestLap(channel)
# fastestLapLEDflash
# lapDetect()
# logDataToCSV()
# newLap(channel)
# reset(channel)
# startSequence()
####################################


# Import libraries
import RPi.GPIO as GPIO
import time
#from Adafruit_7Segment import SevenSegment

# Set i2c address for display, and display zeros
#segment = SevenSegment(address=0x70)
#segment.writeDigit(0, 0)
#segment.writeDigit(1, 0)
#segment.writeDigit(3, 0)
#segment.writeDigit(4, 0)

# Configure the Pi to use the BCM pin names
GPIO.setmode(GPIO.BCM)

# pins used for the switches, IR diodes as sensor and LEDs
reset = 16          # GPIO16 pin 36, lap and fastest lap reset
lapSensor1= 4       # GPIO4 pin 7, This is for the break IR beam sensor
lapSensor2= 5       # GPIO5 pin 29, This is for the reflective IR sensor
lapSensorTest= 6    # GPIO6 pin 31, This is for the push button lap trigger
getFastestLap = 17  # GPIO17 pin 11, This is a push button to display fastest lap
startRace = 27      # GPIO27 pin 13, This is a push button to start the race
redLed = 22         # GPIO22 pin 15, Lap indicator
greenLed = 26       # GPIO26 pin 37, Fastest lap indicator
countDown5 = 25     # GPIO25 pin 22, countdown LEDs on bar LED
countDown4 = 23     # GPIO23 pin 16, countdown LEDs on bar LED
countDown3 = 24     # GPIO24 pin 18, countdown LEDs on bar LED
countDown2 = 12     # GPIO12 pin 32, countdown LEDs on bar LED
countDown1 = 13     # GPIO13 pin 33, countdown LEDs on bar LED

# configure outputs for LED
print('The LEDs are being configured.  Red for lap detection and green for fasted lap')
GPIO.setwarnings(False)
GPIO.setup(redLed, GPIO.OUT)      # Red LED channel 22
GPIO.setup(greenLed, GPIO.OUT)    # Green LED channel 26
GPIO.setup(countDown5, GPIO.OUT)  # LED bar LED5 channel 25
GPIO.setup(countDown4, GPIO.OUT)  # LED bar LED4 channel 23
GPIO.setup(countDown3, GPIO.OUT)  # LED bar LED3 channel 24
GPIO.setup(countDown2, GPIO.OUT)  # LED bar LED2 channel 12
GPIO.setup(countDown1, GPIO.OUT)  # LED bar LED1 channel 13

# Configure inputs using event detection, pull up resistors
print('Configuring the detection input channels for the GPIO')
GPIO.setup(reset, GPIO.IN, pull_up_down=GPIO.PUD_UP)          # Reset signal channel GPIO16 pin 36
GPIO.setup(lapSensorTest, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # lapSensorTest switch channel GPIO6 pin 31
GPIO.setup(lapSensor1, GPIO.IN, pull_up_down=GPIO.PUD_UP)     # lapSensor1 channel GPIO4 pin 7
GPIO.setup(lapSensor2, GPIO.IN, pull_up_down=GPIO.PUD_UP)     # lapSensor2 channel GPIO5 pin 39
GPIO.setup(getFastestLap, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # getFastestLap channel GPIO17 pin 11
GPIO.setup(startRace, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # startRace channel GPIO27 pin 13

# Switch off LEDs
print('Switching all LEDs off')
GPIO.output(redLed, False)
GPIO.output(greenLed, False)

# Define new variables for lap counting and remembering fastest lap time
lapNumber = 0
fastestLap = 9999

# Funtion to run the start sequence countdown
def startSequence():
    GPIO.output(countDown5, False)  #Turn off LED
    GPIO.output(countDown4, False)  #Turn off LED
    GPIO.output(countDown3, False)  #Turn off LED
    GPIO.output(countDown2, False)  #Turn off LED
    GPIO.output(countDown1, False)  #Turn off LED
    print('Gentlemen start your engines')
    time.sleep(1)
    GPIO.output(countDown5, True)  #Turn on LED
    print('Five!')
    time.sleep(1)
    GPIO.output(countDown4, True)  #Turn off LED
    print('Four!')
    time.sleep(1)
    GPIO.output(countDown3, True)  #Turn off LED
    print('Three!')
    time.sleep(1)
    GPIO.output(countDown2, True)  #Turn off LED
    print('Two!')
    time.sleep(1)
    GPIO.output(countDown1, True)  #Turn off LED
    print('One!')
    time.sleep(1)
    GPIO.output(countDown5, False)  #Turn off LED
    GPIO.output(countDown4, False)  #Turn off LED
    GPIO.output(countDown3, False)  #Turn off LED
    GPIO.output(countDown2, False)  #Turn off LED
    GPIO.output(countDown1, False)  #Turn off LED
    print('GO!!!!')
    raceStartTime = time.localtime()     # This returns the local start time of the race
    raceStartTimeFormatted = time.strftime("%a, %d %b %Y %H:%M:%S %Z ", raceStartTime)
    print("\nOfficial Race Start Time = ", raceStartTimeFormatted)

# Function to flash red LED once
def lapDetect():
#    print('Lap was detected. Flashing a Red LED')
#    print('Red LED ON')
    GPIO.output(redLed, True)
    time.sleep(0.1)
#    print('Red LED off')
    GPIO.output(redLed, False)

# Function to repeatedly flash green LED when a fastest lap occurs
def fastestLapLEDflash():
    for i in range(0,5):
#        print('Green LED ON')
        GPIO.output(greenLed, True)
        time.sleep(0.1)
#        print('Green LED OFF')
        GPIO.output(greenLed, False)
        time.sleep(0.1)
    print('You just completed your fastest lap!')

# Function to write lap time to the 7 Segment display
def display(time):
    print('This is value for lap time that gets displayed in the 7 segment display')
    print('Your lap time = ', "%.3f" %time, ' seconds')
#    segment.writeDigit(1, int(str(time)[0]))
#    segment.setColon(True)
#    segment.writeDigit(3, int(str(time)[2]))
#    segment.writeDigit(4, int(str(time)[3]))

# Function to open, create and configure .csv file
def openCSVFile():
    print("Creating .csv file")
    with open('raceData.csv', mode='a') as race_data:
        data_writer = csv.writer(race_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['This is data for: ', raceNumber])
        data_writer.writerow(['Lap #', 'Lap Time (sec)', 'Fastest Lap(sec)'])

# Function to write data to .csv file
def writeDatatoCSVFile():
    with open('raceData.csv', mode='a') as race_data:
        data_writer = csv.writer(race_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fastestLapInString = str(fastestLap)        # float -> str
        lapNumberInString = str(lapNumber)          # float -> str
        lapTimeInString = str(lapTime)              # float -> str
        data_writer.writerow([lapNumberInString, lapTimeInString, bestLapInString])

# Function to determine what actions to take on new lap detection
def newLap(channel):
    lapDetect()
    global lapNumber       # This variable is the lap count.  May want to make this user inputable.
    global previousTime    # This is the previous time or time at start of lap
    global currentTime     # This is the current time or time at end of lap
    global lapTime         # This is the current lap time
    global fastestLap      # This is the fasted lap time
    if lapNumber < 1:       # This executes on the first lap only to set the start time
        previousTime = time.time()    # This is the start time and the time at the begining of lap #1
        print("Lap: " + str(lapNumber))
        lapNumber += 1   # Increments the lap counter
    else:
        currentTime = time.time()          # Grabs the current time
        lapTime = currentTime - previousTime    # Current time minus previous time gets you the current lap time.
        print(' ')
        print("Lap: " + str(lapNumber), " Lap time = %.3f" % lapTime, ' seconds') # Prints the current lap number and lap time
        previousTime = currentTime     # This sets the lap end time to be the start time of the next lap
        lapNumber += 1   # Increments the lap counter
        if lapTime < fastestLap:
            print('New fastest lap!! Lap Time = ' "%.3f" % lapTime, ' seconds') # Prints the fasted lap time when it happens
            fastestLapLEDflash() # Calls function that lights the green LED ofr fastest lap indicator
            fastestLap = lapTime    # Serts a new fasted lap standard to hit
        #if lapTime < 10:   # DOT SURE WHY IT ONLY CALLS & SEGMENT WHEN LAP TIME IS LESS THAN 10 SEC
        display(lapTime)    # Calls function that sisplays lap time on 7 Segment display

# Function to reset lap times and counts
def reset(channel):
    global count
    global fastestLap
    lapNumber = 0
    fastestLap = 99999
    print('Lap times reset to zero')
#    segment.writeDigit(0, 0)
#    segment.writeDigit(1, 0)
#    segment.writeDigit(3, 0)
#    segment.writeDigit(4, 0)

# Function to write the fastest lap time to the display
def displayFastestLap(channel):
    global fastestLap
    print('Displaying fastest lap to 7 segment display.  Fastest lap = ' "%.3f" % fastestLap)
#    segment.writeDigit(1, int(str(fastestLap)[0]))
#    segment.setColon(True)
#    segment.writeDigit(3, int(str(fastestLap)[2]))
#    segment.writeDigit(4, int(str(fastestLap)[3]))

startSequence()   # Calls the start sequence
GPIO.add_event_detect(16, GPIO.FALLING, callback=reset, bouncetime=200)  # This is reset
GPIO.add_event_detect(6, GPIO.FALLING, callback=newLap, bouncetime=2000) # The is new lap test button
GPIO.add_event_detect(17, GPIO.FALLING, callback=displayFastestLap, bouncetime=200) # This is display fasted lap
GPIO.add_event_detect(4, GPIO.FALLING, callback=newLap, bouncetime=200)  # The is new lap Break Beam Detection
GPIO.add_event_detect(5, GPIO.FALLING, callback=newLap, bouncetime=200)  # The is new lap Reflective Detection


try:
    print "Waiting racer to push "Start" buttong"
    GPIO.wait_for_edge(27, GPIO.FALLING, bouncetime=2000)   # This is the start buttong being pressed
    print('The Race has started.')
    while True:
        time.sleep(0.01)
        pass    # Does nothing.  Kind of like a no op

finally:
    print('Done!!  The Race is over.')
    raceFinishTime = time.localtime()     # This returns the local finish time of the race
    raceFinishTimeFormatted = time.strftime("%a, %d %b %Y %H:%M:%S %Z ", raceFinishTime)
    print("\nOfficial Race Finish Time = ", raceFinishTimeFormatted)
#    segment = SevenSegment(address=0x70)
    GPIO.cleanup()

### This might be a better way to do the previous try/Except ###
# try:
#    print "Waiting for falling edge on port TBD"
#    GPIO.wait_for_edge(TBD GPIO port #, GPIO.FALLING)
#    print('Done!!  The Race is over.')
#
#except KeyboardInterrupt:
#    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
#    print('Done!!  The Race is over.')
#print('Done!!  The Race is over.')
#GPIO.cleanup()           # clean up GPIO on normal exit
#################################################################
