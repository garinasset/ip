# 免费 IP 查询接口 开发 & Linux 服务器部署 指南

本文档指导用户在 **Linux / macOS** 系统上快速开发 IP API 服务，包含 uv、Python 虚拟环境和依赖管理, 并为非开发者用户提供了 Linux 服务器一键部署脚本.

---

##  1️⃣ 开发

```bash
git clone https://github.com/garinasset/ip.git

# Install uv with official standalone installer
curl -LsSf https://astral.sh/uv/install.sh | sh

cd ip

# 如果系统已安装 python3.12, 可跳过. 理论适用python 3.10+ , 未经测试.
uv python install 3.12

uv venv
uv sync --frozen

fastapi dev
```

##  2️⃣ Linux 服务器部署 (适用基于 Debian 的操作系统, 例如ubuntu 等)
```bash
curl -LsSf https://https://raw.githubusercontent.com/garinasset/ip/refs/heads/main/install.sh | sh
```

## 3️⃣ 卸载
```
rm -rf ip/
```

## 更新与反馈

- GitHub 仓库：[https://github.com/garinasset/ip](https://github.com/garinasset/ip)  
- Issues & Bug 报告：[https://github.com/garinasset/ip/issues](https://github.com/garinasset/ip/issues)  
- 自动更新：脚本内配置了 `@updateURL` 指向 GitHub Raw 文件，Tampermonkey 会自动检查更新