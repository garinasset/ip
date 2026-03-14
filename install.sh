#!/bin/bash
set -e  # 遇到错误立即退出

# 颜色输出（可选，增加可读性）
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 临时把 ~/.local/bin 加入 PATH
export PATH="/usr/local/bin:/usr/bin:/bin:$HOME/.local/bin:$PATH"

echo -e "${GREEN}=== 检查系统依赖 ===${NC}"

# 检查 Git
if ! command -v git &>/dev/null; then
    echo -e "${YELLOW}Git 未安装，正在安装...${NC}"
    sudo apt update
    sudo apt install -y git
else
    echo -e "${GREEN}Git 已安装，跳过${NC}"
fi

# 检查 curl
if ! command -v curl &>/dev/null; then
    echo -e "${YELLOW}curl 未安装，正在安装...${NC}"
    sudo apt update
    sudo apt install -y curl
else
    echo -e "${GREEN}curl 已安装，跳过${NC}"
fi

echo -e "${GREEN}=== 安装 uv ===${NC}"
if ! command -v uv &>/dev/null; then
    echo -e "${YELLOW}正在安装 uv...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # 确保 ~/.local/bin 在 PATH 中
    export PATH="$HOME/.local/bin:$PATH"

    # 验证 uv 是否安装成功
    if ! command -v uv &>/dev/null; then
        echo -e "${RED}uv 安装失败，请手动安装${NC}"
        exit 1
    fi
    echo -e "${GREEN}uv 安装完成${NC}"
else
    echo -e "${GREEN}uv 已安装，跳过${NC}"
fi

echo -e "${GREEN}=== 克隆或更新项目 ===${NC}"
# 检查目标目录是否存在
if [ -d "ip" ]; then
    cd ip || { echo -e "${RED}无法进入 ip 目录${NC}"; exit 1; }

    if [ -d ".git" ]; then
        echo -e "${GREEN}已存在 git 仓库，尝试更新...${NC}"
        git pull || { echo -e "${RED}git pull 失败，请手动处理${NC}"; exit 1; }
    else
        echo -e "${RED}目录 ip 已存在，但不是 git 仓库，请手动处理${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}正在克隆项目...${NC}"
    git clone https://github.com/garinasset/ip.git || { echo -e "${RED}git clone 失败${NC}"; exit 1; }
    cd ip || { echo -e "${RED}无法进入 ip 目录${NC}"; exit 1; }
fi

echo -e "${GREEN}=== 安装 Python 3.12 ===${NC}"
# 检查是否已安装 Python 3.12
if ! uv python list | grep -q "3.12"; then
    uv python install 3.12 || { echo -e "${RED}Python 3.12 安装失败${NC}"; exit 1; }
else
    echo -e "${GREEN}Python 3.12 已安装${NC}"
fi

echo -e "${GREEN}Python 版本检查：${NC}"
uv python list | grep "3.12"

echo -e "${GREEN}=== 创建虚拟环境 ===${NC}"
# 检查是否已存在虚拟环境
if [ -d ".venv" ]; then
    echo -e "${YELLOW}虚拟环境已存在，是否重新创建？(y/n)${NC}"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        rm -rf .venv
        uv venv || { echo -e "${RED}虚拟环境创建失败${NC}"; exit 1; }
    else
        echo -e "${GREEN}使用现有虚拟环境${NC}"
    fi
else
    uv venv || { echo -e "${RED}虚拟环境创建失败${NC}"; exit 1; }
fi

echo -e "${GREEN}=== 安装依赖（使用锁文件） ===${NC}"
# 检查 pyproject.toml 或 uv.lock 是否存在
if [ ! -f "pyproject.toml" ] && [ ! -f "uv.lock" ]; then
    echo -e "${RED}错误：找不到 pyproject.toml 或 uv.lock 文件${NC}"
    exit 1
fi

uv sync --frozen || { echo -e "${RED}依赖安装失败${NC}"; exit 1; }

echo -e "${GREEN}=== 安装完成 ===${NC}"
echo -e "${GREEN}虚拟环境已创建，依赖已安装${NC}"
echo -e "${YELLOW}启动 API 的命令示例：${NC}"
echo "uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"

# 可选：显示激活虚拟环境的命令
echo -e "${YELLOW}激活虚拟环境的命令：${NC}"
echo "source .venv/bin/activate"