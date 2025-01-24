def shortening_service(url):
    shortening_domains = ["bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd", "buff.ly", "tiny.cc", "cli.gs", "tr.im", "u.nu", "snipurl.com", "shorturl.at", "shrtco.de", "tiny.ie", "url.ie", "clicky.me", "buzurl.com", "tweez.me", "snipr.com", "short.ie", "xr.com", "x.co", "tiny.pl", "short.to", "href.in", "lnkd.in", "dft.ba", "qr.ae", "smarturl.it", "ity.im", "v.gd", "shorte.st", "adf.ly", "bc.vc", "q.gs", "1url.com", "2.gp", "4zip.in", "alturl.com", "cutt.ly", "is.gd", "t2m.io"]

    url_parts = url.split('/')
    domain = url_parts[2] if len(url_parts) >= 3 else None

    if domain in shortening_domains:
        return -1  # Shortened URL
    else:
        return 1  # Not shortened URL

