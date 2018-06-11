import sys  
import os
import re

filepath = 'log'  
with open(filepath) as fp:  
    line = fp.readline()
    cnt = 1

    setOfTimestamps = []
   
    previousTimeStamp = 0
    previousLine = ""
    while line:
        if "Jun" in line:
            time = line.split()[3]
            time = time.split(":")
            time = [int(c) for c in time]
            time = (time[0]*360) + (time[1]*60 )+ (time[2])
            line = line.replace (".","")

            if not(time - previousTimeStamp <=110):
                print previousLine.rstrip() + " <------> "+ line.rstrip()

            previousTimeStamp = time
            previousLine = line
            setOfTimestamps.append(time)



        line = fp.readline()
        cnt += 1
