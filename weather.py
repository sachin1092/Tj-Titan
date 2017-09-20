import requests
import sys
from location import Location
from constants import weather_creds

condition_map = ["Tornado",
"Tropical Storm",
"Hurricane",
"Strong Storms",
"Thunder and Hail",
"Rain to Snow Showers",
"Rain",
"Sleet",
"Freezing Drizzle",
"Drizzle",
"Freezing Rain",
"Light Rain",
"Rain",
"Scattered Flurries",
"Light Snow",
"Drifting Snow",
"Snow",
"Hail",
"Sleet",
"Sandstorm",
"Foggy",
"Haze",
"Smoke",
"Breezy",
"Windy",
"Frigid",
"Cloudy",
"Mostly Cloudy",
"Mostly Cloudy",
"Partly Cloudy",
"Partly Cloudy",
"Clear",
"Sunny",
"Mostly Clear",
"Mostly Sunny",
"Mixed Rain & Hail",
"Hot",
"Isolated Thunderstorms",
"Thunderstorms",
"Scattered Showers	",
"Heavy Rain",
"Scattered Snow Showers	",
"Heavy Snow",
"Blizzard",
None,
"Scattered Showers",
"Scattered Snow Showers",
"Scattered Thunderstorms"]

url = weather_creds.get("url")

def getCurrentWeather(location, temp_unit="F"):
	lat, lng = location.get_latlng()
	r = requests.get(url + "/api/weather/v1/geocode/" + str(lat) + "/" + str(lng) + "/observations.json?language=en-US")
	data = r.json()
	observation = data.get("observation", {})
	condition = condition_map[int(observation.get("wx_icon", 56))]
	temperature = observation.get("temp", None)
	if condition and temperature:
		return  "Currently in " + location.get_address() + ", it's " + condition \
		+ " with a temperature of " + \
		((str(temperature) + " degree fahrenheit.") if temp_unit.upper() == "F" else str((int(temperature) - 32) * 0.5556) + " degree celsius.")
	elif condition:
		return  "Currently in " + location.get_address() + ", it's " + condition
	elif temperature:
		return  "Currently in " + location.get_address() + ", it's " + \
		((str(temperature) + " degree fahrenheit.") if temp_unit.upper() == "F" else str((int(temperature) - 32) * 0.5556) + " degree celsius.")
	else:
		return "I am sorry, I couldn't get weather."

def getWeatherForTomorrow(location, temp_unit="F"):
	lat, lng = location.get_latlng()
	r = requests.get(url + "/api/weather/v1/geocode/" + str(lat) + "/" + str(lng) + "/forecast/daily/3day.json")
	data = r.json()
	forecasts = data.get("forecasts", [])
	if len(forecasts) >= 2:
		observation = forecasts[1]
		return "Tomorrow in " + location.get_address() + " it's " + observation["narrative"]
	else:	
		return "I am sorry, I couldn't get weather."

def getRainToday(location):
	lat, lng = location.get_latlng()
	r = requests.get(url + "/api/weather/v1/geocode/" + str(lat) + "/" + str(lng) + "/observations.json?language=en-US")
	data = r.json()
	observation = data.get("observation", {})
	rain = observation.get("precip_total", 0)
	rain = rain if rain else 0
	return "No, rain is not expected today in " + location.get_address() if int(rain) <= 0 \
		else "Yes, rain is expected today in " + location.get_address()


def getRainTomorrow(location):
	lat, lng = location.get_latlng()
	r = requests.get(url + "/api/weather/v1/geocode/" + str(lat) + "/" + str(lng) + "/forecast/daily/3day.json")
	data = r.json()
	forecasts = data.get("forecasts", [])
	if len(forecasts) >= 2:
		observation = forecasts[1]
		rain = True if ("rain" in observation.get("night", {}).get("narrative", "") or "rain" in observation.get("day", {}).get("narrative", "")) else False
		return "Yes, rain is expected tomorrow in " + location.get_address() if rain \
		else "No, rain is not expected tomorrow in " + location.get_address()
	else:
		return "No, rain is not expected tomorrow in " + location.get_address()



if __name__ == '__main__':
	# print(getCurrentWeather(Location(33.40, -83.42)))
	# print(getWeatherForTomorrow(Location(33.40, -83.42)))
	# print(getRainToday(Location(33.40, -83.42)))
	# print(getRainTomorrow(Location(33.40, -83.42)))
	# print("********")
	# print(getCurrentWeather(Location(30.267153, -97.7430608)))
	# print(getWeatherForTomorrow(Location(30.267153, -97.7430608)))
	# print(getRainToday(Location(30.267153, -97.7430608)))
	# print(getRainTomorrow(Location(30.267153, -97.7430608)))
	# print("********")
	# print(getCurrentWeather(Location(18.5204, 73.8567)))
	# print(getWeatherForTomorrow(Location(18.5204, 73.8567)))
	# print(getRainToday(Location(18.5204, 73.8567)))
	# print(getRainTomorrow(Location(18.5204, 73.8567)))

	print(getCurrentWeather(Location(address='san francisco')))
