import io
import sys

from watson_developer_cloud import TextToSpeechV1

from audiolib import AudioFile
from constants import watson_tts_credentials


def say(phrase, voicemodel = 'en-US_AllisonVoice'):
    text_to_speech = TextToSpeechV1(
        username=watson_tts_credentials['username'],
        password=watson_tts_credentials['password'],
        x_watson_learning_opt_out=True)

    audio_file = AudioFile(file_data=io.BytesIO(
        text_to_speech.synthesize(phrase,
                                  accept='audio/wav',
                                  voice=voicemodel)))

    audio_file.play()
    audio_file.close()


if __name__ == '__main__':
    say(sys.argv[1], sys.argv[2])
