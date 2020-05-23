# coding=utf-8
import os

from google.cloud import speech_v1
import io

from google.cloud.speech_v1.gapic import enums
from pydub import AudioSegment


def sample_recognize(local_file_path):
    """
    Transcribe a short audio file using synchronous speech recognition

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\Users\PcCom1\Desktop\SSMM\SSMM pracs\speech\credentials\elated-bebop-276315-02cb42398afe.json'
    client = speech_v1.SpeechClient()

    # local_file_path = 'resources/brooklyn_bridge.raw'

    # The language of the supplied audio
    language_code = "es-ES"
    #language_code = "en-US"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 48000

    enable_word_time_offsets = True
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
    print_sentences(response)


def print_sentences(response):

    canco = AudioSegment.from_wav("C:/Users/PcCom1/Desktop/SSMM/SSMM pracs/speech/audio.wav")
    canco.export("audio_out_file.wav", format="wav")
    for result in response.results:
        canco1 = AudioSegment.from_wav("C:/Users/PcCom1/Desktop/SSMM/SSMM pracs/speech/audio_out_file.wav")
        best_alternative = result.alternatives[0]
        transcript = best_alternative.transcript
        confidence = best_alternative.confidence
        print('-' * 80)
        print(transcript)
        print_word_offsets(best_alternative, canco1)



def print_word_offsets(alternative, canco):
    for word in alternative.words:
        start_ms = word.start_time.ToMilliseconds()
        end_ms = word.end_time.ToMilliseconds()
        word = word.word
        aux = word.upper()
        if aux == "CASOS" or aux == "EPIDEMIA" or aux == "SINTOMAS" or aux == "INFORMACION":
                canco = saber_temps(word, start_ms, end_ms, canco)

    canco.export("audio_out_file.wav", format="wav")

def saber_temps(paraula,start, end, canco):
    print("LA PARAULA QUE ESTEM BUSCANT ES: " + paraula)
    print("EL SEU TEMPS INICIAL ES: " + str(start))
    print("EL SEU TEMPS FINAL ES: " + str(end))

    duracio=end-start
    primera_part = canco[:start]
    ultima_part = canco[end:]
    segment = AudioSegment.silent(duration=duracio)
    rec = AudioSegment.from_wav("C:/Users/PcCom1/Desktop/SSMM/SSMM pracs/speech/Enregistrament.wav")
    final_song = primera_part + rec + ultima_part
    #final_song.export("audio_out_file.wav", format="wav")
    return final_song

def mp4_to_wav(file):
    audio = AudioSegment.from_file(file, format="mp4")
    audio.export("audio.wav", format="wav")
    return audio

if __name__ == "__main__":
    mp4_to_wav('UltimaHora_Trim_Trim_Trim.mp4')
    song =AudioSegment.from_wav("C:/Users/PcCom1/Desktop/SSMM/SSMM pracs/speech/audio.wav")
    song = song.set_channels(1)
    song.export("audio.flac", format="flac")
    sample_recognize("C:/Users/PcCom1/Desktop/SSMM/SSMM pracs/speech/audio.flac")