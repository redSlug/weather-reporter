from darksky import forecast
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import requests
import os
from dotenv import load_dotenv, find_dotenv
from collections import namedtuple
import datetime
from get_calendar import write_calendar_data

from train_info import TrainInfo

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

WeatherData = namedtuple('WeatherData', 'currently_icon, summary, temp, chance_rain')


class DarkSkyWeather:
    def __init__(self, api_key, lat, long):
        self.api_key = api_key
        self.lat = lat
        self.long = long

    def get_weather(self):
        location = forecast(self.api_key, self.lat, self.long)
        currently_icon = location.currently.icon.replace('-', '_')
        uv = None           # location.currently.uvIndex
        humidity = None     # int(location.currently.humidity * 100)
        low = int(location.daily.data[0].apparentTemperatureLow)
        high = int(location.daily.data[0].apparentTemperatureHigh)
        chance_rain = int(location.currently.precipProbability * 100)
        summary = location.hourly.summary + ' '
        temp = '{low}-{high}F '.format(low=low, high=high)

        if humidity:
            summary += 'humid:{humid}% '.format(humid=humidity)
        if uv:
            summary += 'uv:{uv} '.format(uv=uv)
        if chance_rain:
            summary += 'rain:{rain}% '.format(rain=chance_rain)
        return WeatherData(currently_icon=currently_icon,
                           summary=summary,
                           temp=temp,
                           chance_rain=chance_rain)


class BannerMaker:
    def __init__(self, banner_id):
        self.banner_id = banner_id

    def replace_banner(self, weather, calendar_text=' ', message_text=' ',
                       train_text=''):
        currently_icon = weather.currently_icon

        now = datetime.date.strftime(datetime.datetime.now(), "%a %-I:%M%p")

        summary = now + ' '
        if train_text:
            summary += train_text + '~ '

        summary += weather.summary
        summary += weather.temp

        font_size_in_points = 9
        font = ImageFont.truetype(FONTS_DIR + 'led.ttf', font_size_in_points)
        font_size = font.getsize(summary)
        print(
            'summary: {}, font size: {} calendar_text: {}, message_text{}'.format(
                summary, font_size, calendar_text, message_text))
        summary_img = Image.new('RGB', font_size)
        draw = ImageDraw.Draw(summary_img)
        draw.text((0, 0), summary, font=font)
        enh = ImageEnhance.Contrast(summary_img)
        enh.enhance(1.99).save(GENERATED_DIR + 'enh.ppm')

        enhanced_summary = Image.open(GENERATED_DIR + 'enh.ppm')

        current_img = Image.open(
            '{}{}'.format(IMAGES_DIR, weather_files[currently_icon]))

        if message_text:
            font_size = font.getsize(message_text)
            message_img = Image.new('RGB', font_size)
            message_draw = ImageDraw.Draw(message_img)
            message_draw.text((0, 0), message_text, font=font,
                              fill='GreenYellow')
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

        size = (
        enhanced_summary.width + current_img.width + enhanced_calendar.width + message_width,
        16)

        banner = Image.new('RGB', size)
        banner.paste(enhanced_summary, (0, 4))
        banner.paste(current_img, (enhanced_summary.width, 0))

        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
        for i, color in enumerate(colors):
            stripe = Image.new('RGB', (enhanced_summary.width, 1), color)
            banner.paste(stripe, (0, i if i < 3 else i + 10))

        banner.paste(enhanced_calendar,
                     (enhanced_summary.width + current_img.width, 4))

        if message_text:
            banner.paste(enhanced_message, (
            enhanced_summary.width + current_img.width + enhanced_calendar.width,
            4))

        led_output_file_name = 'weather{}.ppm'.format(self.banner_id)
        web_output_file_name = 'display{}.jpg'.format(self.banner_id)

        banner.save(GENERATED_DIR + led_output_file_name)
        banner.save(STATIC_DIR + led_output_file_name)
        self.exportJpg(GENERATED_DIR + led_output_file_name,
                       STATIC_DIR + web_output_file_name)

    @staticmethod
    def exportJpg(ppmFilePath, outputFilePath):
        im = Image.open(ppmFilePath)
        im.save(outputFilePath)


def get_calendar_text():
    try:
        with open(CALENDAR_DATA) as f:
            l = f.readline()
            return l.rstrip()
    except:
        print('unable to get calendar data')
        return ' '  # hack to avoid div by zero when creating img


def get_message_text():
    # TODO connect to db directly maybe?? or make it port 5000 if local debug
    # can't return empty string, TODO div by zero when creating img
    try:
        url = 'http://localhost:{}/matrix/api/message'.format(
            os.environ['APP_PORT'])
        result = requests.get(url=url)
        message = result.json().get('messages')
        if not message:
            return ' ... '

        return ' ' + message[-1]['message']
    except:
        return " Let's hack! You can submit a PR dynamicdisplay.recurse.com "


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    write_calendar_data()

    DARK_SKY_API_KEY = os.environ['DARK_SKY_API_KEY']
    LAT = os.environ['LAT']
    LONG = os.environ['LONG']
    dsw = DarkSkyWeather(api_key=DARK_SKY_API_KEY, lat=LAT, long=LONG)

    now = datetime.datetime.now()
    weather = dsw.get_weather()
    message_text = get_message_text()
    calendar_text = get_calendar_text()

    print('message_text={}#'.format(message_text))
    print('calendar_text={}#'.format(calendar_text))

    rc_banner = BannerMaker(banner_id='')

    rc_banner.replace_banner(
        weather=weather,
        calendar_text=calendar_text,
        message_text=message_text
    )

    home_banner = BannerMaker(banner_id='_2')

    home_banner.replace_banner(
        weather=weather
    )
