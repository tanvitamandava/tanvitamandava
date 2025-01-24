import re

def detect_prefix_suffix(url):
    # Regular expression pattern to match suspicious prefixes or suffixes separated by a dash symbol
    prefix_suffix_pattern = r'[-]\w+'

    # Check if the pattern exists in the URL
    if re.search(prefix_suffix_pattern, url):
        return -1  # Indicates the presence of suspicious prefixes or suffixes separated by a dash symbol
    else:
        return 1  # Indicates the absence of suspicious prefixes or suffixes

