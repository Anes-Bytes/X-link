import re


RESERVED_SUBDOMAIN_NAMES = frozenset(
    ["admin", "api", "www", "mail", "static", "media", "root"]
)

SUBDOMAIN_PATTERN = re.compile(r"^(?!-)[a-z0-9-]{3,30}(?<!-)$")


def normalize_subdomain_name(name):
    return (name or "").strip().lower()


def validate_subdomain_format(name):
    return bool(SUBDOMAIN_PATTERN.fullmatch(name or ""))


def is_reserved_subdomain(name):
    return normalize_subdomain_name(name) in RESERVED_SUBDOMAIN_NAMES
