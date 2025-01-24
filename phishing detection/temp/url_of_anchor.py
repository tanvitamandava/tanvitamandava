import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def fetch_html_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print("Error: Unable to fetch HTML content.")
            return None
    except Exception as e:
        print("Error:", e)
        return None

def check_anchor_tags(main_url):
    html_content = fetch_html_content(main_url)
    main_domain = urlparse(main_url).netloc
    soup = BeautifulSoup(html_content, 'html.parser')
    anchor_tags = soup.find_all('a')

    for tag in anchor_tags:
        href = tag.get('href')
        if href:
            href_domain = urlparse(href).netloc
            if href_domain != main_domain:
                return -1  # Phishing attempt
            elif href.startswith("#") or href.startswith("javascript"):
                return 0  # Suspicious case
    return 1  # Correct URL