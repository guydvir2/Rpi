import requests
url = 'https://maps.googleapis.com/maps/api/geocode/json'
params = {'sensor': 'false', 'address': 'Eilat, Il'}
r = requests.get(url, params=params)
results = r.json()['results']
location = results[0]['geometry']['location']
print(location['lat'], location['lng'])

#print (location)