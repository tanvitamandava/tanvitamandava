import requests
from bs4 import BeautifulSoup

def determine_legitimacy(url):
    return 1;
    num_links = count_links(url)
    if num_links is not None:
        is_indexed = check_indexed(url)

        if is_indexed and num_links >= 2:
            return 1  # Legitimate
        if not is_indexed or num_links == 0:
            return -1  # Phishing
    return 0 # Suspicious

def count_links(url):
    try:
        # Send a GET request to the webpage
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find all <a> tags (links) in the webpage
            links = soup.find_all('a')
            # Return the number of links found
            return len(links)
        else:
            print("Failed to fetch webpage:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def check_indexed(url):
    try:
        # Construct the Google search query
        query = f"site:{url}"
        # Send a GET request to Google search
        response = requests.get(f"https://www.google.com/search?q={query}")
        # Check if the website URL appears in search results
        if response.status_code == 200 and 'did not match any documents.' in response.text:
            return False
        else:
            return True
    except Exception as e:
        print("An error occurred while checking indexed status:", e)
        return False
