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



from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw, ImageFont

class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5



def draw_boxes(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""

    draw = ImageDraw.Draw(image)
    font_type = ImageFont.truetype("Arial.ttf", 14)

    for bound in bounds:
        print(str(bound))
        draw.polygon([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y], "black", color)


        draw.text(xy=( bound.vertices[0].x, bound.vertices[0].y), text="NOPE", fill=(255, 255, 255), font=font_type)


    #image.open()
    #image.show()

    return image


def assemble_word(word):
    assembled_word=""
    for symbol in word.symbols:
        assembled_word+=symbol.text
    return assembled_word



def get_document_bounds(image_file, feature, words_to_find):
    """Returns document bounds given an image."""
    client = vision.ImageAnnotatorClient.from_service_account_json('../credentials/gcloudcert.json')
    bounds = []

    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation


    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    assembled_word = assemble_word(word)
                    for worde in words_to_find:
                        if (assembled_word == worde):
                            if (feature == FeatureType.WORD):
                                bounds.append(word.bounding_box)

                if (feature == FeatureType.PARA):
                    bounds.append(paragraph.bounding_box)

            if (feature == FeatureType.BLOCK):
                bounds.append(block.bounding_box)

    # The list `bounds` contains the coordinates of the bounding boxes.
    print(bounds)
    return bounds

def render_doc_text(filein, fileout):
    image = Image.open(filein)
    """bounds = get_document_bounds(filein, FeatureType.BLOCK)
    draw_boxes(image, bounds, 'blue')
    bounds = get_document_bounds(filein, FeatureType.PARA)
    draw_boxes(image, bounds, 'red')"""
    words_to_find = ["coronavirus", "CORONAVIRUS", "Coronavirus", "COVID-19", "COVID - 19", "COVID", "VIRUS", "Virus", "virus", "Covid-19", "Covid"]
    bounds = get_document_bounds(filein, FeatureType.WORD, words_to_find)
    draw_boxes(image, bounds, 'red')

    if fileout != 0:
        image.save(fileout)
    else:
        image.show()




def extract_frames_from_video(video_path, frames_path):
    subprocess.call("ffmpeg -r 1 -i {video_path} -r 1 {out_path}".format(
        video_path=video_path,
        out_path=os.path.join(frames_path, "frame_%06d.png")), shell=True)


def convert_frames_to_video(frames_path):

    images = [img for img in os.listdir(frames_path) if img.endswith(".png")]
    images.sort()
    frame = cv2.imread(os.path.join(frames_path, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter("video_name2.mp4", 0x7634706d, 24, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(frames_path, image)))

    cv2.destroyAllWindows()
    video.release()




if __name__ == '__main__':
    """parser = argparse.ArgumentParser()
    parser.add_argument('detect_file', help='The image for text detection.')
    parser.add_argument('-out_file', help='Optional output file', default=0)
    args = parser.parse_args()"""

    input_filename = os.path.abspath("../inputs/video2.mp4")
    output_filename = os.path.abspath("../ouputVideo")
    output_video = os.path.abspath("../ouputVideo/video2.mp4")
    #output_path = os.path.abspath("../outputs")

    #command = "ffmpeg -i ../inputs/video2.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.wav"
    #subprocess.call(command, shell=True)

    #extract_frames_from_video(input_filename, output_filename)
    #source_img = Image.open("/Users/pol/Desktop/GCV/src/nada.png").convert("RGBA")
    #render_doc_text("/Users/pol/Desktop/GCV/ouputVideo/cap.png", "../src/frame.png")


    input_path = Path('/Users/pol/Desktop/GCV/ouputVideo')
    output_path = Path('/Users/pol/Desktop/GCV/outputs')
    input_frames = input_path.glob('*.png')

    for in_frame in input_frames:
        out_frame = output_path / in_frame.name
        #render_doc_text(in_frame, out_frame)

    #convert_frames_to_video(output_path)



    cmd = 'ffmpeg -y -i /Users/pol/Desktop/GCV/src/audio.wav  -r 30 -i /Users/pol/Desktop/GCV/src/video_name2.mp4  -filter:a aresample=async=1 -c:a flac -c:v copy av.mkv'
    subprocess.call(cmd, shell=True)


