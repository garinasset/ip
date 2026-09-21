# [IP 地理 API © 嘉林数据](https://api.garinasset.com/ip/redoc)
## 🧩 技术栈

| 技术 | 作用 |
| --- | --- |
| [![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/) | Python Web API 框架，负责 API 接口与服务端业务能力 |
| [![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/) | 编程语言，为 API 服务提供运行环境 |
| [![uv](https://img.shields.io/badge/uv-261230?logo=uv&logoColor=white)](https://docs.astral.sh/uv/) | Python 项目与依赖管理，负责虚拟环境、依赖安装与运行 |
| [![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?logo=uvicorn&logoColor=white)](https://www.uvicorn.org/) | ASGI 应用服务器，负责运行 FastAPI 应用并处理 HTTP 请求 |
| [![systemd](https://img.shields.io/badge/systemd-000000?logo=linux&logoColor=white)](https://systemd.io/) | Linux 服务管理，负责 API 服务常驻、启动与自动重启 |
| [![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)](https://github.com/) | 代码托管与版本管理 |
| [![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)](https://docs.github.com/en/actions) | CI/CD 自动化，将代码变更自动部署到生产服务器 |
| [![Nginx](https://img.shields.io/badge/Nginx-009639?logo=nginx&logoColor=white)](https://nginx.org/) | 反向代理与 HTTPS 入口，将域名请求转发至 API 服务 |
| [![Cloudflare](https://img.shields.io/badge/Cloudflare-F38020?logo=cloudflare&logoColor=white)](https://www.cloudflare.com/) | DNS、HTTPS 与负载均衡，连接用户与多台生产服务器 |

## 🚀 部署设计

**GitHub → GitHub Actions → SSH → 服务器集群 → systemd → Uvicorn → FastAPI → Nginx → Cloudflare**

采用 **GitHub Actions + SSH** 实现自动部署。服务器端由 **systemd** 管理 Uvicorn 服务进程，**Uvicorn** 负责运行 FastAPI 应用，**FastAPI** 提供 API 接口；Nginx 提供 Web 入口，Cloudflare Load Balancing 负责多节点流量调度。

## 🔗 应用

[https://api.garinasset.com/ip/redoc](https://api.garinasset.com/ip/redoc)

## 📚 官方文档

[FastAPI](https://fastapi.tiangolo.com/) ·
[Python](https://docs.python.org/3/) ·
[uv](https://docs.astral.sh/uv/) ·
[systemd](https://systemd.io/) ·
[Uvicorn](https://www.uvicorn.org/) ·
[GitHub Actions](https://docs.github.com/en/actions) ·
[Nginx](https://nginx.org/en/docs/) ·
[Cloudflare Load Balancing](https://developers.cloudflare.com/load-balancing/)