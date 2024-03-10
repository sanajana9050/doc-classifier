import argparse
import base64
from enum import Enum
import io
from io import BytesIO

import png
from google.cloud import vision
from PIL import Image, ImageDraw

import os


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def draw_boxes(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        draw.polygon(
            [
                bound.vertices[0].x,
                bound.vertices[0].y,
                bound.vertices[1].x,
                bound.vertices[1].y,
                bound.vertices[2].x,
                bound.vertices[2].y,
                bound.vertices[3].x,
                bound.vertices[3].y,
            ],
            None,
            color,
        )
    return image


def get_paragraph_text(para):
    """Returns the text in the paragraph."""
    text = ""
    for word in para.words:
        for symbol in word.symbols:
            text = text + symbol.text

        text = text + " "

    return text


def get_word_text(word):
    """Returns the text in the word."""
    text = ""
    for symbol in word.symbols:
        text = text + symbol.text

    return text


def get_document_bounds(img, feature):
    """Returns document bounds given an image."""
    # load credentials from json file and create client
    # creds.json is the json file that contains the credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.dirname(os.path.abspath(__file__)) + '/creds.json'
    client = vision.ImageAnnotatorClient()

    bounds = []
    texts = []
    #img = Image.open(BytesIO(img))

    # vision api image object
    img = vision.Image(content=img)


    response = client.document_text_detection(image=img)
    document = response.full_text_annotation
    # full_text = response.text

    # Collect specified feature bounds by enumerating driving_license document features
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if feature == FeatureType.SYMBOL:
                            bounds.append(symbol.bounding_box)
                            texts.append(symbol.text)

                    if feature == FeatureType.WORD:
                        bounds.append(word.bounding_box)
                        texts.append(get_word_text(word))

                if feature == FeatureType.PARA:
                    bounds.append(paragraph.bounding_box)
                    texts.append(get_paragraph_text(paragraph))

            if feature == FeatureType.BLOCK:
                bounds.append(block.bounding_box)

    # The list `bounds` contains the coordinates of the bounding boxes.
    return [bounds, texts, document.text]

def isInside(vertices, x, y, width, height):
    for i in range(0, 4):
        if vertices[i].x < x or vertices[i].x > x + width or vertices[i].y < y or vertices[i].y > y + height:
            return False
    return True