from typing import Optional
from pydantic import BaseModel


class ModelDatabaseCity(BaseModel):
    country_code: Optional[str]
    state1: Optional[str]
    state2: Optional[str]
    city: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    postcode: Optional[str]
    timezone: Optional[str]

    class Config:
        from_attributes = True


class ModelDatabaseASN(BaseModel):
    autonomous_system_number: Optional[int]
    autonomous_system_organization: Optional[str]

    class Config:
        from_attributes = True