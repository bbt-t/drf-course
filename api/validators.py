from re import findall
from sys import getsizeof

from rest_framework.exceptions import ValidationError


def find_links(text: str, allowed_domain: str) -> bool:
    url_pattern: str = r'(https?://\S+|www\.\S+|\S+\.\S+)'
    links: list = findall(url_pattern, text)

    return not all(allowed_domain in link for link in links)


def validate_materials(value: str):
    allowed_domain = 'youtube.com'
    is_found: bool = find_links(value, allowed_domain)
    if is_found:
        raise ValidationError("Ссылки на этот домен не разрешены")
