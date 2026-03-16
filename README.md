# 免费 IP 地理信息查询接口 - 嘉林数据

## 📖 项目简介

一个免费、开源、快速的 IP 地理信息查询服务。基于 mmdb 数据库，可提供稳定、毫秒级的 API 查询服务。

- **在线体验**：https://ip.garinasset.com/
- **接口文档**：https://api.garinasset.com/ip/redoc
- **开源仓库**：https://github.com/garinasset/ip

## ✨ 核心特性

- 🆓 **完全免费**：无需 API Key，无调用限制
- 🚀 **高性能**：在线接口采用 双机集群部署，负载均衡
- 📦 **准确可靠**：采用 DB-IP 数据库，数据质量还不错
- 🔧 **易于部署**：一键安装脚本，快速自托管
- 📚 **完整文档**：提供 ReDoc 接口文档

## 💻 开发调试

如果你想在本地运行和调试此项目：

```bash
# 1. 克隆仓库
git clone https://github.com/garinasset/ip.git
cd ip

# 2. 安装 UV 包管理器
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. 安装指定 Python 版本（需要 3.10+，推荐 3.12）
uv python install 3.12

# 4. 创建虚拟环境并安装依赖
uv venv
uv sync --frozen

# 5. 启动开发服务器
fastapi dev
```

## 🚀 一键部署

你可以使用我们提供的一键安装脚本，快速部署到你的服务器：
```bash
curl -LsSf https://raw.githubusercontent.com/garinasset/ip/refs/heads/main/install.sh | bash
```

该脚本会自动：

- 检测系统环境
- 安装必要的依赖
- 配置 Python 环境
- 下载最新的 IP 数据库

## 🗑️ 完全卸载

如果需要完全卸载:

```bash
# 删除项目目录即可
rm -rf ip/
```

## 📬 更新与反馈
- GitHub 仓库：[https://github.com/garinasset/ip](https://github.com/garinasset/ip)  
- Issues & Bug 报告：[https://github.com/garinasset/ip/issues](https://github.com/garinasset/ip/issues)