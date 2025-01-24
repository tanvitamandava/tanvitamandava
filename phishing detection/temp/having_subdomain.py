import re

def detect_url_category(url):
    # Remove www. from the URL
    url = re.sub(r'^www\.', '', url)
    
    # Extract subdomain
    subdomain = url.split('.')[0]
    
    # Phishing pattern matching
    phishing_patterns = ['secure', 'login', 'bank', 'signin', 'account']
    for pattern in phishing_patterns:
        if re.search(pattern, subdomain, re.IGNORECASE):
            return -1
    
    # Suspicious pattern matching
    suspicious_patterns = ['xyz', 'random', '123', '-']
    for pattern in suspicious_patterns:
        if re.search(pattern, subdomain, re.IGNORECASE):
            return 0
    
    # Default to legitimate if no suspicious patterns found
    return 1

