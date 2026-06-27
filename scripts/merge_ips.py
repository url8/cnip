import ipaddress
import requests

V4_SOURCES = [
    "https://raw.githubusercontent.com/gaoyifan/china-operator-ip/refs/heads/ip-lists/china.txt",
    "https://raw.githubusercontent.com/mayaxcn/china-ip-list/master/chnroute.txt",
    "https://raw.githubusercontent.com/ChanthMiao/China-IPv4-List/release/cn.txt",
    "https://raw.githubusercontent.com/wendellouyang/geolite2_china_ip_list/refs/heads/main/chnip.txt",
    "https://raw.githubusercontent.com/1715173329/IPCIDR-CHINA/refs/heads/master/ipv4.txt",
    "https://cira.moedove.com/geo/country/ipv4/CN.txt",
]

V6_SOURCES = [
    "https://raw.githubusercontent.com/gaoyifan/china-operator-ip/refs/heads/ip-lists/china6.txt",
    "https://raw.githubusercontent.com/mayaxcn/china-ip-list/master/chnroute_v6.txt",
    "https://raw.githubusercontent.com/ChanthMiao/China-IPv6-List/release/cn6.txt",
    "https://raw.githubusercontent.com/1715173329/IPCIDR-CHINA/refs/heads/master/ipv6.txt",
    "https://cira.moedove.com/geo/country/ipv6/CN.txt",
]


def fetch_sources(urls):
    data = set()
    for url in urls:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        for line in r.text.splitlines():
            line = line.strip()
            if line:
                data.add(line)
    return data


def merge_cidrs(cidrs, version=4):
    nets = []
    for c in cidrs:
        try:
            net = ipaddress.ip_network(c, strict=False)
            if (version == 4 and isinstance(net, ipaddress.IPv4Network)) or \
               (version == 6 and isinstance(net, ipaddress.IPv6Network)):
                nets.append(net)
        except:
            pass

    # collapse_addresses 自动合并相邻/可聚合网段
    merged = list(ipaddress.collapse_addresses(nets))
    return sorted(merged, key=lambda x: int(x.network_address))


def write_file(path, nets):
    with open(path, "w") as f:
        for n in nets:
            f.write(str(n) + "\n")


def main():
    # IPv4
    v4_raw = fetch_sources(V4_SOURCES)
    v4_merged = merge_cidrs(v4_raw, version=4)
    write_file("data/ipv4_merged.txt", v4_merged)

    # IPv6
    v6_raw = fetch_sources(V6_SOURCES)
    v6_merged = merge_cidrs(v6_raw, version=6)
    write_file("data/ipv6_merged.txt", v6_merged)
  
if __name__ == "__main__":
    main()
