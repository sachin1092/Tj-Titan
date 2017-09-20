import picamera
import os
from time import sleep
import subprocess

image_directory="files/images"
video_directory="files/videos"

def capture_image():
    camera = picamera.PiCamera()
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)
    i = 0
    while os.path.exists(image_directory + '/' + 'image_' + str(i) + '.jpg'):
        i += 1
    subprocess.Popen(["python", "audiolib.py", "assets/shutter.wav"] , stdout=subprocess.PIPE)
    camera.capture(image_directory + '/' + 'image_' + str(i) + '.jpg')
    print "capturing image"
    return image_directory + '/' + 'image_' + str(i) + '.jpg'

def capture_video(time=10):
    camera = picamera.PiCamera()
    if not os.path.exists(video_directory):
        os.makedirs(video_directory)
    i = 0
    while os.path.exists(video_directory + '/' + 'video_' + str(i) + '.h264'):
        i += 1
    subprocess.Popen(["python", "audiolib.py", "assets/video.wav"] , stdout=subprocess.PIPE)
    camera.start_recording(video_directory + '/' + 'video_' + str(i) + '.h264')
    sleep(time)
    camera.stop_recording()
    return video_directory + '/' + 'video_' + str(i) + '.h264'


if __name__ == '__main__':
    #capture_image()
    capture_video()
