from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator

# 官方数据库模型
class ModelDatabaseIPGeolocation(BaseModel):
    # country_code: Optional[str] = None 含义：
    # 1. Optional[str]：字段的值可以是 str 或 None
    # 2. = None：字段是“可选的”，即输入数据(对应数据库输出)中可以缺失该字段
    # 3. 如果输入数据中没有该字段，Pydantic 会自动赋值为 None
    # 4. 但在 pydantic 模型实例中，该字段会始终存在（不会缺失），只是值可能为 None
    continent: str | None = None
    country: str | None = None
    region: str | None = None
    region_code: int | None = None
    city: str | None = None
    metro_code: int | None = None
    longitude: float | None = None
    latitude: float | None = None
    postcode: str | None = None
    timezone: str | None = None
    ISP: str | None = None
    ASN: int | None = None
    ASO: str | None = None

    # Pydantic v2 配置写法，避免 class-based Config 的弃用警告。
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def map_database_fields(cls, values: Any) -> Any:
        """
        在模型初始化之前，把数据库字段映射到统一字段
        city 数据库：
            country_code -> country
            state1 -> region

        ASN 数据库：
            autonomous_system_number -> ASN
            autonomous_system_organization -> ASO
        """
        if not isinstance(values, dict):
            return values

        mapping = {
            "country_code": "country",
            "state1": "region",
            "autonomous_system_number": "ASN",
            "autonomous_system_organization": "ASO",
        }
        for src, dest in mapping.items():
            if src in values and values[src] is not None:
                values[dest] = values.pop(src)
        return values
