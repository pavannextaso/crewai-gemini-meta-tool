# /tools/plagiarism.py
import json
import os
import requests
from langchain.tools import tool
from dotenv import load_dotenv
load_dotenv()

@tool
def plagiarism_detector(text: str) -> dict:
    """Check the input text for plagiarism using MLTools API."""
    try:
        print("Text: ", text)
        api_url = "https://mltools.ws.multivariate.ai/plagiarism_detector"

        payload = {
            'submit': 'Submit',
            'text': text,
            'api':"true"
        }
        headers = {
            'Origin': 'https://mltools.ws.multivariate.ai',
            'Referer': 'https://mltools.ws.multivariate.ai/plagiarism_detector',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            'authorization': 'Basic ' + os.getenv('MLTools_API_Key')
        }
        response = requests.request("POST", api_url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()
        return data

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# Correct test call
# print(plagiarism_detector("Photosynthesis is the process by which green plants make their food."))
