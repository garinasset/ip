import maxminddb
from collections.abc import Mapping
from ipaddress import IPv4Address, IPv6Address
from typing import Any

from models.database import ModelDatabaseIPGeolocation

_readers: dict[str, maxminddb.Reader] = {}


def _merge_if_mapping(target: dict[str, Any], data: Any) -> None:
    if isinstance(data, Mapping):
        target.update(data)


def init_mmdb():
    _readers["city-ipv4"] = maxminddb.open_database("db/dbip-city-ipv4.mmdb")
    _readers["city-ipv6"] = maxminddb.open_database("db/dbip-city-ipv6.mmdb")
    _readers["asn"] = maxminddb.open_database("db/geolite2-asn.mmdb")
    _readers["isp-ipv4"] = maxminddb.open_database("db/isp-ipv4.mmdb")
    _readers["isp-ipv6"] = maxminddb.open_database("db/isp-ipv6.mmdb")


def read_ip_geolocation(ip: IPv4Address | IPv6Address) -> ModelDatabaseIPGeolocation:
    """
    从 city-ipv4/6 + asn 数据库读取数据，统一整合成 IPGeolocation 模型
    """
    # 读取城市信息
    ip_text = ip.compressed
    if ip.version == 4:
        city_data = _readers["city-ipv4"].get(ip_text)
    else:
        city_data = _readers["city-ipv6"].get(ip_text)

    # 读取 ASN 信息
    asn_data = _readers["asn"].get(ip_text)

    # 读取ISP信息
    if ip.version == 4:
        isp_data = _readers["isp-ipv4"].get(ip_text)
    else:
        isp_data = _readers["isp-ipv6"].get(ip_text)

    # pydantic 模型实例 输入数据 空保护
    combined_data = {}

    # 合并两个 dict（后面的字典会覆盖前面的同名字段）
    _merge_if_mapping(combined_data, city_data)
    _merge_if_mapping(combined_data, asn_data)
    _merge_if_mapping(combined_data, isp_data)

    return ModelDatabaseIPGeolocation(**combined_data)
