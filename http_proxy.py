import os
import urllib.request

DOMAINS_ALLOWED = os.environ.get('DOMAINS_ALLOWED', '*')
TIMEOUT_SECONDS = os.environ.get('TIMEOUT_SECONDS', 10)


def proxy(url):
    try:
        response = urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS).read()
        return {
            "body": response.decode('utf-8'),
            "headers": {
                "Access-Control-Allow-Origin": DOMAINS_ALLOWED,
            }
        }
    except Exception as e:
        print(str(e))
        return ""
