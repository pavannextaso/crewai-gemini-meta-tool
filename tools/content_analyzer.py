import requests
from bs4 import BeautifulSoup
from langchain.tools import tool
import json
import re
from collections import Counter

@tool
def analyze_content(url):
    
    """Analyzes webpage content for SEO metrics and returns JSON formatted data."""
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Extract text content
        text_content = soup.get_text()
        words = re.findall(r'\b\w+\b', text_content.lower())
        word_count = len(words)
        
        # Count headings
        headings = {
            "h1": len(soup.find_all("h1")),
            "h2": len(soup.find_all("h2")),
            "h3": len(soup.find_all("h3")),
            "h4": len(soup.find_all("h4")),
            "h5": len(soup.find_all("h5")),
            "h6": len(soup.find_all("h6"))
        }
        
        # Count images and alt tags
        images = soup.find_all("img")
        images_without_alt = [img for img in images if not img.get("alt")]
        
        # Count links
        internal_links = []
        external_links = []
        for link in soup.find_all("a", href=True):
            href = link.get("href")
            if href.startswith("http"):
                external_links.append(href)
            else:
                internal_links.append(href)
        
        # Most common words (excluding common stop words)
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall', 'a', 'an', 'this', 'that', 'these', 'those'}
        filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
        top_keywords = Counter(filtered_words).most_common(10)
        
        analysis = {
            "url": url,
            "content_metrics": {
                "word_count": word_count,
                "heading_count": headings,
                "total_headings": sum(headings.values())
            },
            "image_metrics": {
                "total_images": len(images),
                "images_without_alt": len(images_without_alt),
                "alt_text_coverage": round((len(images) - len(images_without_alt)) / len(images) * 100, 2) if images else 0
            },
            "link_metrics": {
                "internal_links": len(internal_links),
                "external_links": len(external_links),
                "total_links": len(internal_links) + len(external_links)
            },
            "top_keywords": [{
                "keyword": keyword,
                "frequency": freq
            } for keyword, freq in top_keywords],
            "status": "success"
        }
        return json.dumps(analysis, indent=2)
        
    except Exception as e:
        error_response = {
            "url": url,
            "error": str(e),
            "status": "error"
        }
        return json.dumps(error_response, indent=2)

