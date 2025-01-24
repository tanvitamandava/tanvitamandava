import requests
from bs4 import BeautifulSoup

def check_website_legitimacy(url):
    try:
        # Fetch the webpage
        response = requests.get(url)
        if response.status_code != 200:
            print("Failed to fetch the webpage")
            return -1
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        personal_info_keywords = ['name', 'email', 'address', 'phone', 'social security', 'credit card', 'password']
        
        popups = soup.find_all(lambda tag: tag.has_attr('popUpWidnow'))  # corrected the typo
        for popup in popups:
            popup_text = popup.text.lower()
            for keyword in personal_info_keywords:
                if keyword in popup_text:
                    print("Potential phishing detected: Pop-up window asking for personal information")
                    return -1
        
        return 1  # Legitimate website

    except Exception as e:
        print("Error occurred:", e)
        return -1  # Error occurred or potentially phishing

