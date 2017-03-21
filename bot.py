########################################################################
########################################################################
import ch
import random
import sys
import re
import json
import time
import simi
import datetime
import os
import urllib
from xml.etree import cElementTree as ET
if sys.version_info[0] > 2:
  import urllib.request as urlreq
else:
  import urllib2 as urlreq

botname = 'toumabot' ##botname
password = 'evrytime123' ##password

########################################################################
#ROOMS NICKS
########################################################################

def sntonick(username):
    user = username.lower()
    if user in nicks:
        nick = json.loads(nicks[user])
        return nick
    else:
        return user

########################################################################
#GETUPTIME / REBOOT
########################################################################

def getUptime():
    # do return startTime if you just want the process start time
    return time.time() - startTime

def reboot():
    output = ("rebooting server . . .")
    os.popen("sudo -S reboot")
    return output
  
########################################################################
#UPTIME
########################################################################

def uptime():
 
     total_seconds = float(getUptime())
 
     # Helper vars:
     MINUTE  = 60
     HOUR    = MINUTE * 60
     DAY     = HOUR * 24
 
     # Get the days, hours, etc:
     days    = int( total_seconds / DAY )
     hours   = int( ( total_seconds % DAY ) / HOUR )
     minutes = int( ( total_seconds % HOUR ) / MINUTE )
     seconds = int( total_seconds % MINUTE )
 
     # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
     string = ""
     if days > 0:
         string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
     if len(string) > 0 or hours > 0:
         string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
     if len(string) > 0 or minutes > 0:
         string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
     string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )
 
     return string;

########################################################################
#DEFINITIONS
########################################################################

dictionary = dict() 
f = open("definitions.txt", "r")
for line in f.readlines():
  try:
    if len(line.strip())>0:
      word, definition, name = json.loads(line.strip())
      dictionary[word] = json.dumps([definition, name])
  except:
    print("[ERROR]Cant load definition: %s" % line)
f.close()
##nicks
nicks=dict()#empty list
f=open ("nicks.txt","r")#r=read w=right
for line in f.readlines():#loop through eachlinimporte and read each line
    try:#try code
        if len(line.strip())>0:#strip the whitespace checkgreater than 0
            user , nick = json.loads(line.strip())
            nicks[user] = json.dumps(nick)
    except:
        print("[Error]Can't load nick %s" % line)
f.close()
##Rooms
rooms = []
f = open("rooms.txt", "r") 
for name in f.readlines():
  if len(name.strip())>0: rooms.append(name.strip())
f.close()
##owners
owners = []
try:
    file = open("owners.txt", "r")
    for name in file.readlines():
        if len(name.strip()) > 0:
            owners.append(name.strip())
    print("[INFO]Owners loaded...")
    file.close()
except:
    print("[ERROR]no file named owners")
    print("2 second to read the error")
    time.sleep(2)
    exit()
time.sleep(1)

###admin
admin = []
try:
    file = open("admin.txt", "r")
    for name in file.readlines():
        if len(name.strip()) > 0:
            admin.append(name.strip())
    print("[INFO]Admin loaded...")
    file.close()
except:
    print("[ERROR]no file named admin")
    print("2 second to read the error")
    time.sleep(2)
    exit()
time.sleep(1)

##Dlist
dlist = []
f = open("dlist.txt", "r") 
for name in f.readlines():
  if len(name.strip())>0: dlist.append(name.strip())
f.close()
##SN TRY
sn = dict()
try:
  f = open('note.txt','r')
  sn = eval(f.read())
  f.close()
except:pass
##Send Notes
sasaran = dict()
f = open ("notes.txt", "r") 
for line in f.readlines():
  try:
    if len(line.strip())>0:
      to, body, sender = json.loads(line.strip())
      sasaran[to] = json.dumps([body, sender])
  except:
    print("[Error] Notes load fails : %s" % line)
f.close()
##SN Notifs
notif = []
f = open("notif.txt", "r")
for name in f.readlines():
  if len(name.strip())>0: notif.append(name.strip())
f.close


########################################################################
#TEXTO ARCO-ÍRIS
########################################################################

def rainbow(word):
    length = len(word)
    #set rgb values
    r = 255 #rgb value set to red by default
    g = 0
    b = 0
    sub = int(765/length)
    counter = 0
    string = ""
    for x in range(0, length):
        letter = word[counter]
        s = "<f x12%02X%02X%02X='0'>%s" % (r, g, b, letter)
        string = string+s
        counter+=1
        if (r == 255) and (g >= 0) and (b == 0): #if all red
            g = g+sub
            if g > 255: g = 255
        if (r > 0) and (g == 255) and (b == 0): #if some red and all green
            r = r-sub #reduce red to fade from yellow to green
            if r<0: r = 0 #if red gets lower than 0, set it back to 0
        if (r == 0) and (g == 255) and (b >= 0):
            b = b+sub
            if b>255:
                b = 255
                trans = True
        if (r == 0) and (g > 0) and (b == 255):
            g = g-sub
            if g<0: g = 0
        if (r >= 0) and (g == 0) and (b == 255):
            r = r+sub
            if r>255: r = 255
    return string

########################################################################
#BGTIME
########################################################################
  
def bgtime(x):
        try:
                x = user if len(x) == 0 else x
                html = urlreq.urlopen("http://st.chatango.com/profileimg/%s/%s/%s/mod1.xml" % (x.lower()[0], x.lower()[1], x.lower())).read().decode()
                inter = re.compile(r'<d>(.*?)</d>', re.IGNORECASE).search(html).group(1)
                if int(inter) < time.time():
                        lbgtime = getSTime(int(inter))
                        return "O BG desse usuário acabou %s atrás" % lbgtime
                else: return "O tempo de bg de <b>%s</b>: %s" % (x.lower(), getBGTime(int(inter)))
        except: return 'Esse usuário não tem bg.'

def getBGTime(x):
                    total_seconds = float(x - time.time())
                    MIN     = 60
                    HOUR    = MIN * 60
                    DAY     = HOUR * 24
                    YEAR    = DAY * 365.25
                    years   = int( total_seconds / YEAR )      
                    days    = int( (total_seconds % YEAR ) / DAY  )
                    hrs     = int( ( total_seconds % DAY ) / HOUR )
                    min = int( ( total_seconds  % HOUR ) / MIN )
                    secs = int( total_seconds % MIN )
                    string = ""
                    if years > 0: string += "<font color='#00ffff'>" + str(years) + "</font> " + (years == 1 and "ano" or "anos" ) + ", "
                    if len(string) > 0 or days > 0: string += "<font color='#00ffff'>" + str(days) + "</font> " + (days == 1 and "dia" or "dias" ) + ", "
                    if len(string) > 0 or hrs > 0: string += "<font color='#00ffff'>" + str(hrs) + "</font> " + (hrs == 1 and "hora" or "horas" ) + ", "
                    if len(string) > 0 or min > 0: string += "<font color='#00ffff'>" + str(min) + "</font> " + (min == 1 and "minuto" or "minutos" ) + " e "
                    string += "<font color='#00ffff'>" +  str(secs) + "</font> " + (secs == 1 and "segundo" or "segundos" )
                    return string;

########################################################################
#YOUTUBE
########################################################################

def tube(args):
  """
  #In case you don't know how to use this function
  #type this in the python console:
  >>> tube("pokemon dash")
  #and this function would return this thing:
  {'title': 'TAS (DS) Pokémon Dash - Regular Grand Prix', 'descriptions': '1st round Grand Prix but few mistake a first time. Next Hard Grand Prix will know way and few change different Pokémon are more faster and same course Cup.', 'uploader': 'EddieERL', 'link': 'http://www.youtube.com/watch?v=QdvnBmBQiGQ', 'videoid': 'QdvnBmBQiGQ', 'viewcount': '2014-11-04T15:43:15.000Z'}
  """
  search = args.split()
  url = urlreq.urlopen("https://www.googleapis.com/youtube/v3/search?q=%s&part=snippet&key=AIzaSyBSnh-sIjd97_FmQVzlyGbcaYXuSt_oh84" % "+".join(search))
  udict = url.read().decode('utf-8')
  data = json.loads(udict)
  rest = []
  for f in data["items"]:
    rest.append(f)
  
  d = random.choice(rest)
  link = "http://www.youtube.com/watch?v=" + d["id"]["videoId"]
  videoid = d["id"]["videoId"]
  title = d["snippet"]["title"]
  uploader = d["snippet"]["channelTitle"]
  descript = d["snippet"]['description']
  count    = d["snippet"]["publishedAt"]
  return "Result: %s <br/><br/><br/><br/><br/><br/><br/><br/><font color='#ffcc00'><b>%s</b></font><br/><font color='#ff0000'><b>Uploader</b></font>:<b> %s</b><br/><font color='#ff0000'><b>Uploaded on</b></font>: %s<br/><font color='#ff0000'><b>Descriptions</b></font>:<i> %s ...</i><br/> " % (link, title, uploader, count, descript[:200])

########################################################################
#GS / GOOGLE SEARCH
########################################################################

