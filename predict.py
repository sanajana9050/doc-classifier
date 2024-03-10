import os
import openai

# Set your secret API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_prediction(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="text =  \"" + text + "\"\n\njson_schema= \"\n{\n    \"documents\": {\n        \"type\": \"array\",\n        \"items\": {\n            \"type\": \"object\",\n            \"properties\": {\n                \"doc_type\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"pan_card\", \"aadhar_card\", \"bank_statement\", \"itr\", \"utility_bill\", \"cheque\", \"salary_slip\", \"driving_license\", \"voter_id\", \"passport\", \"unknown\"],\n                    \"desc\": \"Doc type, lowercase, one of the listed options\"\n                },\n                \"name\": {\n                    \"type\": \"string\",\n                    \"desc\": \"Full name of individual. None if not found\"\n                },\n                \"id\": {\n                    \"type\": \"string\",\n                    \"desc\": \"Important id no. based on doc_type. None if not found\"\n                },\n                \"dob\": {\n                    \"type\": \"string\",\n                    \"format\": \"date\",\n                    \"desc\": \"DOB of individual. Format YYYY-MM-DD. None if not found\"\n                },\n                \"gender\": {\n                    \"type\": \"string\",\n                    \"desc\": \"Gender of individual. None if not found\"\n                },\n                \"address\": {\n                    \"type\": \"string\",\n                    \"desc\": \"Address of individual. None if not found\"\n                },\n                \"dates\": {\n                    \"type\": \"object\",\n                    \"desc\": \"All dates, with keys representing what they are. Format YYYY-MM-DD. None if not found\"\n                },\n                \"entities\": {\n                    \"type\": \"object\",\n                    \"desc\": \"Other important data in document\"\n                }\n            }\n        }\n    }\n}\n\"\n\n\nGenerate a valid JSON extracting the info from the text above based on the given json_schema :\n\n",
        temperature=0.5,
        max_tokens=1526,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    res = response['choices'][0]['text']
    # convert to json
    import json
    try:
        res = json.loads(res)
    except:
        res = {}
    return res
