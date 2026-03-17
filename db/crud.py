import maxminddb
from pydantic import IPvAnyAddress

from models.database import ModelDatabaseIPGeolocation

_readers = {}


def init_mmdb():
    _readers["city-ipv4"] = maxminddb.open_database("db/dbip-city-ipv4.mmdb")
    _readers["city-ipv6"] = maxminddb.open_database("db/dbip-city-ipv6.mmdb")
    _readers["asn"] = maxminddb.open_database("db/asn.mmdb")

def read_ip_geolocation(ip: IPvAnyAddress) -> ModelDatabaseIPGeolocation:
    """
    从 city-ipv4/6 + asn 数据库读取数据，统一整合成 IPGeolocation 模型
    """
    # 读取城市信息
    if ip.version == 4:
        city_data = _readers["city-ipv4"].get(str(ip))
    else:
        city_data = _readers["city-ipv6"].get(str(ip))

    # 读取 ASN 信息
    asn_data = _readers["asn"].get(str(ip))

    # pydantic 模型实例 输入数据 空保护
    combined_data = {}

    # 合并两个 dict（后面的字典会覆盖前面的同名字段）
    if city_data:
        combined_data.update(city_data)
    if asn_data:
        combined_data.update(asn_data)

    return ModelDatabaseIPGeolocation(**combined_data)