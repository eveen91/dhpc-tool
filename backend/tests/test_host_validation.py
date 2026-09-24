import pytest
from pydantic import ValidationError

from app.schemas.hosts import HostCreate


def test_host_normalizes_mac_address() -> None:
    host = HostCreate(
        hostname="printer-01",
        mac_address="AA-BB-CC-DD-EE-FF",
        ipv4_address="192.168.1.50",
        subnet_name="Office",
    )

    assert host.mac_address == "aa:bb:cc:dd:ee:ff"


def test_host_rejects_invalid_hostname() -> None:
    with pytest.raises(ValidationError, match="hostname"):
        HostCreate(
            hostname="host; range 1.2.3.4",
            mac_address="aa:bb:cc:dd:ee:ff",
            ipv4_address="192.168.1.50",
            subnet_name="Office",
        )
