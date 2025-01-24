def check_url(url):
    # Check if "https" is present in the domain part of the URL
    if "://" in url:
        domain_part = url.split("://")[1]  # Extract the domain part of the URL
        if "https" in domain_part:
            return -1  # Phishing attempt
    return 1   # Correct URL

