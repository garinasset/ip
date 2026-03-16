import ipaddress
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Request, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import IPvAnyAddress
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
    title="api.garinasset.com",
    version="1.0.1",
    summary="免费 IP 地理信息查询接口",
    contact={
        "name": "嘉林资产",
        "url": "https://garinasset.com",
        "email": "contact@garinasset.com",
    },
    license_info={
        "name": "CC BY 4.0",
        "identifier": "CC-BY-4.0",
    }
)

# 允许跨域
app.add_middleware(
    CORSMiddleware,
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
                        "example": "Hello ip!\n"
                    }
                }
            }
         }
)
async def root():
    return f"Hello ip!\n"


@app.get("/", summary="响应 IP 地址",
         response_class=PlainTextResponse,
         responses={
             200: {
                "content": {
                    "text/plain": {
                        "example": "220.181.12.12\n"
                    }
                }
            }
         }
)
async def get_ip(request: Request):
    return f"{request.client.host}\n"


@app.get("/client", summary="响应 客户端 信息", response_model=ModelResponseClient)
async def get_client(request: Request):

    ip = ipaddress.ip_address(request.client.host)
    headers = request.headers

    city = crud.read_city(ip) or {}
    asn = crud.read_asn(ip) or {}

    client = ModelResponseClient(
        ip=ip,
        user_agent=headers.get("user-agent"),
        country=city.get("country_code"),
        state=city.get("state1"),
        city=city.get("city"),
        latitude=city.get("latitude"),
        longitude=city.get("longitude"),
        ASN=asn.get("autonomous_system_number"),
        ASO=asn.get("autonomous_system_organization"),
    )

    return client


@app.get("/{ip_address}", summary="查询 IP 地理信息", response_model=ModelResponseGeolocation)
async def lookup_ip(
        ip_address: Annotated[IPvAnyAddress,Path(title="IP 地址")],
):
    ip = ip_address
    city = crud.read_city(ip) or {}
    asn = crud.read_asn(ip) or {}

    geolocation = ModelResponseGeolocation(
        ip=ip,
        country=city.get("country_code"),
        state=city.get("state1"),
        city=city.get("city"),
        longitude=city.get("longitude"),
        latitude=city.get("latitude"),
        ASN=asn.get("autonomous_system_number"),
        ASO=asn.get("autonomous_system_organization"),
    )

    return geolocation
