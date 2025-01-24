import requests
from bs4 import BeautifulSoup
import tldextract

def get_metadata(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract metadata tags like title, description, keywords, etc.
            title = soup.find('title').text.strip() if soup.find('title') else ""
            description = soup.find('meta', attrs={'name': 'description'})
            description = description['content'].strip() if description else ""
            keywords = soup.find('meta', attrs={'name': 'keywords'})
            keywords = keywords['content'].strip() if keywords else ""
            return title, description, keywords, soup
        else:
            print("Error:", response.status_code)
            return None
    except Exception as e:
        print("Error fetching metadata:", e)
        return None

def analyze_website(url):
    metadata = get_metadata(url)
    if metadata:
        title, description, keywords, soup = metadata
        # Extract domain name
        domain = tldextract.extract(url).domain.lower()
        common_elements = ['contact', 'privacy', 'policy', 'terms']
        for element in common_elements:
            if soup.find(text=lambda text: text and element in text.lower()):
                return 1
        if 'official' in title.lower() or 'trusted' in description.lower():
            return 1
        elif 'login' in keywords.lower() or 'password' in keywords.lower():
            return -1
        elif domain in ["google", "youtube", "facebook", "twitter"]:
            return 1
        else:
            return 0
    else:
        return 0
