import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_favicon_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        favicon_link = soup.find("link", rel="icon") or soup.find("link", rel="shortcut icon")
        if favicon_link:
            favicon_url = favicon_link.get("href")
            if favicon_url:
                return urljoin(url, favicon_url)
    except requests.exceptions.RequestException as e:
        print("Error fetching webpage:", e)
    return None

def is_phishing(url):
    favicon_url = get_favicon_url(url)
    if favicon_url and favicon_url.startswith("http"):
        domain = url.split("//")[-1].split("/")[0]

        favicon_domain = favicon_url.split("//")[-1].split("/")[0]

        if domain != favicon_domain:
            return -1
    return 1