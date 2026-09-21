from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator


class Header(BaseModel):
    # ------------------------------
    # 常规 HTTP Header
    # ------------------------------
    connection: str | None = None
    content_length: str | None = None
    sec_ch_ua: str | None = None
    accept: str | None = None
    sec_ch_ua_mobile: str | None = None
    user_agent: str | None = None
    sec_ch_ua_platform: str | None = None
    origin: str | None = None
    sec_fetch_site: str | None = None
    sec_fetch_mode: str | None = None
    sec_fetch_dest: str | None = None
    referer: str | None = None
    priority: str | None = None
    accept_encoding: str | None = None
    accept_language: str | None = None
    cookie: str | None = None

    # ------------------------------
    # Nginx 透传
    # ------------------------------
    host: str | None = None
    x_real_ip: str | None = None
    x_forwarded_for: str | None = None

    # ------------------------------
    # Cloudflare Geo Header
    # ------------------------------
    cf_ipcountry: str | None = None
    cf_ipcity: str | None = None
    cf_ipcontinent: str | None = None
    cf_iplatitude: str | None = None
    cf_iplongitude: str | None = None
    cf_region: str | None = None
    cf_region_code: str | None = None
    cf_metro_code: str | None = None
    cf_postal_code: str | None = None
    cf_timezone: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def map_headers_fields(cls, values: Any) -> dict[str, Any] | Any:
        if values is None:
            return {}

        # 兼容 starlette Headers 等 Mapping 类型输入。
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
