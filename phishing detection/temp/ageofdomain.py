import whois
from datetime import datetime

def determine_legitimacy(domain):
    try:
        domain_info = whois.whois(domain)
        creation_date = domain_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            age_in_months = (datetime.now() - creation_date).days / 30
            if age_in_months < 6:
                return -1  # Phishing (domain age less than 6 months)
            else:
                return 1  # Legitimate (domain age at least 6 months)
        else:
            return 0  # Suspicious (unable to determine domain age)
    except Exception as e:
        print("An error occurred while checking WHOIS record:", e)
        return 0  # Assume suspicious in case of an error

