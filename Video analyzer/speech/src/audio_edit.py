import io

from google.cloud import speech_v1 as speech
from pydub import AudioSegment
import speech_recognition as sr

def speech_to_text(config, audio1):
    client = speech.SpeechClient.from_service_account_json('credentials/My First Project-182091cab4b3.json')
    r = sr.Recognizer()
    with io.open('audio.wav', "rb") as f:
        content = f.read()
    audio = {"content": content}
    response = client.recognize(config, audio)
    startOffset, endOffset = print_sentences(response)
    return startOffset, endOffset


def print_sentences(response):
    for result in response.results:
        best_alternative = result.alternatives[0]
        startOffset, endOffset = print_word_offsets(best_alternative)
        return startOffset, endOffset



def print_word_offsets(alternative):
    StartBan = []
    EndBan = []
    for word in alternative.words:
        start_ms = word.start_time.ToMilliseconds()
        end_ms = word.end_time.ToMilliseconds()
        word = word.word
        aux = word.upper()
        if aux in bannedWords:
            StartBan.append(start_ms)
            EndBan.app(end_ms)
    return StartBan, EndBan



def mp4_to_wav(file):
    audio = AudioSegment.from_file(file, format="mp4")
    audio.export("audio.wav", format="wav")
    return audio


config = {
    'language_code': 'en-US',
    'enable_automatic_punctuation': True,
    'enable_word_time_offsets': True,
}

bannedWords = "CORONA CORONAVIRUS COVID COVID-19 INFECTION DEAD"


if __name__ == "__main__":
    audio = mp4_to_wav('videoCovid_Trim.mp4')
    startOffset, endOffset = speech_to_text(config, audio)
    print (startOffset)
    print (endOffset)