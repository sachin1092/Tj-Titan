from mpd import MPDClient

import sys

class Spotify(object):
    def __init__(self):
        self.client = MPDClient()
        self.client.timeout = 10
        self.client.idletimeout = None

    def connect(self):
        self.client.connect("localhost", 6600)

    def isConnected(self):
        try:
            self.client.currentsong()
        except:
            return False
        return True

    # This is needed because the connection to mpd is very inconsistent
    def connectIfNC(self):
        if not self.isConnected():
            self.connect()

    def playSong(self, song_name):
        self.connectIfNC()
        self.client.clear()
        self.connectIfNC()
        self.client.searchadd("any", song_name)
        self.connectIfNC()
        print(self.client.playlistinfo())
        try:
            self.client.play(0)
        except:
            self.playLibrary()

    def toggleMusic(self):
        self.connectIfNC()
        state = self.client.status().get('state', 'pause')
        self.connectIfNC()
        self.client.pause(1 if state == 'play' else 0)

    def next(self):
        self.connectIfNC()
        self.client.next()

    def stop(self):
        self.connectIfNC()
        self.client.stop()

    # seek to exact time in seconds
    def seekTo(self, time):
        self.connectIfNC()
        self.client.seekcur(time)

    # seek relative to current location in song
    def seek(self, time):
        self.connectIfNC()
        self.client.seekcur(int(float(self.client.status().get('elapsed'))) + time)

    # volume in range [0, 100]
    def setVol(self, vol):
        self.connectIfNC()
        self.client.setvol(vol)

    def playLibrary(self, playlist=None):
        playlist = playlist if playlist else "Greatest Hits Ever (by playlistmeukfeatured)"
        self.connectIfNC()
        self.client.stop()
        self.connectIfNC()
        self.client.clear()
        self.connectIfNC()
        self.client.load(playlist)
        self.connectIfNC()
        self.client.play(0)


if __name__ == '__main__':
    spotify = Spotify()

    while True:
        try:
            try:
                print "\n\nMenu:\n1. Play Song\n2. Pause/Play \n3. Skip \n4. Seek \n5. Stop \n6. Play Library \nElse: Exit"
                choice = int(raw_input("Choice: "))
                if choice == 1:
                    spotify.playSong(raw_input("\n\nEnter Song name: "))
                elif choice == 2:
                    spotify.toggleMusic()
                elif choice == 3:
                    spotify.next()
                elif choice == 4:
                    spotify.seek(int(raw_input("Enter time in seconds: ")))
                elif choice == 5:
                    spotify.stop()
                elif choice == 6:
                    spotify.playLibrary()
                else:
                    print 'exit'
                    sys.exit(0)
            except KeyboardInterrupt:
                sys.exit(0)
        except:
            pass
