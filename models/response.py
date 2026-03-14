from typing import Optional
from pydantic import BaseModel
from pydantic import IPvAnyAddress


class ModelResponseIp(BaseModel):
    ip: IPvAnyAddress

class ModelResponseClient(ModelResponseIp):
    user_agent: Optional[str]
    # connection: Optional[str]
    # content_length: Optional[str]
    # sec_ch_ua: Optional[str]
    # accept: Optional[str]
    # sec_ch_ua_mobile: Optional[str]
    # sec_ch_ua_platform: Optional[str]
    # origin: Optional[str]
    # sec_fetch_site: Optional[str]
    # sec_fetch_mode: Optional[str]
    # sec_fetch_dest: Optional[str]
    # referer: Optional[str]
    # accept_encoding: Optional[str]
    # accept_language: Optional[str]
    # cookie: Optional[str]
    country: Optional[str]
    state: Optional[str]
    city: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]
    # postcode: Optional[str]
    # timezone: Optional[str]
    ASN: Optional[int]
    ASO: Optional[str]

class ModelResponseGeolocation(ModelResponseIp):
    country: Optional[str]
    state: Optional[str]
    city: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]
    ASN: Optional[int]
    ASO: Optional[str]