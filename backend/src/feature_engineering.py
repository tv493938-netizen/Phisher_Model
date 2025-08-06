import re
import tldextract

def extract_features(url: str) -> dict:
    ext = tldextract.extract(url)
    domain = ext.domain
    suffix = ext.suffix
    subdomain = ext.subdomain

    return {
        "url_length": len(url),
        "num_dots": url.count('.'),
        "num_hyphens": url.count('-'),
        "num_underscores": url.count('_'),
        "num_slashes": url.count('/'),
        "num_equal": url.count('='),
        "num_question": url.count('?'),
        "num_percent": url.count('%'),
        "num_digits": sum(c.isdigit() for c in url),
        "num_params": url.count('&'),
        "has_ip": 1 if re.match(r'^(http[s]?:\\/\\/)?(\\d{1,3}\\.){3}\\d{1,3}', url) else 0,
        "has_https": 1 if 'https' in url else 0,
        "has_www": 1 if 'www' in url else 0,
        "num_subdomains": len(subdomain.split('.')) if subdomain else 0,
        "domain_length": len(domain),
        "suffix_length": len(suffix),
        "has_at_symbol": 1 if '@' in url else 0,
        "has_double_slash": 1 if '//' in url[url.find('//')+2:] else 0,
        "count_http": url.count('http'),
        "count_https": url.count('https'),
        "count_com": url.count('.com'),
        "is_encoded": 1 if '%' in url else 0,
        "count_colons": url.count(':'),
        "num_fragments": url.count('#'),
        "contains_login": 1 if 'login' in url.lower() else 0,
        "contains_secure": 1 if 'secure' in url.lower() else 0,
        "contains_account": 1 if 'account' in url.lower() else 0,
        "contains_update": 1 if 'update' in url.lower() else 0,
        "contains_bank": 1 if 'bank' in url.lower() else 0,
        "contains_free": 1 if 'free' in url.lower() else 0,
        "contains_verify": 1 if 'verify' in url.lower() else 0,
        "contains_paypal": 1 if 'paypal' in url.lower() else 0,
    }
