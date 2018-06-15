from darksky import forecast
from sys import argv
from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageFilter
import requests
import datetime

API_KEY = argv[1]
LAT = argv[2]
LONG = argv[3]

weather_files = dict(
    clear_day='dark_sun.ppm',
    clear_night='clear_night.ppm',
    rain='rainy.ppm',
    snow='snowflake.ppm',
    sleet='rainy.ppm',
    wind='wind1.ppm',
    fog='cloud.ppm',
    cloudy='cloud.ppm',
    partly_cloudy_day='partly_cloudy_day.ppm',
    partly_cloudy_night='partly_cloudy_night.ppm'
)


def replace_banner(currently_icon, summary):
    summary += get_calendar_data()
    try:
        msg = get_message_data()
        if len(msg) < 30:
            summary += msg
    except:
        pass
    font_size_in_points = 9
    font = ImageFont.truetype('fonts/led.ttf', font_size_in_points)
    font_size = font.getsize(summary)
    print('summary: {}, font size: {}'.format(summary, font_size))
    summary_img = Image.new('RGB', font_size)
    draw = ImageDraw.Draw(summary_img)
    draw.text((0, 0), summary, font=font)
    enh = ImageEnhance.Contrast(summary_img)
    enh.enhance(1.99).save('images/enh.ppm')

    enhanced_summary = Image.open('images/enh.ppm')

    current_img = Image.open('images/{}'.format(weather_files[currently_icon]))

    size = (enhanced_summary.width + current_img.width, 16)
    banner = Image.new('RGB', size)
    banner.paste(enhanced_summary, (0, 4))
    banner.paste(current_img, (enhanced_summary.width, 0))

    #colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
    #for i, color in enumerate(colors):
    #    stripe = Image.new('RGB', (enhanced_summary.width, 1), color)
    #    banner.paste(stripe, (0, i if i < 3 else i + 10))

    banner.save('images/weather.ppm')
    exportJpg('images/weather.ppm', 'server/static/display.jpg')


def get_calendar_data():
    try:
        with open('calendar_data') as f:
                l = f.readline()
                if len(l) > 120:
                    l = l[:120]
                return l.rstrip()
    except:
        print('unable to get calendar data')
        return ''


def get_message_data():
    messageURL = 'http://localhost:5000/matrix/api/message'
    result = requests.get(url=messageURL)
    messageData = result.json().get('messages')[-1]['message']
    date = result.json().get('messages')[-1]
    date = date['created']
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.now()
    if (not ((now-date).total_seconds()) >= 360 ):
        return messageData
    else:
        return ""


def get_weather():
    location = forecast(API_KEY, LAT, LONG)
    currently_icon = location.currently.icon.replace('-', '_')
    uv = location.currently.uvIndex
    humidity = int(location.currently.humidity * 100)
    summary = location.hourly.summary
    low = int(location.daily.data[0].apparentTemperatureLow)
    high = int(location.daily.data[0].apparentTemperatureHigh)
    chance_rain = int(location.currently.precipProbability * 100)
    summary ='{low}-{high}F humid:{humid}% uv:{uv} rain:{rain}% '.format(low=low, high=high, uv=uv, humid=humidity, rain=chance_rain) + summary
    return dict(currently_icon=currently_icon, summary=summary)


def exportJpg(ppmFilePath,outputFilePath):
    im = Image.open(ppmFilePath)
    im.save(outputFilePath)


if __name__ == '__main__':
    replace_banner(**get_weather())
