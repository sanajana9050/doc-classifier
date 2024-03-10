import base64

from flask import Flask, request
from flask import render_template

from predict import get_prediction
from extract import get_document_bounds, FeatureType, isInside

app = Flask(__name__)
import json

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/about')
def about():
    jsonX = {
        "name": "Vishesh",
        "age": 21
    }
    # stringify the json object
    json_string = json.dumps(jsonX)
    return json_string


# route: /ocr , method: POST , body: {image: <base64 encoded image>}
@app.route('/ocr', methods=['POST'])
def ocr():
    # get the image from the request body

    image = request.json['image']
    # remove data:image/jpeg;base64, from the image string
    image = image.replace('data:image/jpeg;base64,', '')
    # remove data:image/png;base64, from the image string
    image = image.replace('data:image/png;base64,', '')
    # decode the image
    image = base64.b64decode(image)

    # get the text from the image
    [bounds, text, fullText] = get_document_bounds(image, FeatureType.PARA)
    # return the text
    response = {
        "text": text,
        "fullText": fullText
    }
    return json.dumps(response)
    #return "{}"

# route: /predict , method: POST , body: {text: <text>, boundingBox: <bounding box> | None}
@app.route('/predict', methods=['POST'])
def predict():
    image = request.json['image']
    # remove data:image/jpeg;base64, from the image string
    image = image.replace('data:image/jpeg;base64,', '')
    # remove data:image/png;base64, from the image string
    image = image.replace('data:image/png;base64,', '')
    # decode the image
    image = base64.b64decode(image)

    # get the text from the image
    [bounds, texts, fullText] = get_document_bounds(image, FeatureType.PARA)
    # bound has 4 vertices, each vertex has x and y
    print("Done: OCR")
    unclassified_prediction = get_prediction(fullText)
    print("Done: unclassified_prediction")
    boundingBoxes = request.json['boundingBoxes']

    classified_text = ""
    for boundingBox in boundingBoxes:
        # get the x, y, width and height

        label = boundingBox['label']
        x = boundingBox['left']
        y = boundingBox['top']
        width = boundingBox['width']
        height = boundingBox['height']

        classified_text = classified_text + label + "{\n "
        # filter the text that is inside the bounding box
        filteredText = ""
        for i in range(len(bounds)):
            # get the vertices of the bounding box
            vertices = bounds[i].vertices
            # get the text
            text = texts[i]
            # check if the text is inside the bounding box
            if isInside(vertices, x, y, width, height):
                filteredText = filteredText + text + "\n"


        classified_text = classified_text + filteredText + "\n}"

    classified_prediction = get_prediction(classified_text)
    print("Done: classified_prediction")
    response = {
        "unclassified_prediction": unclassified_prediction,
        "classified_prediction": classified_prediction
    }
    return json.dumps(response)






