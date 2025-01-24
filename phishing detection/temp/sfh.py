import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def is_phishing_website(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.content, 'html.parser')
        sfh_forms = soup.find_all('form', action=True)
        
        for form in sfh_forms:
            action_url = form['action']
            if action_url == '' or action_url.lower() == 'about:blank':
                return True  
            
            parsed_action_url = urlparse(action_url)
            parsed_base_url = urlparse(url)
            if parsed_action_url.netloc != '' and parsed_action_url.netloc != parsed_base_url.netloc:
                return True  
        
        return False
    except (requests.RequestException, ValueError, TypeError) as e:  
        print(f"Error occurred: {e}")
        return True  

def is_valid_url(url):
    """Check if the URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])  
    except ValueError:
        return False

def determine_website_status(url):
    if not is_valid_url(url):
        return -1
    elif is_phishing_website(url):
        return -1
    else:
        return 1
