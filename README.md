# Weather Thingy

[Displays current DarkSky weather to 32x16 RGB LED Grid](https://medium.com/@bdettmer/displaying-weather-on-a-32x16-led-matrix-ce9281dc67a9)

## Setup
- get a free [Dark Sky API key](https://darksky.net/dev)
- add network name and password between the `**` symbols, removing the `**` symbols
- flash SD card to full raspian using [PiBakery](http://www.pibakery.org/download.html) and `recipe.xml` 
- make sure the Pi has an uninterrupted power supply the first time it boots up, so it can install and set up everything it needs to, then you can `ssh pi@weatherpi.local`, password will be `blueberry` unless you change it
- connect the pi to the MPC1073, connect the MPC1073 to the HUB75 LED matrix 
- schedule [cronjob](https://www.raspberrypi.org/documentation/linux/usage/cron.md) to get weather every two minutes, and render upon boot

### Pi
```console
@reboot /home/pi/weather-reporter/pi/show_weather.sh >> /home/pi/weather-reporter/log
```

### Server
```console
* * * * * /home/bd/weather-reporter/server/update_display.sh >> /home/bd/log
```

## BOM
- Raspberry Pi or Pi Zero with [Hammer Header Male Connector](https://www.adafruit.com/product/3662?gclid=CjwKCAjw_47YBRBxEiwAYuKdw5l9LOCGMq1DYlVqqCFQ7JWwCHZdirC31xi53t6ke8LuWUJVX_u75RoCaIEQAvD_BwE), and power supply
- [MPC1073](http://www.electrodragon.com/product/rgb-matrix-panel-drive-board-raspberry-pi/) and CR1220 battery
- 16+ GB SD card, and card reader / writer
- [32x16 LED matrix](https://www.adafruit.com/product/420) with ribbon and 5 Volt 2 Amp power supply
- [Female DC Power adapter - 2.1mm jack to screw terminal block](https://www.adafruit.com/product/368) to go in back of the LED Matrix

## Troubleshooting
- `curl https://api.darksky.net/forecast/<API_KEY>/37.8267,-122.4233`
- notice what happens on the grid when `sudo ping -f -s 30000 weatherpi.local`
- wait at least 2 minutes after powering your pi with the LED display for the weather to appear
- after plugging in a pi with a freshly baked flash card, wait at least 5 minutes

## Thank You
- [Henner Zeller](https://github.com/hzeller/rpi-rgb-led-matrix) for sharing your sample code
- [Ari Zilnik](https://medium.com/@azilnik) for helping with soldering and graphics
- [Janice Shiu](https://github.com/contrepoint) for thinking of a cool name
- [Powered by Dark Sky](https://darksky.net/poweredby/)
