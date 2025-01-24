def detect_double_slash(url):
    # Check if the URL starts with "HTTP"
    if url.startswith("http://"):
        if url.find("//", 6) != -1:
            return -1  # Indicates presence of "//" at the sixth position for "HTTP"
    # Check if the URL starts with "HTTPS"
    elif url.startswith("https://"):
        if url.find("//", 7) != -1:
            return -1  # Indicates presence of "//" at the seventh position for "HTTPS"
    
    return 1  # Indicates absence of "//" at the specified positions

