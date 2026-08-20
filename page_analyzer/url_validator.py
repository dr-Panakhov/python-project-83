from urllib.parse import urlparse
import validators


def validate(url):
    errors = []
    if not url or len(url) > 255 or not validators.url(url):
        errors.append('Некорректный URL')
    return errors


def normalize(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"
