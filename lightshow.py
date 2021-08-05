#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
 
import time
from rpi_ws281x import *
import argparse
 
# LED strip configuration:
LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def solidLightWipe(strip,color,wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i,color)
        strip.show()
        time.sleep(wait_ms/1000)
 

def breath(strip,color,wait_ms=50):
    increment = 1
    value = 0
    initialColor = color
    while True:
        if color[0] <= 0 or color[1] <= 0 or color[2] <= 0:
            break
        color[0]= color[0]-1;
        color[1] = color[1]-1;
        color[2] = color[2]-1;
    minColor = color
    for i in range(256):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i,color)
        strip.show()
        color[0] = color[0] + increment
        color[1] = color[1] + increment
        color[2] = color[2] + increment
        if (color[0] >= initialColor[0] or color[1] >= initialColor[1] or color[2] >= initialColor[2]):
            increment = -1
        elif(color[0]< minColor[0] or color[1]< minColor[1] or color[2]< minColor[2]):
            increment = 1
        time.sleep(wait_ms/1000.0)


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
 
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
 
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
 
    try:
     
        while True:
            solidLightWipe(strip,Color(255,0,0))
 
    except KeyboardInterrupt:
        if args.clear:
            solidLightWipe(strip, Color(0,0,0), 10)


# In[ ]:Color(1,2,3)





# %%
