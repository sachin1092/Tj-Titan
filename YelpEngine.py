import requests
from constants import yelp_creds

baseurl = yelp_creds.get("baseurl")
businessurl = yelp_creds.get("businessurl")
header = yelp_creds.get("header")

#Location can be city name, address, zip code
def getRestaurantsByLocation(location, category=''):
    if category == '':
        url = baseurl + '&location=' + location
    else:
        url = baseurl + '&location=' + location + '&categories=' + category
    r = requests.get(url, headers=header)
    resp = r.json()

    response = ''

    if 'businesses' in resp:
        for item in resp['businesses']:
            response += item['name'] + ', '
    return response

def getRestaurantsByCoord(latitude, longitude, category = ''):
    if category == '':
        url = baseurl + '&latitude=' + latitude + '&longitude=' + longitude
    else:
        url = baseurl + '&latitude=' + latitude + '&longitude=' + longitude + '&categories=' + category
    r = requests.get(url, headers=header)
    resp = r.json()

    resp = ''
    if 'businesses' in resp:
        for item in resp['businesses']:
            resp += item['name'] + ', '
    return resp

def getRestaurantTimings(businessid):
    url = businessurl + businessid

    r = requests.get(url, headers=header)
    resp = r.json()

    if 'hours' in resp:
        print resp['hours']

if __name__ == '__main__':
    getRestaurantsByLocation('Gracy Farms Ln')
    getRestaurantsByLocation('78758','indpak')
    getRestaurantsByCoord('30.38','-97.7')
    getRestaurantTimings('halal-bros-austin-3')
