# [Weather Thingy](https://medium.com/@bdettmer/displaying-weather-on-a-32x16-led-matrix-ce9281dc67a9)

Displays current DarkSky weather to 32x16 RGB LED Grid

## Setup
- get a free [Dark Sky API key](https://darksky.net/dev)
- add network name and password, Dark Sky API key, and GPS LAT and LONG coordinates to `recipe.xml` between the ** symbols
- flash SD card using recipe.xml pibakery http://www.pibakery.org/download.html
- make sure the Pi has an uninterrupted power supply the first time it boots up, so it can install and set up everything it needs to
- `ssh pi@weatherpi.local`, password will be `blueberry` unless you change it
- connect the pi to the MPC1073, connect the MPC1073 to the HUB75 LED matrix [like so](https://github.com/redSlug/weather-reporter/blob/master/images/hw.jpg) 
- schedule [cronjob](https://www.raspberrypi.org/documentation/linux/usage/cron.md) to get weather every two minutes, and render upon boot
```console
*/2 * * * * /home/pi/weather-reporter/get_weather.sh >> /home/pi/weather-reporter/log
@reboot /home/pi/weather-reporter/show_weather.sh >> /home/pi/weather-reporter/log
```

## BOM
- Raspberry Pi 
- MPC1073 and CR1220 battery
- flash card, and card reader / writer
- 32x16 LED matrix with ribbon

## Thank You
- [Henner Zeller](https://github.com/hzeller/rpi-rgb-led-matrix) for sharing your sample code
- [Ari Zilnik](https://medium.com/@azilnik) for helping with soldering and graphics
- [Janice Shiu](https://github.com/contrepoint) for thinking of a cool name
- [Powered by Dark Sky](https://darksky.net/poweredby/)
