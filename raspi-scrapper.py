
import urllib
from BeautifulSoup import *
import re

from datetime import datetime
from threading import Timer

import sys

import Image
import ImageDraw
import ImageFont

from lib_tft24T import TFT24T
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

import spidev

from time import sleep

# Raspberry Pi configuration.
#For LCD TFT SCREEN:
DC = 24
RST = 25
LED = 18

#For PEN TOUCH:
#   (nothing)

# Create TFT LCD/TOUCH object:
TFT = TFT24T(spidev.SpiDev(), GPIO, landscape=True)
# If landscape=False or omitted, display defaults to portrait mode
# This demo can work in landscape or portrait

# Initialize display.
TFT.initLCD(DC, RST, LED)
# If rst is omitted then tie rst pin to +3.3V
# If led is omitted then tie led pin to +3.3V

# Get the PIL Draw object to start drawing on the display buffer.
draw = TFT.draw()

global films_str

def scrap():
    print ""
    url = "http://www.mejortorrent.com/torrents-de-peliculas-hd-alta-definicion.html"

    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)

    count = 0
    tags = soup('a')

    lst = list()
    for tag in tags:
        if re.search("peli-descargar-torrent-.+[0-9]",str(tag)) and not "img" in str(tag):
            if count > 9:
                initNamePos = str(tag).find(">")
                finishNamePos = str(tag).find(".",initNamePos)
                #print "initNamePos =", initNamePos
                #print "finishNamePos =",finishNamePos
                filmName = str(tag)[initNamePos+1:finishNamePos]
                filmName = re.sub('[\r]', '', filmName)
                filmName = re.sub('[\n]', '', filmName)
                if filmName not in lst:
                    lst.append(filmName)
            count += 1

    for film in range(len(lst)):
        global films_str
        films_str += lst[film] + "\n"
        #print "\t" + lst[film]

while 1:
    TFT.backlite(1)
    global films_str
    TFT.clear()
    font=ImageFont.truetype('FreeSans.ttf', 25)
    if TFT.is_landscape:
        draw.textwrapped((0,0), films_str, 38, 20, font, "lightblue")
    else:
        draw.textwrapped((0,0), films_str, 27, 20, font, "lightblue") # a bit narrower for portrait!
    TFT.display()
    sleep(20)
    TFT.clear()
    TFT.backlite(0)
    sleep(35)

#        All colours may be any notation (exc for clear() function):
#        (255,0,0)  =red    (R, G, B) - a tuple
#        0x0000FF   =red    BBGGRR   - note colour order
#        "#FF0000"  =red    RRGGBB   - html style
#        "red"      =red    html colour names, insensitive
"""
