import argparse
import cv2
import os
import numpy as np
import string
import subprocess
from enum import Enum
from os.path import isfile, join
import io
from pathlib import Path
import glob

import pydub
from moviepy.editor import *
from pydub import AudioSegment
import moviepy.editor as mpe
from src import audio, image
from flask import Flask, request



from google.cloud import vision, speech_v1
from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.vision import types
from google.cloud import speech_v1 as speech
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
@app.route('/', methods=['GET'])

def isAudio(ruta):

    #Convertir un audio wav a flac amb nomes 1 canal
    print("CONVERTINT EL TEU AUDIO")
    song = AudioSegment.from_wav(ruta)
    song = song.set_channels(1)
    song.export("./src3", format="flac")
    print("PROCESSANT EL TEU AUDIO SIUSPLAU ESPERI")
    # Crida a l'api de speech to text
    audio.sample_recognize('../src/src3')

def isVideo(ruta, nomVideo):

    # Extreure l'audio d'un video
    print("EXTRAIENT L'AUDIO DEL VIDEO")
    command = "ffmpeg -i " + ruta + " -ab 160k -ac 2 -ar 44100 -vn audio.wav"
    subprocess.call(command, shell=True)

    isAudio("audio.wav")

    print("EXTRAIENT ELS FRAMES DEL VIDEO")
    input_filename = os.path.abspath(ruta)
    output_filename = os.path.abspath("../src/outputvideo")
    #Extreure els frames d'un video
    image.extract_frames_from_video(input_filename, output_filename)

    input_path = Path('../src/outputvideo')
    output_path = Path('../src/output')
    input_frames = input_path.glob('*.png')
    # crida a l'api de Text images per analisi de video
    print("PROCESSANT EL TEU VIDEO SIUSPLAU ESPERI")
    for in_frame in input_frames:
        out_frame = output_path / in_frame.name
        image.render_doc_text(in_frame, out_frame, nomVideo)

    # Convertim frames en video
    print("RECONVERTINT EL VIDEO")
    image.convert_frames_to_video(output_path)

    # Inserir audio en un video
    print("INSERINT AUDIO AL VIDEO")
    cmd = 'ffmpeg -y -i ../AudioOut/audio_out_file.wav -r 30 -i ../src/video_name.mp4  -filter:a aresample=async=1 -c:a flac -c:v copy ../VideoOut/output.mkv'
    subprocess.call(cmd, shell=True)


def isImage(ruta, nom):


    input_filename = os.path.abspath(ruta)
    output_filename = os.path.abspath("../ImageOut/out.png")

    image.render_doc_text(input_filename, output_filename, nom)

if __name__ == '__main__':
    """parser = argparse.ArgumentParser()
    parser.add_argument('detect_file', help='The image for text detection.')
    parser.add_argument('-out_file', help='Optional output file', default=0)
    args = parser.parse_args()"""
    #app.run(host='localhost', port=8080, debug=True)

    print("Introdueixi la direccio del arxiu que vol convertir")
    ruta = input()

    if(ruta[-3:]=="wav"):
        print("El teu arxiu es un audio")
        isAudio(ruta)

    elif(ruta[-3:]=="png" or ruta[-3:]=="jpg" or ruta[-4:] == "jpeg"):

        print("El teu arxiu es una imatge")
        print("Escriu una paraula per censurar la imatge: ")
        nom = input()
        isImage(ruta, nom)

    elif(ruta[-3:] == "mp4"):
        print("El teu arxiu es un video")
        print("Escriu una paraula per censurar la imatge: ")
        nomVideo = input()
        isVideo(ruta, nomVideo)







