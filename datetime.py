from tqdm import *

import time

import urllib
from BeautifulSoup import *
import re

def scrap_func():
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

print "This script scrap mejortorrent to gather the last HD quality movies."
#scrap_func()

while True:
    for i in tqdm(range(3600)):
        time.sleep(1)
    #time.sleep(10)
    scrap_func()
