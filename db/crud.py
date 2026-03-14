import maxminddb
from pydantic import IPvAnyAddress

from models.database import ModelDatabaseCity, ModelDatabaseASN

_readers = {}


def init_mmdb():
    _readers["city-ipv4"] = maxminddb.open_database("db/dbip-city-ipv4.mmdb")
    _readers["city-ipv6"] = maxminddb.open_database("db/dbip-city-ipv6.mmdb")
    _readers["asn-ipv4"] = maxminddb.open_database("db/dbip-asn-ipv4.mmdb")
    _readers["asn-ipv6"] = maxminddb.open_database("db/dbip-asn-ipv6.mmdb")


def read_city(ip: IPvAnyAddress) -> ModelDatabaseCity:

    if ip.version == 4:
        return _readers["city-ipv4"].get(str(ip))
    else:
        return _readers["city-ipv6"].get(str(ip))


def read_asn(ip: IPvAnyAddress) -> ModelDatabaseASN:

    if ip.version == 4:
        return _readers["asn-ipv4"].get(str(ip))
    else:
        return _readers["asn-ipv6"].get(str(ip))