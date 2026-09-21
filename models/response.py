from pydantic import BaseModel, IPvAnyAddress


class ModelResponseIp(BaseModel):
    ip: IPvAnyAddress

class ModelResponseClient(ModelResponseIp):
    user_agent: str | None = None
    country: str | None = None
    region: str | None = None
    city: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    ISP: str | None = None
    ASN: int | None = None
    ASO: str | None = None

class ModelResponseGeolocation(ModelResponseIp):
    country: str | None = None
    region: str | None = None
    city: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    ISP: str | None = None
    ASN: int | None = None
    ASO: str | None = None
