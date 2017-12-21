import geocoder

g1=geocoder.ip('213.57.240.163')
g2=geocoder.ip('me')
print(g1.latlng)
print(g2.latlng)