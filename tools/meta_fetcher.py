import requests
from bs4 import BeautifulSoup
from langchain.tools import tool
import json

@tool
def fetch_meta(url: str) -> str:
    """Fetches comprehensive metadata from a webpage and returns JSON formatted data."""
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Basic metadata
        title = soup.title.string.strip() if soup.title else "No Title Found"
        desc_tag = soup.find("meta", attrs={"name": "description"})
        description = desc_tag["content"].strip() if desc_tag else "No Meta Description Found"
        
        # Heading tags
        h1 = soup.find("h1")
        h1_text = h1.get_text(strip=True) if h1 else "No H1 found"
        
        # Additional meta tags
        keywords_tag = soup.find("meta", attrs={"name": "keywords"})
        keywords = keywords_tag["content"].strip() if keywords_tag else "No Keywords Found"
        
        # Open Graph tags
        og_title = soup.find("meta", property="og:title")
        og_description = soup.find("meta", property="og:description")
        og_image = soup.find("meta", property="og:image")
        
        # Twitter Card tags
        twitter_title = soup.find("meta", attrs={"name": "twitter:title"})
        twitter_description = soup.find("meta", attrs={"name": "twitter:description"})
        twitter_image = soup.find("meta", attrs={"name": "twitter:image"})
        
        # Build JSON response
        metadata = {
            "url": url,
            "basic_meta": {
                "title": title,
                "description": description,
                "keywords": keywords,
                "h1": h1_text
            },
            "open_graph": {
                "title": og_title["content"] if og_title else None,
                "description": og_description["content"] if og_description else None,
                "image": og_image["content"] if og_image else None
            },
            "twitter_card": {
                "title": twitter_title["content"] if twitter_title else None,
                "description": twitter_description["content"] if twitter_description else None,
                "image": twitter_image["content"] if twitter_image else None
            },
            "status": "success"
        }
        
        return json.dumps(metadata, indent=2)
        
    except Exception as e:
        error_response = {
            "url": url,
            "error": str(e),
            "status": "error"
        }
        return json.dumps(error_response, indent=2)
