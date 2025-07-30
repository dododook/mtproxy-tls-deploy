import os
import random
import socket
import time
import subprocess

port_start = int(os.getenv("PORT_START", "30000"))
port_end = int(os.getenv("PORT_END", "30010"))
PORT_POOL = list(range(port_start, port_end))
USED_PORTS = set()

FAKE_TLS_DOMAIN = os.getenv("TLS_DOMAIN", "www.cloudflare.com")
SECRET = os.getenv("PROXY_SECRET", "abcdef0123456789abcdef0123456789")
MTG_PATH = "/usr/local/bin/mtg"
LISTEN_ADDR = "0.0.0.0"

def start_proxy(port):
    print(f"[+] 启动代理：端口 {port}")
    cmd = [
        MTG_PATH,
        "run",
        "--bind", f"{LISTEN_ADDR}:{port}",
        "--secret", f"tls:{FAKE_TLS_DOMAIN}:{SECRET}"
    ]
    return subprocess.Popen(cmd)

def is_port_blocked(port):
    try:
        sock = socket.create_connection(("1.1.1.1", port), timeout=1)
        sock.close()
        return False
    except:
        return True

def run_proxy_manager():
    process = None
    port = None

    while True:
        if process is None or process.poll() is not None or is_port_blocked(port):
            if process:
                print(f"[-] 端口 {port} 失效，尝试更换")
                process.kill()
                USED_PORTS.discard(port)

            available_ports = list(set(PORT_POOL) - USED_PORTS)
            if not available_ports:
                print("[!] 没有可用端口，退出")
                break

            port = random.choice(available_ports)
            USED_PORTS.add(port)
            process = start_proxy(port)
            print(f"[+] 新代理启动成功: {port}")

        time.sleep(30)

if __name__ == "__main__":
    run_proxy_manager()
