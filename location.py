from __future__ import print_function
import re
import requests
from constants import location_creds

URL1 = location_creds.get('url_1')
URL2 = location_creds.get('url_2')

def getLatLng(address):
    address = re.sub("\s+", "+", address.strip())
    url = URL1 + address + URL2
    r = requests.get(url)
    data = r.json()
    results = data.get("results", [])
    if len(results) > 0:
        loc = results[0].get("geometry", {}).get("location", {})
	return loc.get("lat"), loc.get("lng")
    return 0, 0

def getAddress(lat, lng):
    loc = str(lat) + "," + str(lng)
    loc = re.sub("\s+", "+", loc.strip())
    
    url = URL1 + loc + URL2
    
    r = requests.get(url)
    data = r.json()

    results = data.get("results", [])

    if len(results) > 0:
        addresses = results[0].get("address_components", [])
    
        toRet = "";
    
        subl, local, country, admin1, admin2 = "", "", "", "", ""
        for address in addresses:
            types = address.get("types", [])
            check = types[0] if len(types) > 0 else "" 
            if check =="sublocality":
                subl = address.get("long_name", "")
            if check == "locality":
                local = address.get("long_name", "")
            if check == "country":
                country = address.get("long_name", "")
            if check == "administrative_area_level_2":
                admin2 = address.get("long_name", "")
            if check == "administrative_area_level_1":
                admin1 = address.get("long_name", "")

        if len(subl):
            toRet = subl

        if len(toRet) and len(local):
            toRet = toRet + ", " + local
        elif len(local):
            toRet = local

        if not len(subl) and len(admin2):
            if admin2 != local:
                if not len(toRet):
                    toRet = admin2
                else:
                    toRet = toRet + ", " + admin2

        if not len(local) and len(admin1):
            if admin1 != admin2 and admin1 != subl:
                if not len(toRet):
                    toRet = admin1
                else:
                    toRet = toRet + ", " + admin1

        if len(toRet) and len(country):
            if country != admin2 and country != subl and country != admin1 and country != local:
                toRet = toRet + ", " + country
        elif len(country):
            toRet = country
        
        return toRet

class Location(object):
    def __init__(self, lat=None, lng=None, address=None):
        if (lat and lng) and (not address):
           self.lat = lat
           self.lng = lng
           self.address = getAddress(lat, lng)
        elif not (lat or lng) and address:
           self.lat, self.lng = getLatLng(address)
           self.address = address
        if (lat and lng) and address:
           self.lat = lat
           self.lng = lng
           self.address = address

    def get_latlng(self):
        return self.lat, self.lng

    def get_address(self):
        return self.address

    def set_latlng(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def set_address(self, address):
        self.address = address
       

if __name__ == '__main__':
    loc1 = Location(address="Austin")
    print(loc1.get_latlng(), loc1.get_address())

    loc2 = Location(lat=30.316, lng=78.032)
    print(loc2.get_latlng(), loc2.get_address())
