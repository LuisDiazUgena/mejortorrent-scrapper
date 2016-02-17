import urllib
from BeautifulSoup import *
import re

from datetime import datetime
from threading import Timer
from time import sleep

import sys
from tqdm import * 

now=datetime.today()
nextTime=now.replace(day=now.day, hour=now.hour, minute= now.minute, second=now.second, microsecond=0)

def calculateNextTime():

        now=datetime.today()
        if (now.minute + 1) > 60:
            nextMinute = 0
        else:
            nextMinute = now.minute + 1
        nextTime=now.replace(day=now.day, hour=now.hour, minute= nextMinute, second=now.second, microsecond=0)
        delta_t=nextTime-now

        def printNextTime():
            print "Next time will be:", nextTime

        secs=delta_t.seconds+1

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
        print "\t" + lst[film]

    #calculateNextTime()

    '''
    fname = "lastMovies.txt"
    f = open(fname,'r+')
    for film in range(len(lst)):
        f.write(lst[film] + "\n")
        print lst[film]
    f.close()
    '''
    print ""
    #calculateNextTime()

#calculateNextTime()
print "This script scrap mejortorrent to gather the last HD quality movies."
scrap()
doneOnce = False
while True:
    userinput="s"
    #userinput = raw_input("Type \"s\" to continue, \"q\" to exit: ")"
    '''
    if (datetime.hour == 17 and datetime.minute == 30 and doneOnce == False):
        print "it's time to scrap!"
        scrap()
        doneOnce = True
    elif doneOnce == True:
        print "not time"
        doneOnce = False'''
    if userinput == "s" or userinput == "S"  :
        scrap()
    elif userinput == "q" or userinput == "Q" :
        print "Quiting..."
        sys.exit()
    else :
        print "type a valid option: \n\t scrap or quit"
    print "Now i'm going to sleep for a while.."
    for i in tqdm(range(60)):
        sleep(1)
        #now = datetime.today
    #scrap()
    '''
    if (now > nextTime):
        print "Now is the future!"
        calculateNextTime()
    '''
