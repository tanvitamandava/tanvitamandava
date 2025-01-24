import re

def detect_at_symbol(url):
    # Regular expression pattern to match "@" symbol in the URL
    at_symbol_pattern = r'@'

    # Check if "@" symbol exists in the URL
    if re.search(at_symbol_pattern, url):
        return -1  # Indicates the presence of "@" symbol
    else:
        return 1  # Indicates the absence of "@" symbol


