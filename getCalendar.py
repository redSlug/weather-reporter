from subprocess import Popen, PIPE
import re
import datetime
import sys

p = Popen(['curl', sys.argv[1]], stdin=PIPE, stdout=PIPE, stderr=PIPE)
output = p.communicate()
titles = []
output = output[0].split("\n")
now = datetime.datetime.now()
dateForEvent = None
isActiveEvent = False

for o in output:
    if (isActiveEvent) and (o.startswith("SUMMARY")) and (not "office hours" in o.lower()):
        o = o.replace("SUMMARY:","")
        titles.append((o, dateForEvent.strftime('%H:%m')))
        #titles.append((o, (str(dateForEvent).split()[1])[0:-3]))
        isActiveEvent = False

    else:
        '''when we find the start time'''
        if o.startswith("DTSTART"):
            dateLine =  re.search('^DTSTART.*:(.*)', o)
            dateLine = dateLine.group(1)[:-1]
            cal_time = datetime.datetime.strptime(dateLine, "%Y%m%dT%H%M%S")
            if now < cal_time < now + datetime.timedelta(hours=3):
                isActiveEvent = True
                dateForEvent = cal_time

titles.sort(key=lambda x:x[1])
titles = [(summary.rstrip(),time) for summary,time in titles]
uniqueTitleList = {}
for summary, date in titles:
    if summary not in uniqueTitleList:
        uniqueTitleList[summary] = date
        
for u in uniqueTitleList.items():
    print u