
import cv2
import subprocess
from enum import Enum
import io
from moviepy.editor import *




from google.cloud import vision, speech_v1
from google.cloud.vision import types
from PIL import Image, ImageDraw, ImageFont




class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5
    starti = []


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