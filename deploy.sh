#!/bin/bash

set -Eeuo pipefail

# 基础配置

APP_DIR="/home/deploy/ip"
DB_DIR="$APP_DIR/db"
SERVICE="uvicorn-ip.service"
UV="/home/deploy/.local/bin/uv"

# 错误处理

trap 'echo "ERROR: Deployment failed at line $LINENO"' ERR

# 环境变量

export PATH="/home/deploy/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

echo "==> Starting deployment"

cd "$APP_DIR"

echo "==> uv: $("$UV" --version)"
echo "==> Python: $("$UV" run python --version)"
echo "==> Python path: $("$UV" run which python)"

echo "==> Installing dependencies"
"$UV" sync --frozen

# 创建临时数据库目录
#
# 所有下载文件先进入这里。
# 只有 curl 完整成功的文件才允许移动到正式数据库目录。

TMP_DB_DIR="$(mktemp -d "$DB_DIR/.download.XXXXXX")"

cleanup() {
    rm -rf "$TMP_DB_DIR"
}

trap cleanup EXIT

echo "==> Create temporary database directory:"
echo "    $TMP_DB_DIR"

# 下载函数
#
# 下载成功：
#   文件保留在 TMP_DB_DIR，等待后续移动。
#
# 下载失败：
#   删除可能产生的残缺文件。
#   返回 1，但不会让整个部署停止。
#
# 注意：
#   curl 放在 if 条件中，因此 set -e 不会因为预期的下载失败
#   而直接终止整个脚本。

download_file() {
    local url="$1"
    local filename="$2"
    local tmp_file="$TMP_DB_DIR/$filename"

    echo "==> Downloading $filename"

    # 防止临时目录中存在同名残留文件
    rm -f "$tmp_file"

    if curl \
        --fail \
        --location \
        --show-error \
        --silent \
        --retry 3 \
        --retry-all-errors \
        --connect-timeout 15 \
        --max-time 600 \
        --output "$tmp_file" \
        "$url"
    then
        # curl 成功后，再确认文件不是空文件
        if [ ! -s "$tmp_file" ]; then
            echo "ERROR: Downloaded file is empty: $filename"
            rm -f "$tmp_file"
            return 1
        fi

        echo "    OK: $filename"
        return 0
    else
        echo "ERROR: Download failed: $filename"
        rm -f "$tmp_file"
        return 1
    fi
}

# 移动函数
#
# 只有临时目录中存在有效文件时才移动。
#
# 如果下载失败：
#   临时文件不存在
#   -> 跳过
#   -> 正式目录中的旧文件保持不变

move_if_downloaded() {
    local filename="$1"
    local tmp_file="$TMP_DB_DIR/$filename"
    local db_file="$DB_DIR/$filename"

    if [ -s "$tmp_file" ]; then
        mv "$tmp_file" "$db_file"
        echo "    Updated: $filename"
    else
        echo "    Skipped: $filename"
    fi
}

# 下载 GeoLite2 ASN

download_file \
    "https://github.com/sapics/ip-location-db/releases/download/latest/geolite2-asn.mmdb" \
    "geolite2-asn.mmdb" || true

# 下载 DBIP City IPv4

download_file \
    "https://github.com/sapics/ip-location-db/releases/download/latest/dbip-city-ipv4.mmdb" \
    "dbip-city-ipv4.mmdb" || true

# # 下载 DBIP City IPv6

# download_file \
#     "https://github.com/sapics/ip-location-db/releases/download/latest/dbip-city-ipv6.mmdb" \
#     "dbip-city-ipv6.mmdb" || true

# # 下载 GeoLite2 City IPv4

# download_file \
#     "https://github.com/sapics/ip-location-db/releases/download/latest/geolite2-city-ipv4.mmdb" \
#     "geolite2-city-ipv4.mmdb" || true

# 下载 GeoLite2 City IPv6

download_file \
    "https://github.com/sapics/ip-location-db/releases/download/latest/geolite2-city-ipv6.mmdb" \
    "geolite2-city-ipv6.mmdb" || true

# 下载 ISP 数据

download_file \
    "https://gaoyifan.github.io/china-operator-ip/cernet46.txt" \
    "cernet46.txt" || true

download_file \
    "https://gaoyifan.github.io/china-operator-ip/chinanet46.txt" \
    "chinanet46.txt" || true

download_file \
    "https://gaoyifan.github.io/china-operator-ip/cmcc46.txt" \
    "cmcc46.txt" || true

download_file \
    "https://gaoyifan.github.io/china-operator-ip/unicom46.txt" \
    "unicom46.txt" || true

download_file \
    "https://gaoyifan.github.io/china-operator-ip/cstnet46.txt" \
    "cstnet46.txt" || true

download_file \
    "https://gaoyifan.github.io/china-operator-ip/drpeng46.txt" \
    "drpeng46.txt" || true

download_file \
    "https://gaoyifan.github.io/china-operator-ip/googlecn46.txt" \
    "googlecn46.txt" || true

# 更新正式数据库
#
# 每个文件独立处理：
#   下载成功 -> 更新对应正式文件
#   下载失败 -> 跳过，对应正式文件保持旧版本

echo "==> Updating successfully downloaded databases"

move_if_downloaded "geolite2-asn.mmdb"
# move_if_downloaded "dbip-city-ipv4.mmdb"
# move_if_downloaded "dbip-city-ipv6.mmdb"
move_if_downloaded "geolite2-city-ipv4.mmdb"
move_if_downloaded "geolite2-city-ipv6.mmdb"

move_if_downloaded "cernet46.txt"
move_if_downloaded "chinanet46.txt"
move_if_downloaded "cmcc46.txt"
move_if_downloaded "unicom46.txt"
move_if_downloaded "cstnet46.txt"
move_if_downloaded "drpeng46.txt"
move_if_downloaded "googlecn46.txt"

# 构建 ISP 数据库

echo "==> Building ISP database"

cd "$DB_DIR"

"$UV" run build_isp_mmdb.py

cd "$APP_DIR"

# 重启服务

echo "==> Restarting $SERVICE"

sudo systemctl restart "$SERVICE"

# 检查服务状态

echo "==> Checking service status"

sudo systemctl --no-pager --full status "$SERVICE"

# 完成

echo "==> Deployment finished."