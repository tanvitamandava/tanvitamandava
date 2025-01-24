import requests
from urllib.parse import urlparse

def check_website_legitimacy(url):
    try:
        api_url = 'https://openpagerank.com/api/v1.0/getPageRank'
        domains = [urlparse(url).netloc]
        api_url = api_url + '?' + '&'.join([f"domains[]={d}" for d in domains])

        response = requests.get(api_url, headers={'API-OPR': 'o4wsgwk8gw0s44o00sksc80sgwoskgwwc88o40c0'})

        if response.status_code == 200:
            for domain in response.json()['response']:
                if domain['page_rank_decimal'] < 0.5:
                    return -1  # Phishing website
                else:
                    return 1  # Legitimate website
        else:
            return -1  # Error occurred
    except Exception as e:
        print("An error occurred:", e)
        return -1  # Error occurred
