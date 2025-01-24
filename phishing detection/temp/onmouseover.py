import requests
from bs4 import BeautifulSoup

def check_website_legitimacy(url):
    try:
        # Fetch the webpage
        response = requests.get(url)
        if response.status_code != 200:
            print("Failed to fetch the webpage")
            return -1
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for onMouseOver event in HTML tags
        elements = soup.find_all(lambda tag: tag.has_attr('onmouseover'))
        
        if elements:
            print("Potential phishing detected: HTML tag contains onMouseOver event")
            return -1
        
        return 1  # Legitimate website
    except Exception as e:
        print(f"An error occurred: {e}")
        return -1  # Phishing website or error occurred

