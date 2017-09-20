import json
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3
from constants import vr_creds

visual_recognition = VisualRecognitionV3(vr_creds.get("version"), api_key=vr_creds.get("api_key"))

def classifyImage(filename):
    with open(filename) as fileinfo:
        res = visual_recognition.classify(images_file=fileinfo, classifier_ids='TJ_Titans_775279133')
        print json.dumps(res, indent = 2)

if __name__ == '__main__':
    classifyImage('husky.jpg')