def gs(args):
  args = args.split()
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request("https://www.google.co.id/search?q=" + "+".join(args), headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('\r','').replace('\t','').replace('http://','gs:').replace('https://','gs:')
  anjay = re.findall('<h3 class="r">(.*?)</h3>', resp)
  setter = list()
  la = "".join(anjay)
  a = re.findall('<a href="gs:(.*?)" onmousedown="(.*?)">(.*?)</a>', la)
  q = 1
  for link, fak, title in a:
      setter.append('<br/>[%s] %s : http://%s' % (q, title.capitalize(), link))
      q += 1
  return "<br/><br/>".join(setter[0:4])

########################################################################
#GIS
########################################################################

def gisd(cari):
  argss = cari
  args = argss.split()
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request("https://www.google.co.id/search?hl=en&authuser=0&site=imghp&tbm=isch&source=hp&biw=1366&bih=623&q=" + "+".join(args), headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('\r','').replace('\t','').replace('http://','gis:').replace('https://','gis:').replace('.jpg','.jpg:end').replace('.gif','.gif:end').replace('.png','.png:end')
  anjay = re.findall('<div class="rg_meta">(.*?)</div>', resp)
  setter = list()
  la = "".join(anjay)
  a = re.findall('"ou":"gis:(.*?):end","ow"', la)
  q = 1
  for result in a:
    if ".jpg" in result or ".gif" in result or ".png" in result:
     if "vignette" not in result and "mhcdn.net" not in result and "wikia.nocookie" not in result and "twimg.com" not in result:
      setter.append('(<b>%s</b>). http://%s' % (q, result))
      q += 1
  return "Search result for <b>"+cari+"</b>:<br/><br/>"+"<br/>".join(setter[0:5])

def gs(cari):
  args = cari.split()
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request("https://www.google.co.id/search?q=" + "+".join(args), headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('\r','').replace('\t','').replace('http://','gs:').replace('https://','gs:')
  anjay = re.findall('<h3 class="r">(.*?)</h3>', resp)
  setter = list()
  la = "".join(anjay)
  a = re.findall('<a href="gs:(.*?)" onmousedown="(.*?)">(.*?)</a>', la)
  q = 1
  for link, fak, title in a:
      setter.append('(<b>%s</b>). <b>%s</b>: http://%s' % (q, title.capitalize(), link))
      q += 1
  return "Search result for <b>"+cari+"</b>:<br/><br/>"+"<br/>".join(setter[0:5])

def gisc(cari):
  argss = cari
  args = argss.split()
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request("https://www.google.co.id/search?hl=en&authuser=0&site=imghp&tbm=isch&source=hp&biw=1366&bih=623&q=" + "+".join(args), headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('\r','').replace('\t','').replace('http://','gis:').replace('https://','gis:').replace('.jpg','.jpg:end').replace('.gif','.gif:end').replace('.png','.png:end')
  anjay = re.findall('<div class="rg_meta">(.*?)</div>', resp)
  setter = list()
  la = "".join(anjay)
  a = re.findall('"ou":"gis:(.*?):end","ow"', la)
  q = 1
  for result in a:
    if ".jpg" in result or ".gif" in result or ".png" in result:
     if "vignette" not in result and "mhcdn.net" not in result and "wikia.nocookie" not in result and "twimg.com" not in result:
      setter.append('(<b>%s</b>). http://%s' % (q, result))
      q += 1
  return "Search result for <b>"+cari+"</b>:<br/><br/>"+"<br/>".join(setter[0:4])

def gs(cari):
  args = cari.split()
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request("https://www.google.co.id/search?q=" + "+".join(args), headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('\r','').replace('\t','').replace('http://','gs:').replace('https://','gs:')
  anjay = re.findall('<h3 class="r">(.*?)</h3>', resp)
  setter = list()
  la = "".join(anjay)
  a = re.findall('<a href="gs:(.*?)" onmousedown="(.*?)">(.*?)</a>', la)
  q = 1
  for link, fak, title in a:
      setter.append('(<b>%s</b>). <b>%s</b>: http://%s' % (q, title.capitalize(), link))
      q += 1
  return "Search result for <b>"+cari+"</b>:<br/><br/>"+"<br/>".join(setter[0:5])

def gisb(cari):
  argss = cari
  args = argss.split()
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request("https://www.google.co.id/search?hl=en&authuser=0&site=imghp&tbm=isch&source=hp&biw=1366&bih=623&q=" + "+".join(args), headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('\r','').replace('\t','').replace('http://','gis:').replace('https://','gis:').replace('.jpg','.jpg:end').replace('.gif','.gif:end').replace('.png','.png:end')
  anjay = re.findall('<div class="rg_meta">(.*?)</div>', resp)
  setter = list()
  la = "".join(anjay)
  a = re.findall('"ou":"gis:(.*?):end","ow"', la)
  q = 1
  for result in a:
    if ".jpg" in result or ".gif" in result or ".png" in result:
     if "vignette" not in result and "mhcdn.net" not in result and "wikia.nocookie" not in result and "twimg.com" not in result:
      setter.append('(<b>%s</b>). http://%s' % (q, result))
      q += 1
  return "Search result for <b>"+cari+"</b>:<br/><br/>"+"<br/>".join(setter[0:3])

def gs(cari):
  args = cari.split()
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request("https://www.google.co.id/search?q=" + "+".join(args), headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('\r','').replace('\t','').replace('http://','gs:').replace('https://','gs:')
  anjay = re.findall('<h3 class="r">(.*?)</h3>', resp)
  setter = list()
  la = "".join(anjay)
  a = re.findall('<a href="gs:(.*?)" onmousedown="(.*?)">(.*?)</a>', la)
  q = 1
  for link, fak, title in a:
      setter.append('(<b>%s</b>). <b>%s</b>: http://%s' % (q, title.capitalize(), link))
      q += 1
  return "Search result for <b>"+cari+"</b>:<br/><br/>"+"<br/>".join(setter[0:5])

def gisa(cari):
  argss = cari
  args = argss.split()
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request("https://www.google.co.id/search?hl=en&authuser=0&site=imghp&tbm=isch&source=hp&biw=1366&bih=623&q=" + "+".join(args), headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('\r','').replace('\t','').replace('http://','gis:').replace('https://','gis:').replace('.jpg','.jpg:end').replace('.gif','.gif:end').replace('.png','.png:end')
  anjay = re.findall('<div class="rg_meta">(.*?)</div>', resp)
  setter = list()
  la = "".join(anjay)
  a = re.findall('"ou":"gis:(.*?):end","ow"', la)
  q = 1
  for result in a:
    if ".jpg" in result or ".gif" in result or ".png" in result:
     if "vignette" not in result and "mhcdn.net" not in result and "wikia.nocookie" not in result and "twimg.com" not in result:
      setter.append('(<b>%s</b>). http://%s' % (q, result))
      q += 1
  return "Search result for <b>"+cari+"</b>:<br/><br/>"+"<br/>".join(setter[0:2])

def gs(cari):
  args = cari.split()
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request("https://www.google.co.id/search?q=" + "+".join(args), headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('\r','').replace('\t','').replace('http://','gs:').replace('https://','gs:')
  anjay = re.findall('<h3 class="r">(.*?)</h3>', resp)
  setter = list()
  la = "".join(anjay)
  a = re.findall('<a href="gs:(.*?)" onmousedown="(.*?)">(.*?)</a>', la)
  q = 1
  for link, fak, title in a:
      setter.append('(<b>%s</b>). <b>%s</b>: http://%s' % (q, title.capitalize(), link))
      q += 1
  return "Search result for <b>"+cari+"</b>:<br/><br/>"+"<br/>".join(setter[0:5])

def gis(cari):
  argss = cari
  args = argss.split()
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request("https://www.google.co.id/search?hl=en&authuser=0&site=imghp&tbm=isch&source=hp&biw=1366&bih=623&q=" + "+".join(args), headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('\r','').replace('\t','').replace('http://','gis:').replace('https://','gis:').replace('.jpg','.jpg:end').replace('.gif','.gif:end').replace('.png','.png:end')
  anjay = re.findall('<div class="rg_meta">(.*?)</div>', resp)
  setter = list()
  la = "".join(anjay)
  a = re.findall('"ou":"gis:(.*?):end","ow"', la)
  q = 1
  for result in a:
    if ".jpg" in result or ".gif" in result or ".png" in result:
     if "vignette" not in result and "mhcdn.net" not in result and "wikia.nocookie" not in result and "twimg.com" not in result:
      setter.append('(<b>%s</b>). http://%s' % (q, result))
      q += 1
  return "Search result for <b>"+cari+"</b>:<br/><br/>"+"<br/>".join(setter[0:1])

def gs(cari):
  args = cari.split()
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request("https://www.google.co.id/search?q=" + "+".join(args), headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('\r','').replace('\t','').replace('http://','gs:').replace('https://','gs:')
  anjay = re.findall('<h3 class="r">(.*?)</h3>', resp)
  setter = list()
  la = "".join(anjay)
  a = re.findall('<a href="gs:(.*?)" onmousedown="(.*?)">(.*?)</a>', la)
  q = 1
  for link, fak, title in a:
      setter.append('(<b>%s</b>). <b>%s</b>: http://%s' % (q, title.capitalize(), link))
      q += 1
  return "Search result for <b>"+cari+"</b>:<br/><br/>"+"<br/>".join(setter[0:5])

##Random number game
def numbergame():
    randomnumber=random.choice(["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100"])
    answer=randomnumber
    return answer    
########################################################################
#SAVERANK
########################################################################

def saveRank():
    f = open("owners.txt","w")
    f.write("\n".join(owners))
    f.close()
    f = open("admin.txt","w")
    f.write("\n".join(admin))
    f.close()
    
def googleSearch(search):
  try:
    encoded = urllib.parse.quote(search)
    rawData = urllib.request.urlopen("http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="+encoded).read().decode("utf-8")
    jsonData = json.loads(rawData)
    searchResults = jsonData["responseData"]["results"]
    full = []
    val = 1
    for data in searchResults:
      if "youtube" in data["url"]:
        data["url"] = "http://www.youtube.com/watch?v="+data["url"][35:]
      full.append("<br/>"+"(<b>%s</b> %s -> %s" % (val, data["title"], data['url']))
      val = val + 1
    return '<br/>'.join(full).replace('https://','http://')
  except Exception as e:
    return str(e)

########################################################################
#TLI / TRADUTOR
########################################################################

def tli(args, tl):
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urlreq.Request("http://mymemory.translated.net/api/get?q="+"+".join(args.split())+"&langpair=PT|ID", headers = headers)
  resp = urlreq.urlopen(req).read().decode("utf-8").replace('\n','') .replace('\r','').replace('\t','')
  data = json.loads(resp)
  translation = data['responseData']['translatedText']
  if not isinstance(translation, bool):
    return translation
  else:
    matches = data['matches']
    for match in matches:
     if not isinstance(match['translation'], bool):
      next_best_match = match['translation']
      break

def tip(args, tl):
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urlreq.Request("http://mymemory.translated.net/api/get?q="+"+".join(args.split())+"&langpair=ID|PT", headers = headers)
  resp = urlreq.urlopen(req).read().decode("utf-8").replace('\n','') .replace('\r','').replace('\t','')
  data = json.loads(resp)
  translation = data['responseData']['translatedText']
  if not isinstance(translation, bool):
    return translation
  else:
    matches = data['matches']
    for match in matches:
     if not isinstance(match['translation'], bool):
      next_best_match = match['translation']
      break

def tle(args, tl):
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urlreq.Request("http://mymemory.translated.net/api/get?q="+"+".join(args.split())+"&langpair=PT|EN", headers = headers)
  resp = urlreq.urlopen(req).read().decode("utf-8").replace('\n','') .replace('\r','').replace('\t','')
  data = json.loads(resp)
  translation = data['responseData']['translatedText']
  if not isinstance(translation, bool):
    return translation
  else:
    matches = data['matches']
    for match in matches:
     if not isinstance(match['translation'], bool):
      next_best_match = match['translation']
      break

def tlp(args, tl):
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urlreq.Request("http://mymemory.translated.net/api/get?q="+"+".join(args.split())+"&langpair=EN|PT", headers = headers)
  resp = urlreq.urlopen(req).read().decode("utf-8").replace('\n','') .replace('\r','').replace('\t','')
  data = json.loads(resp)
  translation = data['responseData']['translatedText']
  if not isinstance(translation, bool):
    return translation
  else:
    matches = data['matches']
    for match in matches:
     if not isinstance(match['translation'], bool):
      next_best_match = match['translation']
      break

def tjp(args, tl):
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urlreq.Request("http://mymemory.translated.net/api/get?q="+"+".join(args.split())+"&langpair=JA|PT", headers = headers)
  resp = urlreq.urlopen(req).read().decode("utf-8").replace('\n','') .replace('\r','').replace('\t','')
  data = json.loads(resp)
  translation = data['responseData']['translatedText']
  if not isinstance(translation, bool):
    return translation
  else:
    matches = data['matches']
    for match in matches:
     if not isinstance(match['translation'], bool):
      next_best_match = match['translation']
      break


def tlj(args, tl):
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urlreq.Request("http://mymemory.translated.net/api/get?q="+"+".join(args.split())+"&langpair=PT|JA", headers = headers)
  resp = urlreq.urlopen(req).read().decode("utf-8").replace('\n','') .replace('\r','').replace('\t','')
  data = json.loads(resp)
  translation = data['responseData']['translatedText']
  if not isinstance(translation, bool):
    return translation
  else:
    matches = data['matches']
    for match in matches:
     if not isinstance(match['translation'], bool):
      next_best_match = match['translation']
      break


def dtl(args):
  url = "http://ws.detectlanguage.com/0.2/detect?q="+"+".join(quote(args).split())+"&key=demo"
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request(url, headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('  ','').replace(' Subtitle Indonesia','').replace('-subtitle-indonesia','')
  res = re.findall('"language":"(.*?)"', resp)
  newset = list()
  num = 1
  return "".join(res).upper()

def dtg(args):
  url = "http://ws.detectlanguage.com/0.2/detect?q="+"+".join(quote(args).split())+"&key=demo"
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  req = urllib.request.Request(url, headers = headers)
  resp = urllib.request.urlopen(req).read().decode("utf-8").replace('\n','').replace('  ','').replace(' Subtitle English','').replace('-subtitle-english','')
  res = re.findall('"language":"(.*?)"', resp)
  newset = list()
  num = 1
  return "".join(res).upper()

########################################################################
#CORES DE FONTE
########################################################################

class TestBot(ch.RoomManager):
  
  def onInit(self):
    self.setNameColor("000000")
    self.setFontColor("FF0000")
    self.setFontFace("Calibri")
    self.setFontSize(11)
    self.enableBg()
    self.enableRecording()

########################################################################
#CONEXÃO
########################################################################

  def onConnect(self, room):
    print("Connected")
  
  def onReconnect(self, room):
    print("Reconnected")
  
  def onDisconnect(self, room):
    print("Disconnected")

########################################################################
#OBTER ACESSO
########################################################################

  def getAccess(self, user):
    if user.name in owners: return 4 # Owners
    elif user.name in admin: return 3 # Admins
    else: return 0

#SN Notif
    if user.name in notif and user.name in sasaran:
      room.message(user.name+", you got a note left unread. Do +readnote to read it")
      notif.remove(user.name)
      
########################################################################
#ON MENSAGEM / PERSONALIDADE DO BOT E PREFIX
########################################################################
  
  def onMessage(self, room, user, message):
   try:
    msgdata = message.body.split(" ",1)
    if len(msgdata) > 1:
      cmd, args = msgdata[0], msgdata[1]
    else:
      cmd, args = msgdata[0],""
      cmd=cmd.lower() 
    global lockdown
    global newnum
    print(user.name+" - "+message.body)
    if user.name in notif:
        room.message(user.name+", you got ("+str(len(sn[user.name]))+") messages unread. Do irn to read them")
        notif.remove(user.name)
    if user == self.user: return
    if "touma" in message.body.lower() or "Touma" in message.body.lower() and "^" not in message.body[:1]:
        if len(args) > 1:
            room.message(__import__("simi").simi(args),True)
        else:
            room.message("Iya? "+sntonick(user.name), True)

    if message.body.startswith("sepi"):
     if self.getAccess(user) >= 6:
      jawab = ["Kan ada aku ","aku ada disini "]
      room.message (random.choice(jawab) +sntonick(user.name)+" :D",True)
     else:
       room.message("Ada aku kok")

    if message.body.startswith("kacang"):
     if self.getAccess(user) >= 6:
      jawab = ["Yang sabar yah kak","Mampus Dikacangin","Kacang mahal :v"]
      room.message(random.choice(jawab)+" @"+user.name)
     else:
       room.message("Cie yang di kacangin")

    if message.body.startswith("Test") or message.body.startswith("test"):
     if user.name == "evrytimescarlet":
      jawab = ["Test Confirmed"]
      room.message(random.choice(jawab)+" @"+user.name)
     if self.getAccess(user) <= 5 and not user.name in blacklist:
      room.message("Test Accept "+sntonick(user.name)+" :D")

    if message.body.startswith("your mastah mana?"):
     if self.getAccess(user) >= 1 or room.getLevel(user) > 0 and not user.name in blacklist:
      room.message("mastah lagi sibuk XD")

    if message.body.startswith("Tidur")or message.body.startswith("tidur"):
     if self.getAccess(user) >= 1 or room.getLevel(user) > 0 and not user.name in blacklist: 
      room.message (random.choice(["Mimpiin aku ya, "+sntonick(user.name)+" :D ",]),True)
      
    if message.body.startswith("pagi")or message.body.startswith("Pagi"):
     if self.getAccess(user) >= 1 or room.getLevel(user) > 0 and not user.name in blacklist: 
      room.message (random.choice(["Selamat Pagi, "+sntonick(user.name)+" :D ",]),True)
      
    if message.body.startswith("siang")or message.body.startswith("Siang"):
     if self.getAccess(user) >= 1 or room.getLevel(user) > 0 and not user.name in blacklist: 
      room.message (random.choice(["Selamat Siang, "+sntonick(user.name)+" :D ",]),True)
      
    if message.body.startswith("sore")or message.body.startswith("Sore"):
     if self.getAccess(user) >= 1 or room.getLevel(user) > 0 and not user.name in blacklist: 
      room.message (random.choice(["Selamat Sore, "+sntonick(user.name)+" :D ",]),True)
      
    if message.body.startswith("malam") or message.body.startswith("Malam"):
     if self.getAccess(user) >= 1 or room.getLevel(user) > 0 and not user.name in blacklist:
      room.message (random.choice(["Selamat Malam, "+sntonick(user.name)+" :D ",]),True)
      
    if message.body.startswith("afk") or message.body.startswith("AFK"):
     if self.getAccess(user) >= 1 or room.getLevel(user) > 0 and not user.name in blacklist:
      room.message (random.choice(["Balik lagi, aku tunggu loh "+sntonick(user.name)+" :D ",]),True)
      
    if message.body.startswith("back") or message.body.startswith("BACK"):
     if self.getAccess(user) >= 1 or room.getLevel(user) > 0 and not user.name in blacklist:
      room.message (random.choice(["Welcome Back, "+sntonick(user.name)+" :D ",]),True)
      
    if message.body.startswith("brb")or message.body.startswith("BRB"):
     if self.getAccess(user) >= 1 or room.getLevel(user) > 0 and not user.name in blacklist:
      room.message (random.choice(["Jangan Balik Lagi ya "+sntonick(user.name)+" XD ",]),True)
      
    if message.body.startswith("off")or message.body.startswith("OFF"):
     if self.getAccess(user) >= 1 or room.getLevel(user) > 0 and not user.name in blacklist:
      room.message (random.choice(["Matta Nee "+sntonick(user.name)+" :D ",]),True)
      
    if message.body.startswith("quotes"):
      room.message(random.choice(["Kita tidak boleh menangis. Karena menangis adalah kekalahan raga terhadap hati dan hanya membuktikan bahwa kita tidak bisa mengendalikan hati",
          "Kami takut pada yang tidak memiliki wujud",
          "Sama saja, yang mati atau yang ditinggal… dua-duanya sama-sama kesepian!",
          "Orang bisa memiliki harapan karena kematian adalah sesuatu yang tak terlihat",
          "Kau tahu kenapa kakak dilahirkan terlebih dahulu? Untuk melindungi adik-adiknya!",
          "Nyawa bukan sesuatu yang boleh direbut orang lain",
          "Aku tidak bisa melindungimu kalau tidak memegang pedang. Tapi saat memegang pegang aku tidak akan pernah bisa memelukmu",
          "Rasa rindu, rasa cinta atau persahabatan, semua itu benar-benar merepotkan. Apalagi perasaan iri dengan semua itu..",
          "Those painful memories are what help us make it to tomorrow and become stronger.",
          "If you realize you made a mistake with the way you've been living your life, you just have to take the next moment and start over.",
          "If the drive behind one's actions is the thought for another, then it is never meaningless.",
          "Always trying to make myself seem strong... So I locked my own heart in a suit of armor.",
          "If you truly desire greatness, you must first know what makes you weak!",
          "I've heard you've been causing trouble again. Even if Master forgives you, I won't.",
          "I won't allow it! I won't allow you to die like this! You've committed crimes! You must remember everything! Don't think you can be at ease without knowing anything! Don't expect to be forgiven by the people who you've hurt! Live and struggle!",
          "I wonder for how long... How long will I remain anchored at this harbor known as battle?"]))
    if message.body.startswith("qby"):
     if self.getAccess(user) >= 1 or room.getLevel(user) > 0 and not user.name in blacklist:
      room.message(random.choice(["Quotes by Erza Scarlet and Ichigo Kurosaki"]),True)
    if message.body == "": return  
    if message.body[0] in ["!"] or message.body[0] in [""]:   
      data = message.body[1:].split(" ", 1)
      if len(data) > 1:
        cmd, args = data[0], data[1]
      else:
        cmd, args = data[0], ""

########################################################################
#VERIFICAR ACESSO
########################################################################
        
      if self.getAccess(user) == 1: return 
      def pars(args):
        args=args.lower()
        for name in room.usernames:
          if args in name:return name    
      def roompars(args):
        args = args.lower()
        for name in self.roomnames:
          if args in name:return name
      def roomUsers():
          usrs = []
          gay = []
          prop = 0
          prop = prop + len(room._userlist) - 1
          for i in room._userlist:
            i = str(i)
            usrs.append(i)
          while prop >= 0:
            j = usrs[prop].replace("<User: ", "")
            i = j.replace(">", "")
            gay.append(i)
            prop = prop - 1
          return gay
      
      def getParticipant(arg):
          rname = self.getRoom(arg)
          usrs = []
          gay = []
          finale = []
          prop = 0
          prop = prop + len(rname._userlist) - 1
          for i in rname._userlist:
            i = str(i)
            usrs.append(i)
          while prop >= 0:
            j = usrs[prop].replace("<User: ", "")
            i = j.replace(">", "")
            gay.append(i)
            prop = prop - 1
          for j in gay:
            if j not in finale:
              finale.append(j)
          return finale


########################################################################
##COMANDOS ENGRAÇADOS 1
########################################################################
          
##dice
      if cmd == "dice":
          die1=random.randint(1,6)
          die2=random.randint(1,6)
          room.message("Rolando os dados caiu um "+str(die1)+" e um "+str(die2))

##myl
      if cmd == "myl":
          die1=random.randint(1,6)
          die2=random.randint(1,6)
          room.message(""+user.name.title()+" o amor da sua vida é "+random.choice(room.usernames)+" vocês vão se beijar "+str(die1)+" veze's ao dia e tem "+str(die2)+"% de chance de ficar com essa pessoa ^^")
          
##wyl
      if cmd == "wyl":
          die1=random.randint(1,6)
          die2=random.randint(1,6)
          room.message(""+user.name.title()+" sua waifu vai ser "+random.choice(room.usernames)+" vocês vão se beijar "+str(die1)+" vezes ao dia, vai levar "+str(die1)+" fora em um mês e tem "+str(die2)+"% de chance de ficar com essa pessoa ^_^")
         
##suck
      if cmd == "suck":
          die1=random.randint(1,6)
          die2=random.randint(1,6)
          room.message(" "+user.name.title()+"-senpai está chupando "+random.choice(room.usernames)+"-san Bem gostoso.")
          
##eat
      if cmd == "eat":
          die1=random.randint(1,6)
          die2=random.randint(1,6)
          room.message("Ohh Nãão!!! "+user.name.title()+" está comendo "+random.choice(room.usernames)+" u////u")
          
##kills
      if cmd == "kill":
          die1=random.randint(1,6)
          die2=random.randint(1,6)
          room.message(" "+user.name.title()+" acabou de matar "+random.choice(room.usernames)+" :@")

##kisses
      if cmd == "kisses":
          die1=random.randint(1,6)
          die2=random.randint(1,6)
          room.message(""+user.name.title()+" beija "+random.choice(room.usernames))
##BotStop
      if cmd == "stop" and user.name == "evrytimescarlet":##ISI ID LU
          if user.name == "evrytimescarlet":##ISI ID LU
            room.message("[Disconnected]")
            self.setTimeout(4, self.stop, )
          else:
             room.message("Who are you")
##hugs
      if cmd == "hugs":
          die1=random.randint(1,6)
          die2=random.randint(1,6)
          room.message("  "+user.name.title()+" abraça "+random.choice(room.usernames))
          
##hug
      if cmd == "hug":
          if args:
            room.message("*Abraçando " + args+"*")
          else:
            room.message("*Abraço "+random.choice(room.usernames)+"*")
#Find
      if cmd == "find" and len(args) > 0:
            name = args.split()[0].lower()
            if not ch.User(name).roomnames:
              room.message("aku tidak tau")
            else:
              room.message("kamu dapat menemukan  %s Di %s" % (args, ", ".join(ch.User(name).roomnames)),True)

##RB
      elif cmd == "rb":
          if args == "":
            rain = rainbow('Rainbow!')
            room.message(rain,True)
          else: 
             rain = rainbow(args)
             room.message(rain,True)

      elif cmd == "rb2":
          if args == "":
            rain = rainbow('Rainbow!')
            room.message(rain)
          else: 
            rain = rainbow(args)
            room.message(rain)

### MultiChat
      elif cmd == "multichat" or cmd == "mc" or cmd == "MultiChat" or cmd == "Mc":
        if args == "":
            room.message("My Default room : admiralevrytime.chatango.com")
        else:
            room.message("Done ! , This is your Room : http://ch.besaba.com/chat/flash/?"+args+"!")
      elif cmd == "multichat2" or cmd == "mc2":
        if args == "":
            room.message("My Default room : http://ch.besaba.com/chat/html5/?admiralevrytime!,meguminime-chat!,nosobafansubs!,nekonimecom!")
        else:
            room.message("Done : http://ch.besaba.com/chat/html5/?"+(args)+"!")

#### MyIp
      elif cmd =="myip" or cmd == "MyIp" or cmd == "MyIP" or cmd == "My IP Adress":
        try:
         room.message("IP address kamu adalah : "+message.ip)
        except:
         room.message("Gagal melihat IP address, Aku bukan mods disini.")

##testcmd
      if cmd == "webanime":
        room.message("<f x12F00='1'>Web Anime Untuk Sekarang:<f x12334433='1'><br/>1. Animeindo.id : ainew(new update on animeindo.id).<br/>2. Imoutosubs.com : isnew(new update on imoutosubs).<br/>3. Narutobleachlover.net : nbnew(new update on narutobleachlover).<br/>4. Kurogoze.net : krnew(new update on kurogaze) , krsr(kurogaze search).<br/>5. Nekonime.com : nknew(new update on nekonime).<br/>6. Animesave.com : asnew(new update on animesave.com) , assr(animesave.com search).<br/>7. Wardhanime.net : wanew(new update on wardhanime) , wasr(wardhanime search).<br/>8. Otanimesama : otnew(new update on otanimesama) , otsr(otanime search).<br/>9. Oploverz.net : opnew(new update on oploverz) , opsr(oploverz search).<br/>10. Fasatsu.com : fsnew(new update on fansatsu) , fssr(search fansatsu movie or anime).<br/>11. Samehadaku.net : sknew(new update on samehadaku).<br/>12.Anisubindo.net : aonew (new update on anisubindo.", True)
      if cmd == "webanime2":
        room.message("<f x12F00='1'>Web Anime Untuk Sekarang:<f x12334433='1'><br/>1. Meguminime.com<br/>2. Samehadaku.net<br/>3. Nekopoi.org<br/>4. Nekopoi.pro<br/>5. Hentonghaven.org", True)
      if cmd == "manga":
        room.message("<f x12F00='1'>Web Manga Untuk Sekarang:<f x12334433='1'><br/>1. mangaku.web.id<br/>2. mangafox.me<br/>3. onemanga.com<br/>4. sukahentong.com<br/>5. fakku.net<br/>6. pururin.us<br/>7. Hentongbox.net<br/>8. nhentong.net<br/>9. hitomi.la<br/>10. Hentonghere.com<br/>11. Hentong.ms<br/>12. Hentong2read.com<br/>Hentong di ganti HEN*AI", True)
      if cmd == "genre1":
        room.message("<f x12F00='1'>Genre Anime:<f x12334433='1'><br/>1. Action https://myanimelist.net/anime/genre/1/Action.<br/>2. Adventure https://myanimelist.net/anime/genre/2/Adventure.<br/>3. Cars https://myanimelist.net/anime/genre/3/Cars.<br/>4. Comedy https://myanimelist.net/anime/genre/4/Comedy.<br/>5. Dementia https://myanimelist.net/anime/genre/5/Dementia.<br/>6. Demon https://myanimelist.net/anime/genre/6/Demons.<br/>7. Drama https://myanimelist.net/anime/genre/8/Drama.<br/>8. Ecchi https://myanimelist.net/anime/genre/9/Ecchi.<br/>9. Fantasy https://myanimelist.net/anime/genre/10/Fantasy.<br/>10. Game https://myanimelist.net/anime/genre/11/Game.", True)
      if cmd == "genre2":
        room.message("<f x12F00='1'>Genre Anime:<f x12334433='1'><br/>1. Magic https://myanimelist.net/anime/genre/16/Magic.<br/>2. Martial Arts https://myanimelist.net/anime/genre/17/Martial_Arts.<br/>3. Mecha https://myanimelist.net/anime/genre/18/Mecha.<br/>4. Military https://myanimelist.net/anime/genre/38/Military.<br/>5. Music https://myanimelist.net/anime/genre/19/Music.<br/>6. Mystery https://myanimelist.net/anime/genre/7/Mystery.<br/>7. Parody https://myanimelist.net/anime/genre/20/Parody.<br/>8. Police https://myanimelist.net/anime/genre/39/Police.<br/>9. Psychological https://myanimelist.net/anime/genre/40/Psychological.<br/>10. Romance https://myanimelist.net/anime/genre/22/Romance.",True)
      if cmd == "Genre3":
        room.message("<f x12F00='1'>Genre Anime:<f x12334433='1'>", True)
      if cmd == "gannew": room.message(newGa(), True)
      if cmd == "sknew": room.message(newSk(), True)
      if cmd == "asnew": room.message(newAs(), True)
      if cmd == "annew": room.message(newAn(), True)
      if cmd == "aonew": room.message(newAo(), True)
      if cmd == "nknew": room.message(newNk(), True)
      if cmd == "krnew": room.message(newKr(), True)
      if cmd == "nbnew": room.message(newNb(), True)
      if cmd == "wasr": room.message(serWa(args), True)
      if cmd == "joinew": room.message(newJoi(), True)
      if cmd == "ennew": room.message(newEn(), True)
      if cmd == "ainew": room.message(newAi(), True)
      if cmd == "fsnew": room.message(newFs(), True)
      if cmd == "fssr": room.message(serFs(args), True)
      if cmd == "bgtime": room.message(bgtime(args), True)
      if cmd == "n123": room.message(newNonton123(), True)
      if cmd == "n123sr": room.message(serNonton123(args), True)
      if cmd == "hpsr": room.message(serHp(), True)
      if cmd == "opsr": room.message(serOp(args), True)
      if cmd == "krsr": room.message(serKg(args), True)
      if cmd == "assr": room.message(serAs(args), True)

##kiss
      if cmd == "kiss":
          if args:
            room.message("*Beijando " + args+"*")
          else:
            room.message("*Beijo "+random.choice(room.usernames)+"*")

##% / Porcentagem
      if cmd == "%":
          die1=random.randint(0,100)
          if args:
            room.message(random.choice([" "+str(die1)+"% de chance de ser verdade." , " "+str(die1)+"% de chance de ser mentira"]))
          else:
            room.message("Digite >% mais uma pergunta exemplo ( >% você é idiota?) Eu acho que é "+str(die1)+"% idiota, haha.")
            
#amor
      if cmd == "amn":
          die1=random.randint(0,100)
          if args:
            room.message("Seu nível de amor por " + args+ " é "+str(die1)+"%")
          else:
            room.message("Seu nível de amor por "+random.choice(room.usernames)+" é  "+str(die1)+"% ")
            
#kills           
      if cmd == "slay":
          if args:
            room.message(random.choice(["*Cravando uma faca nos olhos de " + args + "* *lol*","*Matando " + args + " com sexo* O/////O", "*Tiros em você, " + args + "*", "*Eu jogo gasolina em, " + args + ", e coloco fogo, queimaaaaaa! *lol*"]))
          else:
            room.message("Oooh, Não!!! "+random.choice(room.usernames)+" acaba de morrer. ")



########################################################################
#SITES DE IMAGENS
########################################################################
            
      if cmd == "psit":
         room.message("Ooi "+user.name+" <br/> http://i.ntere.st <br/>http://giphy.com<br/>http://huaban.com<br/>http://weheartit.com<br/>https://anime-pictures.net<br/>http://www.zerochan.net<br/>http://www.4chan.org<br/>https://br.pinterest.com<br/>http://bakarenders.com<br/>http://www.renders-graphiques.fr <br/>",True)

      if cmd == "psit2":
         room.message("Ooi "+user.name+" <br/> https://prcm.jp<br/>http://e-shuushuu.net<br/>http://www.minitokyo.net<br/>https://wall.alphacoders.com<br/>http://konachan.net<br/>https://yande.re<br/>http://www.gelbooru.com<br/>http://danbooru.donmai.us<br/>http://www.v3wall.com<br/>http://www.theanimegallery.com<br/> ",True)  

      if cmd == "icons":
         room.message("Ooi "+user.name+"  <br/> http://kawaiis-icons.tumblr.com<br/>http://yumis-icons.tumblr.com<br/>http://anime-icon-plaza.tumblr.com<br/>http://r-h-kawai-icons.tumblr.com<br/>http://sillica.tumblr.com<br/>http://anime--icons.tumblr.com<br/>http://2hundrdpx.tumblr.com<br/>http://fuckyeahanimangaicons.tumblr.com<br/>",True)   

      if cmd == "p18":
         room.message("Ooi "+user.name+"  <br/> https://luscious.net<br/>http://www.kawaiihentai.com<br/>http://hentai-image.com<br/>http://mutimutigazou.com<br/>http://www.mg-renders.net<br/>http://g.e-hentai.org<br/>http://www.moe.familyrenders.com<br/>http://ors-renders-ero.animemeeting.com<br/>",True)   

########################################################################
##LISTA DE COMANDOS
########################################################################

      if cmd == "acmds":
          room.message("Oi "+user.name+" Os comandos disponíveis <br/> gcmds[Google search], pcmds[Perfil Chatango], fcmds[Comandos Engraçados], rcmds[Comandos Chats]",True)
      
      if cmd == "gcmds":
          room.message("Oi "+user.name+" Os comandos disponíveis <br/> [Google search] yt(Youtube), gs(Google Pesquisa), gis, gis2, gis3, gis4, gis5(Google Imagens)",True)

      if cmd == "pcmds":
          room.message("Oi "+user.name+" Os comandos disponíveis <br/> [Perfil Chatango] prof, mini, bg, pic, bgtime ",True)

      if cmd == "wcmds":
          room.message("Oi "+user.name+" Os comandos disponíveis <br/>[Websites Imagens] psit, psit2, p18, icons   ",True)

      if cmd == "fcmds":
          room.message("Oi "+user.name+" Os comandos disponíveis <br/> [Comandos Engraçado] bot(Bot + Perguntas), %(Porcentagem + pergunta), amn( Nivel de amor), wyl(previsão waifu), myl(previsão amor), slay(matar um indivíduo), num, guess(Adivinhar), fap, abs, say, rsay, rb,rb2, dice, hug, hugs, suck, eat, kill, kisses, kiss, ping",True)

      if cmd == "rcmds":
          room.message("Oi "+user.name+" Os comandos disponíveis <br/> [Comandos chats] userlist, ismod, find, bc(Transmissão), join, leave, rooms, sn(enviar notas), rn(ler notas), inbox(caixa de entrada), pm(mensagem pv), wiki",True)

      if cmd == "cmds":
          room.message("<br/>"+user.name+"<br/>"+" Perintah[ ! or > ] :<br/>rb , rb2 , wl , whois , webanime ,webanime2 , genre1 , genre2 , manga , cso , pfpic , mini , prof of profile , df(define) , udf(undefine) , fax , bc , sn(sendnote) , rn(readnote) , join , leave , mydict , nick , staff , setnick , mynick , seenick , profile , rank , myrank , ranker , clear , del , sf , sfc, snc , sfz , myip , mc , mc2 , lock , unlock , lockstatus",True) 

########################################################################
#SETRANK
########################################################################
              
##Setrank
      if cmd == "setrank": 
        if self.getAccess(user) < 0:return
        try:
          if len(args) >= 3:
            name = args
            if pars(name) == None:
                name = name
            elif pars(name) != None:
                name = pars(name)
            name, rank = args.lower().split(" ", 1)
            if rank == "4":
              owners.append(name)
              f = open("owners.txt", "w")
              f.write("\n".join(owners))
              f.close()
              room.message("Sukses")
              if name in admin:
                admin.remove(name)
                f = open("admin.txt", "w")
                f.write("\n".join(admin))
                f.close()
            if rank == "3":
              admin.append(name)
              f = open("admin.txt", "w")
              f.write("\n".join(admin))
              f.close()
              room.message("Sukses")
              if name in owners:
                owners.remove(name)
                f = open("owners.txt", "w")
                f.write("\n".join(owners))
                f.close()
            if rank == "2":
               room.message("Sukses")
               if name in owners:
                 owners.remove(name)
                 f = open("owners.txt", "w")
                 f.write("\n".join(owners))
                 f.close()
               if name in admin:
                 admin.remove(name)
                 f = open("admin.txt", "w")
                 f.write("\n".join(admin))
                 f.close()
            if name in owners:
                  owners.remove(name)
                  f = open("owners.txt", "w")
                  f.write("\n".join(owners))
                  f.close()
            if name in admin:
                  admin.remove(name)
                  f = open("admin.txt", "w")
                  f.write("\n".join(admin))
                  f.close()       
        except:
              room.message("something wrong")
            
#######################################################################
#COMANDOS CHAT 1
########################################################################

##delete chat  
      elif (cmd == "delete" or cmd == "dl" or cmd == "del"):
          if room.getLevel(self.user) > 0:
            if self.getAccess(user) >= 0 or room.getLevel(user) > 0:
              name = args.split()[0].lower()
              room.clearUser(ch.User(name))
            else:room.message("You can not do it!!")
          else:
            room.message("I'm not the mods here :|")

##staff
      if cmd == "staff":
        room.message("<br/><f x12000000='0'><b>Owner:</b></f> %s<br/><f x12000000='0'><b>Admin:</b></f> %s" % (", ".join(owners), ", ".join(admin)),True)
  
##banlist            
      elif cmd == "banlist":
          if self.getAccess(user) >= 0 or room.getLevel(user) > 0:
            room.message("The banlist is: "+str(room.banlist))
 
##Find
      if cmd == "find" and len(args) > 0:
        name = args.split()[0].lower()
        if not ch.User(name).roomnames:
          room.message("I do not know")
        else:
          room.message("Pode achar %s em %s" % (args, ", ".join(ch.User(name).roomnames)),True)

########################################################################
#EVAL / SEI LÁ MAIS DEVE SER IMPORTANTE ESSE LANCE
########################################################################
                
      if cmd == "ev" or cmd == "eval" or cmd == "e":
        if self.getAccess(user) == 0:
          ret = eval(args)
          if ret == None:
            room.message("Done.")
            return
          room.message(str(ret))

########################################################################
#COMANDOS ENGRAÇADOS 2
########################################################################

##8ball
      if cmd == "bot":
        if self.getAccess(user) >= 0:
         room.message(random.choice(["Não mesmo *lol*","Pode apostar que sim! ^^ ","Sem chance .-.","Totalmente positivo capitão... o.ô"," Sai fora -.-","Omg, sério isso? >.>"," Claro que não :@ "," Eu adoraria isso! <3","O simples não... ^o^ ","Ah, talvez. :s "," Nunca... :v","Respondo se mandar nudes. *blush*","A resposta seria cabeluda ô.o", "Sim. *-*","Sinto muito, mas… T.T"," Eu respondo se me pagar um sorvete :c"," É provavel que sim ^.^ ","As Perspectivas são boas C: "," Depende do ponto de vista...","Fale seriamente pourra :@", "Como se atreve :@", "Isso vai acontecer em breve (: ", "Isso vai acontecer hoje (: ", "Não vai acontecer nunca n.n", "Cala-te idiota zz","Shh beije-me agora. ","A resposta não é importante "," Esqueça :@"," Eu já disse que te amo? u///u"," Por favor, pare de perguntar coisas estúpidas >.>"," Vou te dizer se você me der uma pizza "," Não vai acontecer nem se você usar mágia ","Vamos fazer sexo? go go"," Faça silêncio pervertido zz "," Você me da nojo, como ousa :@ "," Você é kawaii, lógico que sim, agora me ame n.n "," OMG Casar comigo? "," Pare de ser tão fofis"," Eu não sei o que vou fazer para você n.n"," Continuará com isso? n.n"," Foda-se zz"," Tudo vai ficar bem Shh shh <3 "," *beijo você * silêncio baby "," NÃO !: @ "," YES!: @ "," Definitivamente ^^"," Claro ^~^ "," Eu adoraria isso! >.> ","Sim", "Claro (:", "Sim n.n", "Não de jeito nenhum >.>" "Claro que não '-'", "Certamente não </3", "Não nem em um milhão de anos zz", "Nopes XD", "Não", "Nem", "De jeito nenhum ç.ç" , "Não agora :@", "Não desta vez n.n", "ninguém se importa *bored* ", "não é possível *bored* ", "shh vai comer o seu amigo zz", "shhh me come agora :@", "Noooooooooo", "Yeeeeeeeeesssssssss", " Não me incomode zz "," Que pergunta estúpida zz "]))
        else:
           room.message("pfft.yeah right.")
           
##Say
      if cmd == "say":
        room.message(args)

##rsay
      if cmd == "reverse" or cmd == "rsay":
          if args:
            room.message(args[::-1])
          else:
            room.message("Fook off"[::-1])

##Rainbow
      elif cmd == "rb":
            if args == "":
              rain = rainbow('Rainbow!')
              room.message(rain,True)
            else: 
               rain = rainbow(args)
               room.message(rain,True)

##Rainbow
      elif cmd == "rb2":
          if args == "":
            rain = rainbow('Rainbow!')
            room.message(rain)
          else: 
              rain = rainbow(args)
              room.message(rain)

          
########################################################################
#COMANDOS GIS / GOOGLE IMAGENS
########################################################################
          
      elif cmd == "gis2":
        if args:
          room.message(gisa(args),True)

      elif cmd == "gis3":
        if args:
          room.message(gisb(args),True)

      elif cmd == "gis4":
        if args:
          room.message(gisc(args),True)

      elif cmd == "gis5":
        if args:
          room.message(gisd(args),True)

      elif cmd == "gis":
        if args:
          room.message(gis(args),True)

########################################################################
#COMANDOS ALEATÓRIOS
########################################################################
          
      if cmd == "gs": 
        room.message(gs(args),True)    

      elif cmd == "youtube" or cmd == "yt":
        if args:
          room.message(tube(args),True)

      elif cmd == "bgtime":
        if args:
          room.message(bgtime(args),True)

###New number###
      elif (cmd == "num"):
          newnum = numbergame()
          room.message("Escolhe um numero de 1 a 100 exemplo (>guess 69)")
          print("[INFO] NEW NUMBER : "+newnum)
          return newnum          

###Guess number##
      elif (cmd == "guess") and len(args) > 0:
            if(args==newnum):
              room.message("*star* *star* DING DING DIIING *star* *star* ^_^ "+sntonick(user.name)+" , got it right with the number : "+args)
            elif(args!=newnum and newnum > args ):
              room.message("higher, ohh cmon ^^")
            elif(args!=newnum and newnum < args ):
              room.message("pfftt lower, c'mon-c'mon")
            else:
              room.message("error x_x")

##shot
      elif cmd =="rr":
          room.message("Spins the barrel and pulls the trigger."+random.choice(["Shoots, "+sntonick(user.name)+" dead. v.v","miss.","miss!!!","pop...miss.","missed","Blows off "+sntonick(user.name)+"s head. whahahahaha ."]))              

##dare
      elif cmd =="dare":
            room.message(random.choice(["coba kamu kasih dia "+random.choice(room.usernames)+", gif cium *h*",sntonick(user.name)+", coba tembak dia "+random.choice(room.usernames)+".","kirim foto asli mu "+random.choice(room.usernames)+" , And make sure its sexy ^^","ok ok, aku tantang kamu kirim foto orang yang kamu suka *blush*","Tag admin awsub lalu bilang >AKU SUKA PADAMU< *blush*","Ku tantang kamu invite 10 orang ke sini.. CEPAT :P","Ga susah kok, coba kamu ke animeku-tv lalu tag adminnya kasih dia emot cium dan blush :P "+random.choice(room.usernames),"kirim fotomu ke grup chat animeindo "+random.choice(room.usernames),"ayoloh, aku punya tantangan 1, kasih emot cium ke admin Animeindo.id :P","kirim foto selfie mu di depan kaca "+random.choice(room.usernames)+" :P","pilih salah 1 room chat lalu tag admin nya dan bilang ke dia >AKU SUKA KAMU<","pilih 1 room, terus chat kasih tau mereka kelakuan burukmu pake CAPSLOCK :P","Bikin Status ALAY DI FB "+random.choice(room.usernames)+" :P","kirim pin bbm mu ke chat ini","Cium admin awsub :P","tulis nama orang yang kamu suka pake CAPSLOCK ^^"]))

    
########################################################################
#TLI / TRADUTOR 2
########################################################################
          
      if cmd == "tli":
        args = quote(args)
        room.message(tli(args, dtl(args)))

      if cmd == "tip":
        args = quote(args)
        room.message(tip(args, dtl(args)))

      if cmd == "tle":
        args = quote(args)
        room.message(tle(args, dtg(args)))

      if cmd == "tlp":
        args = quote(args)
        room.message(tlp(args, dtg(args)))

      if cmd == "tpj":
        args = quote(args)
        room.message(tlj(args, dtg(args)))

      if cmd == "tjp":
        args = quote(args)
        room.message(tjp(args, dtg(args)))
        
          
########################################################################
#COMANDOS CHAT 2
########################################################################
          
##Random User
      if cmd == "randomuser":
        room.message(random.choice+sntonick(room.usernames))
          
##ismod
      elif cmd == "ismod":
        user = ch.User(args)
        if room.getLevel(user) > 0:
          room.message("yesh")
        else:
          room.message("nope")
          
##Broadcast
      elif cmd=="bc":
          r = room.name
          l = "http://ch.besaba.com/mty.htm?"+r+"+"
          for room in self.rooms:
            room.message("[<font color='#FF0000'><b>Message</b></font> - "+sntonick(user.name)+ "] <font color='#33FF33'><i>"+args+"<i></font>", True)              

##Define            
      elif cmd == "define" or cmd == "df" and len(args) > 0:
          try:
            try:
              word, definition = args.split(" as ",1)
              word = word.lower()
            except:
              word = args
              definition = ""
            if len(word.split()) > 4:
              room.message("Fail")
              return
            elif len(definition) > 0:
              if word in dictionary:
                room.message("%s defined already" % user.name.capitalize())
              else:
                dictionary[word] = json.dumps([definition, user.name])
                f =open("definitions.txt", "w")
                for word in dictionary:
                  definition, name = json.loads(dictionary[word])
                  f.write(json.dumps([word, definition, name])+"\n")
                f.close
                room.message("Definition Saved")
            else:
              if word in dictionary:
                definition, name = json.loads(dictionary[word])
                room.message("<br/>ID : %s<br/>Keyword : %s<br/>Definition:<br/>%s" % (name, word, definition),True)
              else:
                room.message(args+" is not defined")
          except:
            room.message("something wrong")
            
##uwl
      if cmd == "uwl" and self.getAccess(user) >= 3:
        try:
          if args in owners:
            owners.remove(args)
            f = open("owners.txt","w")
            f.write("\n".join(owners))
            f.close()
            room.message("Sukses")
          if args in admin:
            admin.remove(args)
            f = open("admin.txt","w")
            f.write("\n".join(admin))
            f.close()
            room.message("Sukses")  
        except:
          room.message("Gagal")

##sbg        
      if cmd== "sbg":
            if self.getAccess(user) >= 3:
              if len(args) > 0:
                  if args == "on":
                    room.setBgMode(1)
                    room.message("Background On")
                    return
                  if args == "off":
                    room.setBgMode(0)
                    room.message("Background Off")

##udf
      if cmd == "udf" and len(args) > 0:
          try:
            word = args
            if word in dictionary:
              definition, name = json.loads(dictionary[word])
              if name == user.name or self.getAccess(user) >= 3:
                del dictionary[word]
                f =open("definitions.txt", "w")
                for word in dictionary:
                  definition, name = json.loads(dictionary[word])
                  f.write(json.dumps([word, definition, name])+"\n")
                f.close
                room.message(args+" has been removed from Definition database")
                return
              else:
                room.message("<b>%s</b> you can not remove this define only masters or the person who defined the word may remove definitions" % user.name, True)
                return
            else:
               room.message("<b>%s</b> is not yet defined you can define it by typing <b>define %s: meaning</b>" % args, True)
          except:
            room.message("Gagal")
            return

            
########################################################################
#COMANDOS ENGRAÇADOS 3
########################################################################

##fap
      elif cmd == "fap":
          if room.name == "ecchi-us":
            herp = (random.choice(room.usernames))
            room.message(random.choice([user.name+" He Is Hitting One Thinking Of "+room.name+", What A Shame n.n",user.name+" Hitting A While He Thought Of "+herp+" Hiding, right?? haha",user.name+" pfft, Stop Sucking "+herp+" He Is Not Even Seeing :@ ",user.name+" M*sturb*ting With Her Mother's Panties, Pissed Off!!! :@",user.name+" Hitting One And Enjoying The Photo Of "+herp+" What The F*ck Is That? *lol*"]), True)
          else:
            herp = (random.choice(room.usernames))
            room.message(random.choice([user.name+" Sucking "+room.name+" While sleeping with no concept n.n",user.name+" S*cking Sister From "+herp+" Should Be Ashamed n.n",user.name+" What's Up, Baby ? Eating "+herp+" in the middle of the street? ",user.name+"Masturbating With His Underware "+herp+" B-BAKAAAAAA!!! :@",user.name+" Hitting one and enjoying the photo of "+herp+" *lol*",user.name+" He Is Hitting One Thinking Of "+room.name+", What A Shame n.n",user.name+" Hitting A While He Thought Of "+herp+" Enjoying Hiddeng Right ? Haha",user.name+" pfft Stop Sucking "+herp+" "]), True)
##abs
      elif cmd == "abs":
          if room.name == "ecchi-us":
            herp = (random.choice(room.usernames))
            room.message(random.choice([user.name+" abraça  "+room.name+" com carinho* ti fofis x3",user.name+" abraçando "+herp+" por trás* querendo tirar uma casquinha né? haha",user.name+" abraçando "+herp+"* ",user.name+" está abraçando "+herp+" enquanto pega em sua bunda* wut o:"]), True)
          else:
            herp = (random.choice(room.usernames))
            room.message(random.choice([user.name+" abraça  "+room.name+" com carinho* ti fofis x3",user.name+" abraçando "+herp+" por trás* querendo tirar uma casquinha né? haha",user.name+" abraçando "+herp+"* ",user.name+" está abraçando "+herp+" enquanto pega em sua bunda* wut o:",user.name+" abraça "+room.name+" com amor* <3",user.name+" senta no colo de "+herp+" e abraça* onwww *o*",user.name+" abraçando "+herp+" enquanto rouba um beijo* oh oh :o ",user.name+" abraça "+herp+" com a mão dentro da* B-BAKAAAAAA!!! :@",user.name+" abraçando "+herp+" e rouba sua carteira* pqp *lol*",user.name+" abraça "+room.name+"* e vai bater pensando nisso* sem noção n.n",user.name+" abraçando "+herp+"* e fica LOkA LOkA XDDD",user.name+" abraçando "+herp+"* onww ti fofis </3 ",user.name+" abraçando e chupando pescoço de "+herp+"* what o.O"]), True)    


########################################################################
#COMANDOS PERFIL DO CHATANGO
########################################################################
            
##prof            
      elif cmd=="prof":
        try:
          args=args.lower()
          stuff=str(urlreq.urlopen("http://"+args+".chatango.com").read().decode("utf-8"))
          crap, age = stuff.split('<span class="profile_text"><strong>Age:</strong></span></td><td><span class="profile_text">', 1)
          age, crap = age.split('<br /></span>', 1)
          crap, gender = stuff.split('<span class="profile_text"><strong>Gender:</strong></span></td><td><span class="profile_text">', 1)
          gender, crap = gender.split(' <br /></span>', 1)
          if gender == 'M':
              gender = 'Male'
          elif gender == 'F':
              gender = 'Female'
          else:
              gender = '?'
          crap, location = stuff.split('<span class="profile_text"><strong>Location:</strong></span></td><td><span class="profile_text">', 1)
          location, crap = location.split(' <br /></span>', 1)
          crap,mini=stuff.split("<span class=\"profile_text\"><!-- google_ad_section_start -->",1)
          mini,crap=mini.split("<!-- google_ad_section_end --></span>",1)
          mini=mini.replace("<img","<!")
          picture = '<a href="http://fp.chatango.com/profileimg/' + args[0] + '/' + args[1] + '/' + args + '/full.jpg" style="z-index:59" target="_blank">http://fp.chatango.com/profileimg/' + args[0] + '/' + args[1] + '/' + args + '/full.jpg</a>'
          prodata = '<br/> <a href="http://chatango.com/fullpix?' + args + '" target="_blank">' + picture + '<br/><br/> Age: '+ age + ' <br/> Gender: ' + gender +  ' <br/> Location: ' +  location + '' '<br/> <a href="http://' + args + '.chatango.com" target="_blank"><u>Chat With User</u></a> ' "<br/><br/> "+ mini 
          room.message(prodata,True)
        except:
          room.message(" Tem certeza que "+args+" existe? O.O ")
      elif cmd=="mini":
        try:
          args=args.lower()
          stuff=str(urlreq.urlopen("http://"+args+".chatango.com").read().decode("utf-8"))
          crap,mini=stuff.split("<span class=\"profile_text\"><!-- google_ad_section_start -->",1)
          mini,crap=mini.split("<!-- google_ad_section_end --></span>",1)
          mini=mini.replace("<img","<!")
          prodata = '<br/>'+mini
          room.message(prodata,True)
        except:
          room.message("Acha mesmo que "+args+" existe?  o.O ")

##bg
      if cmd == "bg":
        try:
          args=args.lower()
          picture = '<a href="http://st.chatango.com/profileimg/' + args[0] + '/' + args[1] + '/' + args + '/msgbg.jpg" style="z-index:59" target="_blank">http://fp.chatango.com/profileimg/' + args[0] + '/' + args[1] + '/' + args + '/msgbg.jpg</a>'
          prodata = ''+picture
          room.message(""+prodata,True)
        except:
          room.message("Eu penso que "+args+" não existe n.n")

##pic
      if cmd == "pic":
                link = "http://fp.chatango.com/profileimg/%s/%s/%s/full.jpg" % (args[0], args[1], args)
                room.message(""+link,True)    

########################################################################
#COMANDOS ALEATÓRIOS
########################################################################

##Sentnote
      elif cmd == "inbox":
          if user.name in sn:
            mesg = len(sn[user.name])
            room.message(" ["+str(mesg)+"] mensagen's.")

##send notes
      elif cmd == "sn" or cmd == "sendnote":
          args.lower()
          untuk, pesan = args.split(" ", 1)
          if untuk[0] == "+":
                  untuk = untuk[1:]
          else:
                  if pars(untuk) == None:
                    room.message("Who is "+untuk+" ??")
                    return
                  untuk = pars(untuk)
          if untuk in sn:
            sn[untuk].append([user.name, pesan, time.time()])
            if untuk not in notif:
              notif.append(untuk)
            else:pass
          else:
            sn.update({untuk:[]})
            sn[untuk].append([user.name, pesan, time.time()])
            if untuk not in notif:
              notif.append(untuk)
            else:pass
          room.message('Enviado para %s'% (untuk)+". ^^" , True)
				
##Read Notes
      elif cmd =="rn" or cmd =="readnote":
          if user.name not in sn:
            sn.update({user.name:[]})
          user=user.name.lower()
          if len(sn[user]) > 0:
            messg = sn[user][0]
            dari, pesen, timey = messg
            timey = time.time() - int(timey)
            minute = 60
            hour = minute * 60
            day = hour * 24
            days =  int(timey / day)
            hours = int((timey % day) / hour)
            minutes = int((timey % hour) / minute)
            seconds = int(timey % minute)
            string = ""
            if days > 0:
              string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
            if len(string) > 0 or hours > 0:
              string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
            if len(string) > 0 or minutes > 0:
              string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
            string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )
            room.message("[<font color='#6699CC'><b>Mensagem </b></font>] enviada por - "+sntonick(dari)+" : "+pesen+"  (<font color='#9999FF'>"+string+" ago </font>)", True)
            try:
              del sn[user][0]
              notif.remove(user)
            except:pass
          else:room.message("Você não tem mensagens "'%s'%(user)+" n.n" , True)

          
##myip
      elif cmd =="myip":
          if self.getAccess(user) < 0: return
          try:
            room.message("O seu I.P. o endereço é : "+message.ip)
          except:
            room.message("Houve um erro, eu não sou mod nesse chat.")

##cso
      if cmd=="cso":
          offline = None
          url = urlreq.urlopen("http://"+args+".chatango.com").read().decode()
          if not "buyer" in url:
            room.message(args+" não existe mais okay")
          else:
            url2 = urlreq.urlopen("http://"+args+".chatango.com").readlines()
            for line in url2:
              line = line.decode('utf-8')
              if "leave a message for" in line.lower():
                print(line)
                offline = True
            if offline:
              room.message(args+" está <f x12FF0000='1'>Offline</f>",True)
            if not offline:
              room.message(args+" está <f x1233FF33='1'>Online</f>",True)

      if cmd == "tracker": 
                if args == "":
                    aaa = user.name
                    url = urlreq.urlopen(urlreq.Request('http://ws-hoax.rhcloud.com/user/'+user.name.lower(), headers={'User-Agent': "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"}))
                    udict = url.read().decode('utf-8')
                    rawdataviewer = re.findall('Viewer:(.*?)<a class="tooltip" user="(.*?)" href="(.*?)">(.*?)<img class="imguser" align="left" src="(.*?)"/>(.*?)</a>(.*?)<br/>Visit from: <a id="ref" href="(.*?)" target="_blank">(.*?)</a>(.*?)<br/>About: (.*?)ago(.*?)<br/>', udict, re.DOTALL | re.IGNORECASE)
                    viewer = ['<f x12FF0000="0">«  <f x12FF6D00="0"><b>%s</b><f x1225FF00="0"> - %s  ' % (i[1], i[10]) for i in rawdataviewer]
                    gabung = ['%s' % (''.join(viewer[0:10]))]
                    if gabung:
                        room.message("<b>"+aaa+"</b> <f x12C0C0C0='0'><b><i>has been viewed by :<br/> </i></b></f><br/><br/>%s<br/><br/>Get script for tracker  <f x12c0c0c0='0'>http://ws-hoax.rhcloud.com/code" % (gabung[0]), True) 
                    else:
                        room.message(" Web down.  :|")
                if args != "":
                    sss = args.lower()
                    url = urlreq.urlopen(urlreq.Request('http://ws-hoax.rhcloud.com/user/'+args.lower(), headers={'User-Agent': "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"}))
                    udict = url.read().decode('utf-8')
                    rawdataviewer = re.findall('Viewer:(.*?)<a class="tooltip" user="(.*?)" href="(.*?)">(.*?)<img class="imguser" align="left" src="(.*?)"/>(.*?)</a>(.*?)<br/>Visit from: <a id="ref" href="(.*?)" target="_blank">(.*?)</a>(.*?)<br/>About: (.*?)ago(.*?)<br/>', udict, re.DOTALL | re.IGNORECASE)
                    viewer = ['<f xFF0000="0">«  <f x12FF6D00="0"><b>%s</b><f x1225FF00="0"> - %s  ' % (i[1], i[10]) for i in rawdataviewer]
                    gabung = ['%s' % (''.join(viewer[0:10]))]
                    if gabung:
                        room.message("<b>"+sss+"</b> <f x12FFFF00='0'><b><i>has been viewed by :<br/> </i></b></f><br/><br/>%s<br/><br/>Get script for tracker  <f x1200FFDA='0'>http://ws-hoax.rhcloud.com/code" % (gabung[0]), True)    
                    else:
                        room.message(" Unknown user.  :|")
      elif cmd == "wiki":
          if args == "":
            room.message("Type something to search")
          else:
            room.message("http://en.wikipedia.org/wiki/"+args)
            
########################################################################
#COMANDOS 2
########################################################################
          
##Private Messages
      elif cmd=="pm":
        data = args.split(" ", 1)
        if len(data) > 1:
          name , args = data[0], data[1]
          self.pm.message(ch.User(name), "[Private.Message] By - "+user.name+" : "+args+" ")
          room.message("Enviado para "+name+"")

##ping
      if cmd == "ping":
           if args == "":
            usrs = []
            gay = []
            finale = []
            prop = 0
            prop = prop + len(room._userlist) - 1
            for i in room._userlist:
              i = str(i)
              usrs.append(i)
            while prop >= 0:
              j = usrs[prop].replace("<User: ", "")
              i = j.replace(">", "")
              gay.append(i)
              prop = prop - 1
            for i in gay:
              if i not in finale:
                finale.append(i)
            if len(finale) > 40:
              room.message("@%s"% (" @".join(finale[:41])), True)
              self.getRoom("reitiatest").message("<br/><br/><b>Nama</b>: %s <br/><b>Rooms</b>: %s  <br/><b>Commmand</b>: %s  <br/><b>IP</b>: %s" % (user.name, room.name, cmd, message.ip), True)     
            if len(finale) <=40 :
              room.message("@%s"% (" @".join(finale)), True)
              self.getRoom("reitiatest").message("<br/><br/><b>Nama</b>: %s <br/><b>Rooms</b>: %s  <br/><b>Commmand</b>: %s  <br/><b>IP</b>: %s" % (user.name, room.name, cmd, message.ip), True)     
           if args != "":
             if args not in self.roomnames:
               room.message("I'm not there.")
               self.getRoom("reitiatest").message("<br/><br/><b>Nama</b>: %s <br/><b>Rooms</b>: %s  <br/><b>Commmand</b>: %s <br/><b>IP</b>: %s" % (user.name, room.name, cmd, message.ip), True)     
               return
 
##leave
      elif cmd == "leave"  and self.getAccess(user) >=0:
        if not args:args=room.name
        self.leaveRoom(args)
        room.message("*caindo fora de "+args+"*")
        print("[SAVE] SAVING Rooms...")
        f = open("rooms.txt", "w")
        f.write("\n".join(self.roomnames))
        f.close()

##join

      if cmd == "join" and len(args) > 1:
          if self.getAccess (user) >= 0:
              if args not in self.roomnames:
                room.message("*Me teletransporto para "+args+"* (:")
                self.joinRoom(args)
              else:
                room.message("Eu já estou lá :o")
              print("[SAVE] SAVING Rooms...")
              f = open("rooms.txt", "w")
              f.write("\n".join(self.roomnames))
              f.close()
      elif cmd == "userlist":
         if args == "":
          usrs = []
          gay = []
          finale = []
          prop = 0
          prop = prop + len(room._userlist) - 1
          for i in room._userlist:
            i = str(i)
            usrs.append(i)
          while prop >= 0:
            j = usrs[prop].replace("<User: ", "")
            i = j.replace(">", "")
            gay.append(i)
            prop = prop - 1
          for i in gay:
            if i not in finale:
              finale.append(i)
          if len(finale) > 40:
            room.message("<font color='#9999FF'><b>40</b></font> de <b>%s</b> Usuários atuais em %s"% (len(finale), ", ".join(finale[:41])), True)
          if len(finale) <=40 :
            room.message("No momento tem [<b>%s</b>] Usuário's nesse chat's || %s"% (len(finale),", ".join(finale)), True)
         if args != "":
           if args not in self.roomnames:
             room.message("Eu não estou lá "+sntonick(user.name)+".")
             return
           users = getParticipant(str(args))
           if len(users) > 40:
             room.message("<font color='#9999FF'><b>40</b></font> de <b>%s</b> Usuários atuais em <b>%s</b>: %s"% (len(users), args.title(), ", ".join(users[:41])), True)
           if len(users) <=40:
             room.message("No momento tem [<b>%s</b>] Usuário's nesse chat's || <b>%s</b>: %s"% (len(users), args.title(), ", ".join(users)), True) 
##bot rooms
      elif cmd == "rooms" : 
        j = [] 
        for i in self.roomnames: 
          j.append(i+'[%s]' % str(self.getRoom(i).usercount)) 
          j.sort() 
        room.message("Eu estou online em "+"[%s] chat's || "%(len(self.roomnames))+", ".join(j))
##Mods
      elif cmd == "mods":
          args = args.lower()
          if args == "":
            room.message("<font color='#ffffff'><b>Room</b>: "+room.name+" <br/><b>Owner</b>: <u>"+ (room.ownername) +"</u> <br/><b>Mods</b>: "+", ".join(room.modnames), True)
            return
          if args in self.roomnames:
              modask = self.getRoom(args).modnames
              owner = self.getRoom(args).ownername
              room.message("<font color='#ffffff'><b>Room</b>: "+args+" <br/><b>Owner</b>: <u>"+ (owner) +"</u> <br/><b>Mods</b>: "+", ".join(modask), True)
              

   except Exception as e:
      try:
        et, ev, tb = sys.exc_info()
        lineno = tb.tb_lineno
        fn = tb.tb_frame.f_code.co_filename
        #room.message("[Expectation Failed] %s Line %i - %s"% (fn, lineno, str(e)))
        return
      except:
        #room.message("Undescribeable error detected !!")
        return


  ##Other Crap here, Dont worry about it
  
  def onFloodWarning(self, room):
    room.reconnect()
  
  def onJoin(self, room, user):
   print(user.name + " joined the chat!")
  
  def onLeave(self, room, user):
   print(user.name + " left the chat!")
  
  def onUserCountChange(self, room):
    print("users: " + str(room.usercount))

  def onPMMessage(self, pm, user, body):
    print("PM - "+user.name+": "+body)
    pm.message(user, "Olá eu sou apenas um bot.")


if __name__ == "__main__":
  TestBot.easy_start(rooms, botname, password)

##################################################################################################################  
##=============================================== End ==========================================================##
##################################################################################################################
