#!/bin/bash
set -e  # 遇到错误立即退出

echo "=== 检查系统依赖 ==="
# 安装 git
if ! command -v git &>/dev/null; then
    echo "Git 未安装，尝试安装..."
    sudo apt update && sudo apt install git curl
fi

# 安装 curl
if ! command -v curl &>/dev/null; then
    echo "curl 未安装，尝试安装..."
    sudo apt update && sudo apt install curl
fi

echo "=== 安装 uv ==="
if ! command -v uv &>/dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    echo "uv 已安装，路径: $HOME/.local/bin"
else
    echo "uv 已安装，跳过安装"
fi

echo "=== 克隆项目 ==="
if [ -d "ip" ]; then
    echo "目录 ip 已存在，跳过 git clone"
else
    git clone https://github.com/garinasset/ip.git
fi

cd ip || exit

echo "=== 安装 Python 3.12 ==="
uv python install 3.12

echo "=== 创建虚拟环境 ==="
uv venv

echo "=== 安装依赖（使用锁文件） ==="
uv sync --frozen

echo "=== 完成 ==="
echo "虚拟环境已创建，依赖已安装"
echo "下一步启动 API："
echo "uv run uvicorn main:app --host 0.0.0.0 --port 8000"