```bash
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


TMP_DB_DIR="$(mktemp -d "$DB_DIR/.download.XXXXXX")"

cleanup() {
    rm -rf "$TMP_DB_DIR"
}

trap cleanup EXIT

echo "==> Create temporary database directory:"
echo "    $TMP_DB_DIR"

# 下载函数
download_file() {
    local url="$1"
    local filename="$2"

    echo "==> Downloading $filename"

    curl \
        --fail \
        --location \
        --show-error \
        --silent \
        --retry 3 \
        --retry-all-errors \
        --connect-timeout 15 \
        --max-time 600 \
        --output "$TMP_DB_DIR/$filename" \
        "$url"

    if [ ! -s "$TMP_DB_DIR/$filename" ]; then
        echo "ERROR: Downloaded file is empty: $filename"
        return 1
    fi

    echo "    OK: $filename"
}


# 下载 GeoLite2 ASN
download_file \
    "https://github.com/sapics/ip-location-db/releases/download/latest/geolite2-asn.mmdb" \
    "geolite2-asn.mmdb"


# 下载 DBIP City IPv4
download_file \
    "https://github.com/sapics/ip-location-db/releases/download/latest/dbip-city-ipv4.mmdb" \
    "dbip-city-ipv4.mmdb"


# 下载 DBIP City IPv6
download_file \
    "https://github.com/sapics/ip-location-db/releases/download/latest/dbip-city-ipv6.mmdb" \
    "dbip-city-ipv6.mmdb"


# 下载 ISP 数据
download_file \
    "https://gaoyifan.github.io/china-operator-ip/cernet46.txt" \
    "cernet46.txt"

download_file \
    "https://gaoyifan.github.io/china-operator-ip/chinanet46.txt" \
    "chinanet46.txt"

download_file \
    "https://gaoyifan.github.io/china-operator-ip/cmcc46.txt" \
    "cmcc46.txt"

download_file \
    "https://gaoyifan.github.io/china-operator-ip/unicom46.txt" \
    "unicom46.txt"

download_file \
    "https://gaoyifan.github.io/china-operator-ip/cstnet46.txt" \
    "cstnet46.txt"

download_file \
    "https://gaoyifan.github.io/china-operator-ip/drpeng46.txt" \
    "drpeng46.txt"

download_file \
    "https://gaoyifan.github.io/china-operator-ip/googlecn46.txt" \
    "googlecn46.txt"


# 所有数据库下载完成后，统一替换正式文件
echo "==> All databases downloaded successfully"

mv "$TMP_DB_DIR/geolite2-asn.mmdb" "$DB_DIR/geolite2-asn.mmdb"
mv "$TMP_DB_DIR/dbip-city-ipv4.mmdb" "$DB_DIR/dbip-city-ipv4.mmdb"
mv "$TMP_DB_DIR/dbip-city-ipv6.mmdb" "$DB_DIR/dbip-city-ipv6.mmdb"

mv "$TMP_DB_DIR/cernet46.txt" "$DB_DIR/cernet46.txt"
mv "$TMP_DB_DIR/chinanet46.txt" "$DB_DIR/chinanet46.txt"
mv "$TMP_DB_DIR/cmcc46.txt" "$DB_DIR/cmcc46.txt"
mv "$TMP_DB_DIR/unicom46.txt" "$DB_DIR/unicom46.txt"
mv "$TMP_DB_DIR/cstnet46.txt" "$DB_DIR/cstnet46.txt"
mv "$TMP_DB_DIR/drpeng46.txt" "$DB_DIR/drpeng46.txt"
mv "$TMP_DB_DIR/googlecn46.txt" "$DB_DIR/googlecn46.txt"


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
sudo systemctl --no-pager --full status "$SERVICE" | head -n 10


# 完成
echo "==> Deployment finished."
```