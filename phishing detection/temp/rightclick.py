
import requests

def detect_right_click_disabled(url):
    try:
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            if 'event.button==2' in response.text:
                return -1  # Phishing (right-click function disabled)
            else:
                return 1  # Legitimate (right-click function not disabled)
        else:
            print("Failed to fetch webpage:", response.status_code)
            return -1  # Phishing (failed to fetch webpage)
    except Exception as e:
        print("An error occurred:", e)
        return -1  # Phishing (error occurred while analyzing webpage source code)


