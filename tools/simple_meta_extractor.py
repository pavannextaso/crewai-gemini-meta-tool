import requests
from bs4 import BeautifulSoup
from langchain.tools import tool
import json

@tool
def extract_title_description(url: str) -> str:
    """Extracts just the title and meta description from a webpage and returns JSON formatted data."""
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Basic metadata
        title = soup.title.string.strip() if soup.title else "No Title Found"
        desc_tag = soup.find("meta", attrs={"name": "description"})
        description = desc_tag["content"].strip() if desc_tag else "No Meta Description Found"
        
        # Simple response with just title and description
        result = {
            "url": url,
            "title": title,
            "meta_description": description,
            "status": "success"
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        error_response = {
            "url": url,
            "error": str(e),
            "status": "error"
        }
        return json.dumps(error_response, indent=2)

