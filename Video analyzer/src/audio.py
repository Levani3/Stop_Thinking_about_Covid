import io
from moviepy.editor import *
from pydub import AudioSegment

from google.cloud import vision, speech_v1
from google.cloud.speech_v1p1beta1 import enums




######################
#MODUL AUDIO
#####################

def print_word_offsets(alternative, canco):

    for word in alternative.words:
        start_ms = word.start_time.ToMilliseconds()
        end_ms = word.end_time.ToMilliseconds()
        word = word.word
        aux = word.upper()
        print(f'{start_ms / 1000:>7.3f}',
              f'{end_ms / 1000:>7.3f}',
              f'{word}',
              sep=' | ')
        if aux == "coronavirus" or aux == "CORONAVIRUS" or aux == "COVID" or aux == "covid" or aux == "Coronavirus" or aux == "VIRUS" or aux=="CASOS" or aux == "CORONA":
            print(f'{start_ms/1000:>7.3f}',
                f'{end_ms/1000:>7.3f}',
                f'{word}',
                sep=' | ')
            canco = saber_temps(word, start_ms, end_ms, canco)

    canco.export("../AudioOut/audio_out_file.wav", format="wav")




def print_sentences(response):
    canco = AudioSegment.from_wav("../src/audio.wav")
    canco.export("audio_out_file.wav", format="wav")
    for result in response.results:
        canco1 = AudioSegment.from_wav("../src/audio_out_file.wav")
        best_alternative = result.alternatives[0]
        transcript = best_alternative.transcript
        confidence = best_alternative.confidence
        print('-' * 80)
        print(f'Transcript: {transcript}')
        print(f'Confidence: {confidence:.0%}')
        print_word_offsets(best_alternative, canco1)




def sample_recognize(local_file_path):
        """
        Transcribe a short audio file using synchronous speech recognition

        Args:
          local_file_path Path to local audio file, e.g. /path/audio.wav
        """
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../credentials/credentials.json'
        client = speech_v1.SpeechClient()

        # local_file_path = 'resources/brooklyn_bridge.raw'

        # The language of the supplied audio
        language_code = "en-US"

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

def saber_temps(paraula,start, end, canco):
    print("HOLA ENTRO AL CENSURADOR DAUDIO")
    duracio=end-start
    primera_part = canco[:start]
    ultima_part = canco[end:]
    segment = AudioSegment.silent(duration=duracio)

    final_song = primera_part + segment + ultima_part
    #final_song.export("audio_out_file.wav", format="wav")
    return final_song



