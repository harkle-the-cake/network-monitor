import subprocess
import re
import platform
import time
import ipaddress
import netifaces
from flask import Flask, jsonify

app = Flask(__name__)
PING_CMD = "ping -c 1 -W 1" if platform.system() != "Windows" else "ping -n 1"

def get_local_networks():
    networks = []
    for iface in netifaces.interfaces():
        if iface.startswith("lo") or iface.startswith("docker") or not iface.startswith(("e", "w")):
            continue  # überspringe Loopbacks, virtuelle, etc.

        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                ip = addr.get("addr")
                netmask = addr.get("netmask")
                if ip and netmask:
                    try:
                        net = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                        networks.append(str(net))
                    except ValueError:
                        continue
    return networks

def get_hosts_from_network(cidr):
    try:
        result = subprocess.run(["nmap", "-sL", cidr], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        hosts = []
        for line in lines:
            match = re.search(r"Nmap scan report for (.+?) \(([\d.]+)\)", line)
            if match:
                name, ip = match.groups()
                hosts.append({"name": name, "ip": ip, "network": cidr})
        return hosts
    except Exception as e:
        return []

def ping_host(ip):
    try:
        start = time.time()
        result = subprocess.run(f"{PING_CMD} {ip}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        delay = round((time.time() - start) * 1000)
        return {"status": "online" if result.returncode == 0 else "offline", "delay": delay if result.returncode == 0 else None}
    except Exception:
        return {"status": "error", "delay": None}

@app.route("/hosts")
def hosts():
    all_hosts = []
    for network in get_local_networks():
        hosts = get_hosts_from_network(network)
        for host in hosts:
            ping_result = ping_host(host["ip"])
            host.update(ping_result)
        all_hosts.extend(hosts)
    return jsonify(all_hosts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
