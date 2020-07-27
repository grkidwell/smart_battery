tools for communicating with Dell and HP smart batteries via SMBus

-uses SMBus2 library
-includes using Adafruit PiOLED 128x32 display
-will need to install Adafruit PiOLED library - see:
   https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi
-calls pioled.py local library for font scaling on the display
-use systemd service for loading at boot up 
   (batterystatus.service should be located in /lib/systemd/system) 
