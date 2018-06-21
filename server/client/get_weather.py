from darksky import forecast
from sys import argv
from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageFilter
import requests
import datetime
import os

API_KEY = os.environ['DARK_SKY_API_KEY']
LAT = os.environ['LAT']
LONG = os.environ['LONG']

IMAGES_DIR = 'client/images/'
FONTS_DIR = 'client/fonts/'
GENERATED_DIR = 'client/generated/'
STATIC_DIR = 'static/'
CALENDAR_DATA = 'client/generated/calendar_data'

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

    calendar_text = get_calendar_data()
    calendar_text+= "  "
    message_text = ""
    try:
        msg = get_message_data()
        if len(msg) < 30:
            message_text += msg
    except:
        pass
    font_size_in_points = 9
    font = ImageFont.truetype(FONTS_DIR + 'led.ttf', font_size_in_points)
    font_size = font.getsize(summary)
    print('summary: {}, font size: {}'.format(summary, font_size))
    summary_img = Image.new('RGB', font_size)
    draw = ImageDraw.Draw(summary_img)
    draw.text((0, 0), summary, font=font)
    enh = ImageEnhance.Contrast(summary_img)
    enh.enhance(1.99).save(GENERATED_DIR + 'enh.ppm')

    enhanced_summary = Image.open(GENERATED_DIR + 'enh.ppm')

    current_img = Image.open('{}{}'.format(IMAGES_DIR, weather_files[currently_icon]))

    if message_text:
       font_size = font.getsize(message_text)
       message_img = Image.new('RGB', font_size)
       message_draw = ImageDraw.Draw(message_img)
       message_draw.text((0, 0), message_text, font=font, fill='GreenYellow')
       enh_message = ImageEnhance.Contrast(message_img)
       enh_message.enhance(1.99).save(GENERATED_DIR + 'messagetext.ppm')
       enhanced_message = Image.open(GENERATED_DIR + 'messagetext.ppm')
       message_width = enhanced_message.width
    else:
       message_width = 0

    font_size = font.getsize(calendar_text)
    calendar_img = Image.new('RGB', font_size)
    calendar_draw = ImageDraw.Draw(calendar_img)
    calendar_draw.text((0, 0), calendar_text, font=font, fill='cyan')
    enh_calendar = ImageEnhance.Contrast(calendar_img)
    enh_calendar.enhance(1.99).save(GENERATED_DIR + 'calendartext.ppm')

    enhanced_calendar = Image.open(GENERATED_DIR + 'calendartext.ppm')


    size = (enhanced_summary.width + current_img.width + enhanced_calendar.width + message_width, 16)

    banner = Image.new('RGB', size)
    banner.paste(enhanced_summary, (0, 4))
    banner.paste(current_img, (enhanced_summary.width, 0))

    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
    for i, color in enumerate(colors):
       stripe = Image.new('RGB', (enhanced_summary.width, 1), color)
       banner.paste(stripe, (0, i if i < 3 else i + 10))
    banner.paste(enhanced_calendar, (enhanced_summary.width + current_img.width, 4))

    if message_text:
       banner.paste(enhanced_message, (enhanced_summary.width + current_img.width + enhanced_calendar.width, 4))

    banner.save(GENERATED_DIR + 'weather.ppm')
    banner.save(STATIC_DIR + 'weather.ppm')
    exportJpg(GENERATED_DIR + 'weather.ppm', STATIC_DIR + 'display.jpg')


def get_calendar_data():
    try:
        with open(CALENDAR_DATA) as f:
                l = f.readline()
                return l.rstrip()
    except:
        print('unable to get calendar data')
        return ''


def get_message_data():
    messageURL = 'http://localhost:5000/matrix/api/message'
    result = requests.get(url=messageURL)
    data = result.json().get('messages')[-1]
    message, author = data['message'], data['author']
    if author:
        return author + ": " + message + " "
    return message + " "


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