#!/bin/bash
set -e  # 遇到错误立即退出

# 临时把 ~/.local/bin 加入 PATH
export PATH="$HOME/.local/bin:$PATH"

echo "=== 检查系统依赖 ==="

# 安装 git / curl
for pkg in git curl; do
    if ! command -v $pkg &>/dev/null; then
        echo "$pkg 未安装，正在安装..."
        sudo apt update && sudo apt install -y $pkg
    else
        echo "$pkg 已安装，跳过"
    fi
done

echo "=== 安装 uv ==="
if ! command -v uv &>/dev/null; then
    echo "正在安装 uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "uv 安装完成，请确保 ~/.local/bin 在 PATH 中"
else
    echo "uv 已安装，跳过"
fi

echo "=== 克隆或更新项目 ==="
if [ -d "ip" ]; then
    cd ip || exit
    if [ -d ".git" ]; then
        echo "已存在 git 仓库，尝试更新..."
        git pull
    else
        echo "目录 ip 已存在，但不是 git 仓库，请手动处理"
        exit 1
    fi
else
    git clone https://github.com/garinasset/ip.git
    cd ip || exit
fi

echo "=== 安装 Python 3.12 ==="
uv python install 3.12
echo "Python 版本检查："
uv python list

echo "=== 创建虚拟环境 ==="
uv venv

echo "=== 安装依赖（使用锁文件） ==="
uv sync --frozen

echo "=== 安装完成 ==="
echo "虚拟环境已创建，依赖已安装"
echo "启动 API 的命令示例："
echo "uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"