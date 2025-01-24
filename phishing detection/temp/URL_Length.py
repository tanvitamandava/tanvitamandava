def classify_url(url):
    # Define the threshold for phishing URL length
    phishing_threshold = 54
    
    # Check if the length of the URL is greater than or equal to the phishing threshold
    if len(url) >= phishing_threshold:
        return -1  # Phishing URL
    elif len(url) < phishing_threshold and len(url) > 30:
        return 0  # Suspicious URL (shorter than phishing threshold but longer than typical legitimate URLs)
    else:
        return 1  # Legitimate URL


