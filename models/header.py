from typing import Optional
from pydantic import BaseModel, model_validator


class Header(BaseModel):
    # ------------------------------
    # 常规 HTTP Header
    # ------------------------------
    connection: Optional[str] = None
    content_length: Optional[str] = None
    sec_ch_ua: Optional[str] = None
    accept: Optional[str] = None
    sec_ch_ua_mobile: Optional[str] = None
    user_agent: Optional[str] = None
    sec_ch_ua_platform: Optional[str] = None
    origin: Optional[str] = None
    sec_fetch_site: Optional[str] = None
    sec_fetch_mode: Optional[str] = None
    sec_fetch_dest: Optional[str] = None
    referer: Optional[str] = None
    priority: Optional[str] = None
    accept_encoding: Optional[str] = None
    accept_language: Optional[str] = None
    cookie: Optional[str] = None

    # ------------------------------
    # Nginx 透传
    # ------------------------------
    host: Optional[str] = None
    x_real_ip: Optional[str] = None
    x_forwarded_for: Optional[str] = None

    # ------------------------------
    # Cloudflare Geo Header
    # ------------------------------
    cf_ipcountry: Optional[str] = None
    cf_ipcity: Optional[str] = None
    cf_ipcontinent: Optional[str] = None
    cf_iplatitude: Optional[str] = None
    cf_iplongitude: Optional[str] = None
    cf_region: Optional[str] = None
    cf_region_code: Optional[str] = None
    cf_metro_code: Optional[str] = None
    cf_postal_code: Optional[str] = None
    cf_timezone: Optional[str] = None

    class Config:
        # 默认行为: Pydantic 只接收 dict / mapping 类型的输入
        # 增强兼容: from_attributes 允许 dict / mapping 以及 对象属性 读取字段
        from_attributes = True

    @model_validator(mode="before")
    @classmethod
    def map_headers_fields(cls, values) -> dict:
        # 确保是 dict 类型
        values_dict = dict(values)

        mapping = {
            "host": "host",
            "x-real-ip": "x_real_ip",
            "x-forwarded-for": "x_forwarded_for",
            "connection": "connection",
            "content-length": "content_length",
            "sec-ch-ua": "sec_ch_ua",
            "accept": "accept",
            "sec-ch-ua-mobile": "sec_ch_ua_mobile",
            "user-agent": "user_agent",
            "sec-ch-ua-platform": "sec_ch_ua_platform",
            "origin": "origin",
            "sec-fetch-site": "sec_fetch_site",
            "sec-fetch-mode": "sec_fetch_mode",
            "sec-fetch-dest": "sec_fetch_dest",
            "referer": "referer",
            "priority": "priority",
            "accept-encoding": "accept_encoding",
            "accept-language": "accept_language",
            "cookie": "cookie",
            "cf-ipcountry": "cf_ipcountry",
            "cf-ipcity": "cf_ipcity",
            "cf-ipcontinent": "cf_ipcontinent",
            "cf-iplatitude": "cf_iplatitude",
            "cf-iplongitude": "cf_iplongitude",
            "cf-region": "cf_region",
            "cf-region-code": "cf_region_code",
            "cf-metro-code": "cf_metro_code",
            "cf-postal-code": "cf_postal_code",
            "cf-timezone": "cf_timezone",
        }

        # 做映射
        new_values = {}
        for src, dest in mapping.items():
            if src in values_dict and values_dict[src] is not None:
                new_values[dest] = values_dict[src]

        return new_values