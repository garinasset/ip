import os
from netaddr import IPNetwork, IPSet
from mmdb_writer import MMDBWriter

# ===============================
# 修改 7 个文件 + 运营商名称
# ===============================
FILES = {
    "chinanet46.txt": "中国电信",
    "unicom46.txt": "中国联通",
    "cmcc46.txt": "中国移动",
    "drpeng46.txt": "鹏博士",
    "cernet46.txt": "教育网",
    "cstnet46.txt": "科技网",
    "googlecn46.txt": "谷歌中国"
}

OUTPUT_DB_IPV4 = "isp-ipv4.mmdb"
OUTPUT_DB_IPV6 = "isp-ipv6.mmdb"


def load_networks():
    """
    读取所有 txt 文件，返回两个列表：
    - ipv4_records: [(IPSet, data), ...]
    - ipv6_records: [(IPSet, data), ...]
    """
    ipv4_records = []
    ipv6_records = []

    base_dir = os.path.dirname(os.path.abspath(__file__))

    for filename, isp_name in FILES.items():
        file_path = os.path.join(base_dir, filename)

        if not os.path.exists(file_path):
            print(f"[WARNING] 文件不存在: {file_path}")
            continue

        ipv4_ipset = IPSet()
        ipv6_ipset = IPSet()

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    net = IPNetwork(line)
                    if net.version == 4:
                        ipv4_ipset.add(net)
                    else:
                        ipv6_ipset.add(net)
                except Exception as e:
                    print(f"[ERROR] {filename}: {line} -> {e}")

        if ipv4_ipset:
            ipv4_records.append((ipv4_ipset, {"ISP": isp_name}))
        if ipv6_ipset:
            ipv6_records.append((ipv6_ipset, {"ISP": isp_name}))

    return ipv4_records, ipv6_records


def build_mmdb(records, output_file, ip_version):
    """
    根据 records 构建 MMDB 文件
    """
    # 官方推荐写法，指定 IP 版本、数据库类型、语言和描述
    writer = MMDBWriter(
        ip_version,
        database_type="ISP-DB",
        languages=["ZH"],
        description="运营商数据库"
    )

    for ipset, data in records:
        try:
            writer.insert_network(ipset, data)
        except Exception as e:
            print(f"[INSERT ERROR] {ipset} -> {e}")

    writer.to_db_file(output_file)
    print(f"[OK] MMDB generated: {output_file}")


def main():
    ipv4_records, ipv6_records = load_networks()
    print(f"[INFO] total IPv4 networks loaded: {len(ipv4_records)}")
    print(f"[INFO] total IPv6 networks loaded: {len(ipv6_records)}")

    if ipv4_records:
        build_mmdb(ipv4_records, OUTPUT_DB_IPV4, ip_version=4)
    if ipv6_records:
        build_mmdb(ipv6_records, OUTPUT_DB_IPV6, ip_version=6)


if __name__ == "__main__":
    main()