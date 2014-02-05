#!/bin/sh
# Turn the screen on
tvservice --preferred > /dev/null
fbset -depth 8; fbset -depth 16; xrefresh
#MB_PID=`ps auxwww | grep Adafruit_CharLCD_IPclock_example.py | head -1 | awk '{print $2}'`
#kill -9 $MB_PID
#midori -p -e Fullscreen -a http://localhost:8000
