from bs4 import BeautifulSoup
import requests


def mails(url: str) -> int:
    # Fetch the webpage content
    response = requests.get(url)
    html_content = response.text

    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all anchor tags
    anchor_tags = soup.find_all('a')

    # Check each anchor tag for "mailto" links
    for tag in anchor_tags:
        href = tag.get('href')
        if href and href.startswith('mailto:'):
            return -1
    return 1
