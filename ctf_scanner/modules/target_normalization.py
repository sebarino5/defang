from __future__ import annotations

import ipaddress
from urllib.parse import urlparse

from ctf_scanner.schemas.results import NormalizedTarget


def normalize_target(raw_target: str) -> NormalizedTarget:
    value = raw_target.strip()
    if not value:
        raise ValueError("Target darf nicht leer sein")

    if "/" in value:
        try:
            ipaddress.ip_network(value, strict=False)
            return NormalizedTarget(raw=value, target_type="cidr", host=value)
        except ValueError:
            pass

    try:
        ipaddress.ip_address(value)
        return NormalizedTarget(raw=value, target_type="ip", host=value)
    except ValueError:
        pass

    parsed = urlparse(value)
    if parsed.scheme and parsed.netloc:
        return NormalizedTarget(
            raw=value,
            target_type="url",
            host=parsed.hostname or parsed.netloc,
            port=parsed.port,
            scheme=parsed.scheme,
        )

    if "." in value and " " not in value:
        return NormalizedTarget(raw=value, target_type="domain", host=value)

    raise ValueError(f"Ungültiges Target: {raw_target}")
