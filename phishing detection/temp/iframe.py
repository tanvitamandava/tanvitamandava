import requests
from bs4 import BeautifulSoup

def determine_legitimacy(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            iframes = soup.find_all('iframe')
            for iframe in iframes:
                visibility = iframe.get('frameborder', '').lower() != '0'
                if visibility:
                    return 0  # Suspicious (iframes present and visible)
            return 1  # Legitimate (no visible iframes)
        else:
            print("Failed to fetch webpage:", response.status_code)
            return -1
    except Exception as e:
        print("An error occurred:", e)
        return -1  # Phishing (error occurred)