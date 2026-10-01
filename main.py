import ipaddress
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Request, Path
from pydantic import IPvAnyAddress
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse

from db import crud
from models.response import ModelResponseClient, ModelResponseGeolocation


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # 调用数据库初始化函数 以 一次性加载数据库
    crud.init_mmdb()
    yield


app = FastAPI(
    lifespan=lifespan,
    root_path="/ip",
    title="https://api.garinasset.com/ip",
    version="4.0.0",
    summary="IP 地理 API © 嘉林数据 ",
    contact={
        "name": "技术支持",
        "url": "https://ip.garinasset.com",
        "email": "support@garinasset.com",
    },
    license_info={
        "name": "CC BY 4.0",
        "identifier": "CC-BY-4.0",
    }
)


# 允许跨域
app.add_middleware(
    CORSMiddleware,  # type: ignore[arg-type]
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("", summary="Hello ip! 🚀 https://api.garinasset.com/ip",
         response_class=PlainTextResponse,
         responses={
             200: {
                "content": {
                    "text/plain": {
                        "example": "Hello ip!"
                    }
                }
            }
         }  
)
async def root():
    return f"Hello ip!"


@app.get("/", summary="响应 本地 IP 地址",
         response_class=PlainTextResponse,
         responses={
             200: {
                "content": {
                    "text/plain": {
                        "example": "220.181.12.12"
                    }
                }
            }
         }
)
async def get_ip(request: Request):
    client = request.client
    assert client is not None
    return f"{client.host}"


@app.get("/client", summary="响应 本地客户端 信息", response_model=ModelResponseClient)
async def get_client(request: Request):
    client = request.client
    assert client is not None
    ip = ipaddress.ip_address(client.host)

    # 未来应用: 如果需要更多 header 信息
    # headers = Header.model_validate(request.headers)

    info = crud.read_ip_geolocation(ip)

    client = ModelResponseClient(
        ip=ip,

        # 未来应用: 如果需要更多 header 信息的调用示例
        # user_agent=headers.user_agent,

        user_agent=request.headers.get("User-Agent"),
        country=info.country,
        region=info.region,
        city=info.city,
        latitude=info.latitude,
        longitude=info.longitude,
        ISP=info.ISP,
        ASN=info.ASN,
        ASO=info.ASO,
    )

    return client


@app.get("/{ip_address}", summary="返回 指定 IP 地址的 地理信息", response_model=ModelResponseGeolocation)
async def lookup_ip(
        ip_address: Annotated[IPvAnyAddress,Path(title="IP 地址")],
):
    ip = ip_address

    info = crud.read_ip_geolocation(ip)

    geolocation = ModelResponseGeolocation(
        ip=ip,
        country=info.country,
        region=info.region,
        city=info.city,
        latitude=info.latitude,
        longitude=info.longitude,
        ISP=info.ISP,
        ASN=info.ASN,
        ASO=info.ASO
    )

    return geolocation


@app.get("/{ip_address}/country", summary="返回 指定 IP 地址的 国家代码 ( ISO 3166-1 alpha-2 )",
        response_class=PlainTextResponse,
                 responses={
                     200: {
                        "content": {
                            "text/plain": {
                                "example": "CN"
                            }
                        }
                    }
                 }  
        )
async def lookup_ip_country(
        ip_address: Annotated[IPvAnyAddress,Path(title="IP 地址")],
):
    ip = ip_address

    info = crud.read_ip_geolocation(ip)

    if info is None or not info.country:
        return "ZZ"

    return f"{info.country}"


@app.get("/{ip_address}/isp", summary="返回 指定 IP 地址的 运营商",
        response_class=PlainTextResponse,
                 responses={
                     200: {
                        "content": {
                            "text/plain": {
                                "example": "中国移动"
                            }
                        }
                    }
                 }  
        )
async def lookup_ip_isp(
        ip_address: Annotated[IPvAnyAddress,Path(title="IP 地址")],
):
    ip = ip_address

    info = crud.read_ip_geolocation(ip)

    if info is None or not info.ISP:
        return "未知"

    return f"{info.ISP}"
