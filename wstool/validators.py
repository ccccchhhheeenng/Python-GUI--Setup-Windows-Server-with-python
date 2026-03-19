from __future__ import annotations

import ipaddress


def require_text(value: str, field_name: str) -> str:
    text = value.strip()
    if not text:
        raise ValueError(f"{field_name} is required.")
    return text


def validate_ipv4(value: str, field_name: str) -> str:
    text = require_text(value, field_name)
    try:
        ipaddress.IPv4Address(text)
    except ipaddress.AddressValueError as error:
        raise ValueError(f"{field_name} must be a valid IPv4 address.") from error
    return text


def validate_ipv6(value: str, field_name: str) -> str:
    text = require_text(value, field_name)
    try:
        ipaddress.IPv6Address(text)
    except ipaddress.AddressValueError as error:
        raise ValueError(f"{field_name} must be a valid IPv6 address.") from error
    return text


def validate_zone_name(value: str, field_name: str = "Zone name") -> str:
    text = require_text(value, field_name)
    if text.startswith(".") or text.endswith(".") or ".." in text:
        raise ValueError(f"{field_name} is not a valid DNS zone name.")
    return text


def validate_network_id(value: str) -> str:
    text = require_text(value, "Network ID")
    try:
        network = ipaddress.IPv4Network(f"{text}/24", strict=True)
    except ValueError as error:
        raise ValueError("Network ID must look like 192.168.1.0.") from error
    return str(network.network_address)


def compute_scope_id(start_range: str) -> str:
    address = ipaddress.IPv4Address(start_range)
    octets = str(address).split(".")
    octets[-1] = "0"
    return ".".join(octets)
