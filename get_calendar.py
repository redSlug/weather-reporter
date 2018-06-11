import re
import datetime
import sys
import requests

SUMMARY_LIMIT = 25
CALENDAR_DATA_LIMIT = 120

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
    event_dictionary = {}
    for summary, date in titles:
        if len(summary) > SUMMARY_LIMIT:
            summary_words = summary.split()
            short_summary = ''
            for word in summary_words:
                if len(short_summary + word) + 4 > SUMMARY_LIMIT:
                    break
                short_summary += ' ' + word
            summary = short_summary + '...'

        if summary not in event_dictionary:
            event_dictionary[summary] = date
            
    event_data = ' '
    for (title, date) in event_dictionary.items():
        if len(title + date) > CALENDAR_DATA_LIMIT:
            continue

        event_data += '{title} {date}, '.format(title=title, date=date)
    event_data = event_data[:-2]

    if len(event_dictionary):
        event_data = ' Upcoming: ' + event_data
    
    with open('calendar_data', 'w') as f:
        f.write(event_data)

if __name__ == "__main__":
    getEventsInFuture(sys.argv[1])
