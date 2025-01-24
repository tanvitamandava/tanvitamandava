import requests

def check_website_legitimacy(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        
        num_redirects = len(response.history)
        
        if num_redirects >= 4:
            return -1  # Phishing website
        else:
            return 1  # Legitimate website
    except Exception as e:
        return -1  # Phishing website or error occurred
