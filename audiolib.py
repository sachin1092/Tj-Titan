import pyaudio
import wave
from utils import resource_path

class AudioFile(object):
    chunk = 1024

    def __init__(self, file=None, file_data=None):
        """ Init audio stream """
        if file:
            self.wf = wave.open(file, 'rb')
        else:
            self.wf = wave.open(file_data, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.p.get_format_from_width(self.wf.getsampwidth()),
            channels=self.wf.getnchannels(),
            rate=self.wf.getframerate(),
            output=True
        )

    def play(self):
        """ Play entire file """
        data = self.wf.readframes(self.chunk)
        while data:
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)

    def close(self):
        """ Gracefully close the file """
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

if __name__ == '__main__':
    audio_file = AudioFile(file=resource_path('assets/beep.wav'))
    audio_file.play()
    audio_file.close()
