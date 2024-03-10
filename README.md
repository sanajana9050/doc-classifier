# Document Classification and Entity Extraction

## Installation

### Clone

- Clone this repo to your local machine using `git clone`

### Setup

- Install the required packages using `pip install -r requirements.txt`
- Place the Google Cloud IAM service account key for OCR Detection in the root directory of the project and rename it to `creds.json`
- OPENAI API key is required for the text summarization. Environment variable `OPENAI_API_KEY` should be set to the API key. To get the API key, visit [OpenAI](https://openai.com/)
- Run the following command to start the flask server
    `python -m flask --app index.py run`

