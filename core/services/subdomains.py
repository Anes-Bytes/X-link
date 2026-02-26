from dataclasses import dataclass

from django.db import IntegrityError, transaction

from core.models import UserSubdomain
from core.subdomains import (
    is_reserved_subdomain,
    normalize_subdomain_name,
    validate_subdomain_format,
)


@dataclass(frozen=True)
class SubdomainResult:
    available: bool
    reason: str
    name: str


def check_subdomain_availability(name, user=None):
    normalized = normalize_subdomain_name(name)

    if not validate_subdomain_format(normalized):
        return SubdomainResult(available=False, reason="invalid_format", name=normalized)

    if is_reserved_subdomain(normalized):
        return SubdomainResult(available=False, reason="reserved", name=normalized)

    existing = UserSubdomain.objects.filter(subdomain=normalized).only("id", "user_id").first()
    if existing and user is not None and existing.user_id == user.id:
        return SubdomainResult(available=True, reason="ok", name=normalized)

    exists = existing is not None
    if exists:
        return SubdomainResult(available=False, reason="taken", name=normalized)

    return SubdomainResult(available=True, reason="ok", name=normalized)


@transaction.atomic
def assign_subdomain_to_user(user, name):
    check = check_subdomain_availability(name, user=user)
    normalized = check.name

    if not check.available:
        return check

    try:
        UserSubdomain.objects.update_or_create(
            user=user,
            defaults={"subdomain": normalized, "is_active": True},
        )
    except IntegrityError:
        return SubdomainResult(available=False, reason="taken", name=normalized)

    return SubdomainResult(available=True, reason="ok", name=normalized)
