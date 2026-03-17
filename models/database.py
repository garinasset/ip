from typing import Optional

from pydantic import BaseModel, model_validator

# 官方数据库模型
class ModelDatabaseIPGeolocation(BaseModel):
    # country_code: Optional[str] = None 含义：
    # 1. Optional[str]：字段的值可以是 str 或 None
    # 2. = None：字段是“可选的”，即输入数据(对应数据库输出)中可以缺失该字段
    # 3. 如果输入中没有该字段，Pydantic 会自动赋值为 None
    # 4. 但在 pydantic 模型实例中，该字段会始终存在（不会缺失），只是值可能为 None
    continent: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    region_code: Optional[int] = None
    city: Optional[str] = None
    metro_code: Optional[int] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    postcode: Optional[str] = None
    timezone: Optional[str] = None
    ISP: Optional[str] = None
    ASN: Optional[int] = None
    ASO: Optional[str] = None

    class Config:

        # 默认行为: Pydantic 只接收 dict / mapping 类型的输入
        # 增强兼容: from_attributes 允许 dict / mapping 以及 对象属性 读取字段
        from_attributes = True

    @model_validator(mode="before")
    @classmethod
    def map_database_fields(cls, values: dict) -> dict:
        """
        在模型初始化之前，把数据库字段映射到统一字段
        city 数据库：
            country_code -> country
            state1 -> region

        ASN 数据库：
            autonomous_system_number -> ASN
            autonomous_system_organization -> ASO
        """
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