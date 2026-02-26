from django.conf import settings


def _clean_host(host):
    host = (host or "").strip().lower()
    if ":" in host:
        host = host.split(":", 1)[0]
    return host.rstrip(".")


def extract_subdomain_from_host(host):
    host = _clean_host(host)
    base_domain = (getattr(settings, "BASE_DOMAIN", "") or "").strip().lower().rstrip(".")

    if not host:
        return None

    if host in {"localhost", "127.0.0.1", "[::1]"}:
        return None

    if host.endswith(".localhost"):
        return host[: -len(".localhost")] or None

    if base_domain and host == base_domain:
        return None

    if base_domain and host.endswith(f".{base_domain}"):
        candidate = host[: -(len(base_domain) + 1)]
        return candidate or None

    return None
