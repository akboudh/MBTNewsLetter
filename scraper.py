import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_source(url: str) -> Dict[str, any]:
    """Scrape content from a news source URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text content
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Extract article titles and links if available
        articles = []
        for link in soup.find_all('a', href=True):
            title = link.get_text(strip=True)
            href = link.get('href', '')
            if title and len(title) > 10 and len(title) < 200:
                # Make absolute URL if relative
                if href.startswith('/'):
                    from urllib.parse import urljoin
                    href = urljoin(url, href)
                articles.append({'title': title, 'url': href})
        
        return {
            'url': url,
            'text': text[:5000],
            'articles': articles[:20],
            'success': True
        }
    except Exception as e:
        logger.error("Error parsing %s: %s", url, e)
        return {'url': url, 'text': '', 'articles': [], 'success': False, 'error': str(e)}

def scrape_all_sources(urls: List[str]) -> List[Dict[str, any]]:
    """Scrape all news sources. Continues on per-source failures."""
    results = []
    for i, url in enumerate(urls):
        logger.info("Scraping [%d/%d] %s...", i + 1, len(urls), url)
        result = scrape_source(url)
        results.append(result)
        if not result.get('success'):
            logger.warning("Skipped (failed): %s", url)
        time.sleep(2)  # Rate limiting
    return results



