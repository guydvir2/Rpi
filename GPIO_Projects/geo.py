import requests
import json

send_url = 'http://freegeoip.net/json'
r = requests.get(send_url)
j = json.loads(r.text)
lat = j['latitude']
lon = j['longitude']

print ( lat, lon )



freegeoip = "http://freegeoip.net/json"
geo_r = requests.get(freegeoip)
geo_json = geo_r.json()

user_postition = [geo_json["latitude"], geo_json["longitude"]]

print(user_postition)


import geocoder
g = geocoder.ip('me')
print(g.latlng)


