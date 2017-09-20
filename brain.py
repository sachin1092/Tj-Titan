from __future__ import print_function

from ConversationEngine import getConversationResponse
from YelpEngine import getRestaurantsByLocation, getRestaurantTimings
from weather import getCurrentWeather, getWeatherForTomorrow
from TranslatorEngine import translateSentence
try:
    from camera import capture_image, capture_video
except:
    pass
from drive import upload_and_delete
from spotify import Spotify
from location import Location
import subprocess
import time
import sys

currentLocation = 'Austin'
player = Spotify()

def say(phrase, voicemodel = 'en-US_AllisonVoice'):
    subprocess.Popen(["python", "watson_tts.py", phrase, voicemodel] , stdout=subprocess.PIPE)

def handle_results(data):
    print("\n\n^^^^^^^^")
    print(data)
    response = getConversationResponse(data[0])
    parseConvResponse(response)
    print("^^^^^^^^\n\n")

def parseConvResponse(response):
    intents = response['intents']
    print("*"*50)
    print(intents)
    print("*"*50)   
    if len(intents):
        intent = intents[0]['intent']
        entities = response['entities']
        query = response['input']['text']

        if intent == 'PLAY_MUSIC':
            query = query.lower()
            for entity in entities:
                if entity['entity'] == 'STOP_WORDS':
                    query = query.replace(entity['value'],'')
            playMusic(query.strip())

        elif intent == 'GET_RESTAURANTS':
            location = currentLocation
            category = ''
            for entity in entities:
                if entity['entity'] == 'sys-location':
                    location = entity['value']
                elif entity['entity'] == 'RESTAURANT_TYPE':
                    category = entity['value']
            getYelpResponse(location, category)

        elif intent == 'WEATHER_REPORT':
            day = ''
            location = currentLocation
            for entity in entities:
                if entity['entity'] == 'day':
                    day = entity['value']
                elif entity['entity'] == 'sys-location':
                    location = entity['value']
            getWeatherReport(location, day)

        elif intent=='TRANSLATE':
            query = query.lower()
            voicemodel = ''
            destLang = ''
            for entity in entities:
                if entity['entity'] == 'STOP_WORDS':
                    query = query.replace(entity['value'],'')
                elif entity['entity'] == 'TTS_VOICE':
                    voicemodel = entity['value']
                    query = query.replace(entity['value'],'')
                elif entity['entity'] == 'TRANSLATOR_DEST':
                    destLang = entity['value']
                elif entity['entity'] == 'LANGUAGE':
                    query = query.replace(entity['value'],'')
            if destLang != '':
                getTranslation(query, destLang, voicemodel)

        elif intent=='CAPTURE_IMAGE':
            captureImage()

        elif intent=='RECORD_VIDEO':
            captureVideo()

        else:
            say("Sorry, I need an upgrade to answer that.")
    else:
        say("Sorry, I need an upgrade to answer that.")

def captureImage():
    try:
        image = capture_image()
        print("uploading: " + str(image))
        upload_and_delete(image)
        say('Image was captured and saved to google drive')
    except Exception as e:
        print(e) 
        say("Sorry, I could not capture picture at the moment")

def captureVideo():
    try:
        video = capture_video()
        upload_and_delete(video, 'video')
        say('Ten seconds of video has been captured and saved to google drive')
    except Exception as e:
        print(e)
        say("Sorry, I could not capture picture at the moment")

def getTranslation(query, destLang, voicemodel):
    try:
        translation = translateSentence(query, 'en', destLang)
        say(translation, voicemodel)
    except Exception as e:
        say("Sorry, I couldn't understand your request, would you like to try again?")

def getYelpResponse(location, category):
    try:
        restaurants = getRestaurantsByLocation(location, category)
        response = 'Here are the list of top 5 ' + category + ' restaurants. ' + restaurants
        print(response)
        say(response)
    except Exception as e:
        print(e)
        say("Sorry, I couldn't understand your request, would you like to try again?")

def getWeatherReport(location, day):
    try:
        loc1 = Location(address=location)
        report = ''
        if day == 'tomorrow':
            report = getWeatherForTomorrow(loc1)
        else:
            report = getCurrentWeather(loc1)
        print(report)

        say(report)
    except Exception as e:
        print(e)
        say("Sorry, I couldn't understand your request, would you like to try again?")

def playMusic(song):
    try:
        player.playSong(song)
        time.sleep(10)
        player.stop()
    except Exception as e:
        print(e)
        say("Sorry, I couldn't understand your request, would you like to try again?")

if __name__ == '__main__':
    print(sys.argv)
    import json
    if len(sys.argv) >= 2:
        handle_results(json.loads(sys.argv[1]))
