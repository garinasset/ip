from typing import Optional
from pydantic import BaseModel
from pydantic import IPvAnyAddress


class ModelResponseIp(BaseModel):
    ip: IPvAnyAddress

class ModelResponseClient(ModelResponseIp):
    user_agent: Optional[str]
    country: Optional[str]
    state: Optional[str]
    city: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]
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