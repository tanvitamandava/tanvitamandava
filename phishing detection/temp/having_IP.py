import re
def detect_ip_in_url(url):
    # Regular expression pattern to match IPv4 addresses
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'  
    # Regular expression pattern to match hexadecimal IPv4 addresses
    hex_ip_pattern = r'http?://(?:[0-9a-fA-F]+\.?)+(/[0-9a-fA-F]+)*'
    
    # Check if the URL contains a normal IP address
    if re.search(ip_pattern, url):
        return -1
    
    # Check if the URL contains a hexadecimal IP address
    if re.search(hex_ip_pattern, url):
        return -1
    
    return 1
