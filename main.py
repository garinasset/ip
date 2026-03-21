import ipaddress
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Request, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import IPvAnyAddress
from starlette.responses import PlainTextResponse

from db import crud
from models.header import Header
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
    version="2.0.0",
    summary="免费 IP 地理信息查询接口",
    contact={
        "name": "嘉林数据",
        "url": "https://ip.garinasset.com",
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


@app.get("/{ip_address}", summary="查询 IP 地理信息", response_model=ModelResponseGeolocation)
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
