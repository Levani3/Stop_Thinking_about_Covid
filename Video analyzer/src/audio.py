
import io
from moviepy.editor import *
from pydub import AudioSegment

from google.cloud import vision, speech_v1
from google.cloud.speech_v1p1beta1 import enums
from google.cloud import speech_v1 as speech



######################
#MODUL AUDIO
#####################

def speech_to_text(config, audio):

    client = speech.SpeechClient()
    response = client.recognize(config, audio)
    print_sentences(response)

def print_word_offsets(alternative):
    for word in alternative.words:
        start_ms = word.start_time.ToMilliseconds()
        end_ms = word.end_time.ToMilliseconds()
        word = word.word

        print(f'{start_ms/1000:>7.3f}',
            f'{end_ms/1000:>7.3f}',
            f'{word}',
            sep=' | ')

def print_sentences(response):
    for result in response.results:
        best_alternative = result.alternatives[0]
        transcript = best_alternative.transcript
        confidence = best_alternative.confidence
        print('-' * 80)
        print(f'Transcript: {transcript}')
        print(f'Confidence: {confidence:.0%}')
        print_word_offsets(best_alternative)

def sample_recognize(local_file_path):
        """
        Transcribe a short audio file using synchronous speech recognition

        Args:
          local_file_path Path to local audio file, e.g. /path/audio.wav
        """
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/pol/Desktop/GCV/credentials/credentials.json'
        client = speech_v1.SpeechClient()

        # local_file_path = 'resources/brooklyn_bridge.raw'

        # The language of the supplied audio
        language_code = "es-ES"

        # When enabled, the first result returned by the API will include a list
        # of words and the start and end time offsets (timestamps) for those words.
        enable_word_time_offsets = True

        # Sample rate in Hertz of the audio data sent
        sample_rate_hertz = 44100

        # Encoding of audio data sent. This sample sets this explicitly.
        # This field is optional for FLAC and WAV audio formats.
        encoding = enums.RecognitionConfig.AudioEncoding.FLAC
        config = {
            "enable_word_time_offsets": enable_word_time_offsets,
            "language_code": language_code,
            "sample_rate_hertz": sample_rate_hertz,
            "encoding": encoding,
        }
        with io.open(local_file_path, "rb") as f:
            content = f.read()
        audio = {"content": content}

        response = client.recognize(config, audio)

        for result in response.results:
            # First alternative is the most probable result
            alternative = result.alternatives[0]
            print(u"Transcript: {}".format(alternative.transcript))
            #print(result)
            print_sentences(response)

def saber_temps(paraula,start, end):
    print("LA PARAULA QUE ESTEM BUSCANT ES: " + paraula)
    print("EL SEU TEMPS INICIAL ES: " + str(start))
    print("EL SEU TEMPS FINAL ES: " + str(end))

    canco = AudioSegment.from_wav("/Users/pol/Desktop/GCV/src/audio.wav")

    duracio=end-start
    primera_part = canco[:start]
    ultima_part = canco[end:]
    segment = AudioSegment.silent(duration=duracio)

    final_song = primera_part + segment + ultima_part
    final_song.export("audio_out_file.wav", format="wav")



