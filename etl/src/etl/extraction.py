import requests
from bs4 import BeautifulSoup
import re
from search_logging import get_logger

logger = get_logger(__name__)

def fetch_and_parse(url):
    try:
        logger.info(f"fetching url: {url}")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def extract_title(soup):
    title = soup.title.string if soup.title else ''
    if not title:
        h1_tag = soup.find('h1')
        title = h1_tag.get_text() if h1_tag else ''
    
    return title.strip()

def extract_text(soup):
    article_content = soup.find_all('p')
    text = " ".join([para.get_text() for para in article_content])
    return text.strip()

def clean_text(document):
    document['title'] = re.sub(r'\s+', ' ', document['title'])
    document['content'] = re.sub(r'<.*?>', '', document ['content'])
    return document

def get_cleaned_content(url):
    soup = fetch_and_parse(url)
    if soup is None:
        return None
    
    title = extract_title(soup)
    content = extract_text(soup)

    full_content = {'url': url, 'title': title, 'content': content}

    cleaned_content = clean_text(full_content)
    return cleaned_content




