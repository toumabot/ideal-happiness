import sys
if sys.version_info[0] < 3:
  class urllib:
    request = __import__("urllib2")
else:
  import urllib.request

import json
import random
 
global bahasa, key
key = "0a81c816-b9b9-491e-b8f7-d40fc5df5949" #### KASIH KEY LU #######
bahasa = "id"
 
def set(x):
    global bahasa
    bahasa = x
   
def simi(kalimat):
    a = random.choice(["Hmmm?","Kenapa kak?","Iya kak","Oke deh kak"])
    kata = kalimat.replace(" ","+")
    try:
        data = urllib.request.urlopen("http://sandbox.api.simsimi.com/request.p?key=%s&lc=%s&ft=1.0&text=%s" % (key, bahasa, kata)).read().decode('utf-8')
        jsondata = json.loads(data)
        respon = jsondata["response"]
        if "I HAVE NO RESPONSE" in respon:
            respon = a
    except Exception as e:
        respon = random.choice(["Hmmm?","Kenapa kak?","Iya kak","Oke deh kak"])
    return respon
