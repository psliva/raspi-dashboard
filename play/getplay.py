# Gather data from a variety of sources
import requests
from bs4 import BeautifulSoup
import pickle

import time

user_agent = {'User-agent': 'Mozilla/5.0'}
weather_url = 'Some_weather_feed'

# Store days in the pickle dump file
def days():
    arr = []
    for i in range(7):
        arr.append(time.strftime("%a (%b %d)", time.localtime(time.time() + 60 * 60 * 24 * i)))
    pickle.dump(arr,open('days.dat', 'w'))

# Store weather in the pickle dump file
def weather():
    arr = []
    r = requests.get(weather_url)
    soup = BeautifulSoup(r.text)

    s = ""
    num = 7
    for div in soup.find_all('div'):
        if div.get('class') == [u'wx-daypart']:
            #print(div.img)
            deg = ""
            degl = ""
            phrase = ""
            rain = ""
            img = ""
            for r2 in div.find_all('div'):
                for mp in r2.find_all('p'):
                    if mp != None and mp.get('class') == [u'wx-temp']:
                        if (mp.span != None):
                            mp.span.decompose()
                        if (mp.span != None):
                            mp.span.decompose()
                        if (mp.sup != None):
                            mp.sup.decompose()
                        deg = mp.get_text().strip()
                    if mp != None and mp.get('class') == [u'wx-temp-alt']:
                        if (mp.span != None):
                            mp.span.decompose()
                        if (mp.sup != None):
                            mp.sup.decompose()
                        degl = mp.get_text().strip()
                    if mp != None and mp.get('class') == [u'wx-phrase']:
                        phrase = mp.get_text().strip()
                if r2.get('class') == [u'wx-conditions']:
                    for mp2 in r2.find_all('p'):
                        mp2.decompose()
                    for mp3 in r2.img.find_all('a'):
                        mp3.decompose()
                    img = str(r2.img)
            for r3 in div.find('dd'):
                rain = r3.strip()
            num = num - 1
            if (num >= 0):
                arr.append([img.replace('\n',''),phrase.replace('\n',''),deg,degl,rain])
                #s = s + '<td><center>' + img + '<br>' + phrase + '<br><b>' + deg + '</b>&deg;' + ' | ' + degl + '&deg; | ' + rain + '</center></td>'
    pickle.dump(arr,open('weather.dat', 'w'))

# Get noaa wind forecast
# Acquired permission from mikes
def windNOAA(zone, filename):
    url = 'http://www.nwwind.net/regionfcst.php?fcst=' + zone
    print("Getting URL:%s, name:%s" % (url, filename))
    r = requests.get(url, headers = user_agent)
    soup = BeautifulSoup(r.text)
    res = soup.body.table.contents[11]
    arr = []
    last = ""
    for r in res:
        try:
            r.contents[6]
            if (last == r.contents[1].text):
                arr[len(arr)] = arr[len(arr)] + ', night:' + r.contents[5].text
            else:
                last = r.contents[1].text
                arr.append(r.contents[5].text)
            #print("%s, %s, %s" % (r.contents[1].text, r.contents[3].text, r.contents[5].text) )
        except Exception:
            1 == 1
    pickle.dump(arr, open( filename + '.dat', 'w'))

# Get all kiting forecast weather
# Todo: get permission from owner...
def kite():
    r = requests.get('http://windonthewater.com/api/region_wind.php?v=1&r=nw&k=test', headers = user_agent)
    soup = BeautifulSoup(r.text)
    db = int(soup.markers.find(id='KWAFREEL8')['wind'])
    dbg = int(soup.markers.find(id='KWAFREEL8')['gust'])
    snoq = int(soup.markers.find(id='OSOSNO')['wind'])
    snoqg = int(soup.markers.find(id='OSOSNO')['gust'])
    loc = int(soup.markers.find(id='WA010')['wind'])
    locg = int(soup.markers.find(id='WA010')['gust'])

# Get snow temp forecast
def snow():
    r = requests.get('http://www.snow-forecast.com/resorts/Stevens-Pass/6day/mid', headers = user_agent)
    soup = BeautifulSoup(r.text)
    soup.body.table.contents[1].decompose()
    soup.body.table.contents[2].decompose()
    soup.body.table.contents[11].decompose()
    soup.body.table.contents[22].decompose()
    soup.body.table.contents[23].decompose()
    soup.body.table.contents[24].decompose()
    soup.body.table.contents[25].decompose()
    mf = open("stevens.xml", "w")
    mf.write(soup.body.table.__str__())
    mf.close()

if __name__=="__main__":
    print "generating report..."
    days()
    weather()
    windNOAA('10', 'windns')
    windNOAA('60', 'windai')
    windNOAA('20', 'windc')
    snow()
