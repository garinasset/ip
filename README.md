# 免费 IP 查询接口 开发 & Linux 服务器部署 指南

本文档指导用户在 **Linux / macOS** 系统上快速开发 IP API 服务，包含 uv、Python 虚拟环境和依赖管理, 并为非开发者用户提供了 Linux 服务器一键部署脚本.

---

##  1. 二次开发

```bash
git clone https://github.com/garinasset/ip.git
curl -LsSf https://astral.sh/uv/install.sh | sh
cd ip

# 适用 python 3.10+ , 项目开发时 作者 采用 python 3.12.
uv python install 3.12

uv venv
uv sync --frozen
fastapi dev
```

## 2. 部署安装
```bash
curl -LsSf https://raw.githubusercontent.com/garinasset/ip/refs/heads/main/install.sh | bash
```

## 3. 完整卸载
```
rm -rf ip/
```

## 更新与反馈

- GitHub 仓库：[https://github.com/garinasset/ip](https://github.com/garinasset/ip)  
- Issues & Bug 报告：[https://github.com/garinasset/ip/issues](https://github.com/garinasset/ip/issues)