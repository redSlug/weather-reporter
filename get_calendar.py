from subprocess import Popen, PIPE
import re
import datetime
import sys
import requests

def getEventsInFuture(calendar_token):
    calendarURL = 'https://www.recurse.com/calendar/events.ics?token=' + calendar_token
    result = requests.get(url=calendarURL)
    output = result.text
    titles = []
    output = output.split("\n")
    now = datetime.datetime.now()
    dateForEvent = None
    isActiveEvent = False
    for o in output:
        if (isActiveEvent) and (o.startswith("SUMMARY")) and (not "office hours" in o.lower()):
            o = o.replace("SUMMARY:","")
            titles.append((o, dateForEvent.strftime('%H:%m')))
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
    eventDictionary = {}
    for summary, date in titles:
        if summary not in eventDictionary:
            eventDictionary[summary] = date
    
    return eventDictionary



if __name__ == "__main__":
    print(getEventsInFuture(sys.argv[1]))
