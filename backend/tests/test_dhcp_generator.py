import pytest

from app.domain.dhcp.generator import DhcpConfigurationError, generate_dhcpd_conf
from app.schemas.hosts import HostCreate
from app.schemas.subnets import SubnetCreate


def test_generator_creates_deterministic_static_configuration_without_range() -> None:
    subnet = SubnetCreate(
        name="Office",
        network="192.168.10.0/24",
        gateway="192.168.10.1",
        dns_servers=["192.168.10.10"],
    )
    host = HostCreate(
        hostname="laptop01",
        mac_address="AA-BB-CC-DD-EE-FF",
        ipv4_address="192.168.10.100",
        subnet_name="Office",
    )

    result = generate_dhcpd_conf([subnet], [host])

    assert "deny unknown-clients;" in result.content
    assert "range" not in result.content.lower()
    assert "hardware ethernet aa:bb:cc:dd:ee:ff;" in result.content
    assert result.sha256


def test_generator_rejects_unsafe_range_option() -> None:
    subnet = SubnetCreate(
        name="Office",
        network="192.168.10.0/24",
        gateway="192.168.10.1",
        additional_options={"range": "192.168.10.20 192.168.10.30"},
    )

    with pytest.raises(DhcpConfigurationError, match="range"):
        generate_dhcpd_conf([subnet], [])
