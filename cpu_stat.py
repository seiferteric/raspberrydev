#!/usr/bin/python3

import psutil
import time
import signal
import sys
import RPi.GPIO as GPIO

#Call this when program exits
def cleanup(signal, frame):
  print("Cleaning up!")
  GPIO.cleanup()
  sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
print("Press Ctrl+C to exit")

#Using BCM Mappings, maybe change this later
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Set the (BCM) channels you want to use for your LED display
#The order matters
chan = [4, 5, 6, 12, 13, 16, 17, 18, 19, 20]

#Set to output mode, at LOW level
GPIO.setup(chan, GPIO.OUT, initial=GPIO.LOW)


while True:
  time.sleep(0.08)
  cpu = psutil.cpu_percent()
  #Figure outhow many LEDs should be lit based on cpu usage and number of LEDs we are configured to use.
  count = round(len(chan)*(cpu/100.0))
  for i,c in enumerate(chan):
    if i < count:
      if GPIO.input(c) != GPIO.HIGH:
        GPIO.output(c, GPIO.HIGH)
    else:
      if GPIO.input(c) != GPIO.LOW:
        GPIO.output(c, GPIO.LOW)


