## Convert Adress to Lat-Long & Vice Versa

import certifi
import ssl
import geopy.geocoders
from geopy.geocoders import Nominatim


ctx = ssl.create_default_context(cafile = certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

address = "1540 East 82nd Place"

## Create GeoLocator Object
geolocator = Nominatim(scheme='http')

## For Address to Lat-Long
location = geolocator.geocode(address)

## For Lat-long to Address
##      location = geolocator.geocode(lat, long)

print("on round 1: ", location.address)
lat = location.raw['lat']
long = location.raw['lon']
print(lat)
print(long)
coords = str(lat) + ", " + str(long)

#location = geolocator.reverse(coords)

#print("On round 2: ", location.address)
