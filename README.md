# Document Classification and Entity Extraction

## Introduction 
The goal of this project is to develop a library that utilizes advanced machine learning and image processing
techniques to classify and extract data from various types of documents, including PAN, Aadhaar, bank statements,
ITR/Form 16, customer photographs, utility bills, cheque leaves, salary slips, driving licenses, voter IDs, and
passports. The library must be able to process vast amounts of files efficiently and securely, while being scalable to
handle large datasets.

## Image object detection and classification pipeline

### Document Classification

The initial step in the process involves classifying the different types of documents present within the input file. To
accomplish this, a custom machine learning model was trained using Google Vertex AI AutoML. The model was
trained on a dataset of 7500 images, representing each document type, with the aim of achieving high precision
(>98%) in detecting Aadhar card and PAN card. The document detection model was trained for the following
documents: Aadhar card front, PAN card, voter ID, passport, cheque, and driving license.

![image](https://github.com/sanajana9050/doc-classifier/assets/91480566/cbfb5118-9267-4680-b838-9d33a671ca19)


### Data Augmentation 

To increase the dataset, data augmentation techniques were applied to artificially increase the number of images
available for training. This is crucial to mitigate the risk of overfitting and to improve the generalization capabilities of
the model. Data augmentation techniques such as Rotation, Flipping, Scaling, Translation, Noise, Color manipulation,
Blur were employed.
After applying data augmentation, the dataset size was increased by a factor of 8. Data augmentation was applied in
a way that preserved the distribution of the data, and a hold-out dataset was used to validate the performance of
the model.
After that, the dataset of 7500 unique images are generated, these images contain a random number of nonoverlapping documents with random scale, position, and orientation with a random background.
Since the objective of the model was to find the bounding box the object was in, these kind of generated images
were the only option with this much-limited data.


### Object Detection and OCR

Once the bounding boxes of the documents in a multi-document image are generated, the text detected by OCR is
filtered to the respective bounding boxes and passed to the raw text classification pipeline for contextual data and
entity extraction. However, one major drawback of the object detection model is false positives. These issues can be
addressed with higher quality datasets and more robust training methods.

### Multi Document Image Test:


![image](https://github.com/sanajana9050/doc-classifier/assets/91480566/032aec5d-00fa-4387-a46d-0993df65bbf2)


Note*: Images for testing and training were sourced from publically available Google Images.

### Result (Entities automatically extracted based on Document Context):


![image](https://github.com/sanajana9050/doc-classifier/assets/91480566/6de9eda7-5845-41ae-b326-06330692d893)


## Classification Pipeline Based on Raw Text Data

For documents that do not have a standard appearance and/or can be highly varied, the object detection model
cannot be used. These types of documents include bank statements, ITR, utility bills, and salary slips. For these types
of documents, a classification pipeline based on raw text data can be used. This method works well for single
document images, but for multi-document images, it may not be able to find all the document types. To extract
relevant entities from the documents, a custom model was trained on top of GPT-3. The GPT-3 model is used to
extract relevant entities from the documents that do not have a standard appearance and cannot be classified using
the object detection model.
The custom AI model trained on top of GPT-3 is used to extract structured data from unstructured text. It can
understand the context of the text and identify specific entities such as names, addresses, and dates. The model is
also able to understand the relationships between different entities and extract them in a structured format.
To extract the relevant entities, a specific type of JSON schema was designed to fetch the results in a standardized
way and reduce variability in the way the data is structured. The JSON schema is used to map the extracted entities
to specific fields, making it easy to understand and process the data.

### Limitations 

Due to lack of extensive training and small amount of training dataset, the object detection pipeline may mark some
false positives, in such cases raw data pipeline can be referenced for a more accurate prediction:

Example where Raw Text Classification pipeline performs better than
Image object detection pipeline:



*Salary slip falsely identified as Aadhar (Image Object Detection pipeline)*                      


![image](https://github.com/sanajana9050/doc-classifier/assets/91480566/6698f6b2-c353-458c-8214-ea86acf7a7af)



*Raw Text Classification Pipeline (Accurate Classification)*



![image](https://github.com/sanajana9050/doc-classifier/assets/91480566/c4bf0b96-13d2-4054-9902-55502bde7043)


















## Installation

### Clone

- Clone this repo to your local machine using `git clone`

### Setup

- Install the required packages using `pip install -r requirements.txt`
- Place the Google Cloud IAM service account key for OCR Detection in the root directory of the project and rename it to `creds.json`
- OPENAI API key is required for the text summarization. Environment variable `OPENAI_API_KEY` should be set to the API key. To get the API key, visit [OpenAI](https://openai.com/)
- Run the following command to start the flask server
    `python -m flask --app index.py run`
