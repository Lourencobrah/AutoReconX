import socket
from urllib.parse import urlparse

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt"
}

def scan_port(host, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0
    except Exception:
        return False

def run(url):
    parsed = urlparse(url)
    host = parsed.hostname

    if not host:
        return {
            "error": "Host inválido.",
            "open_ports": [],
            "closed_ports": [],
            "all_ports": []
        }

    results = []
    open_list = []
    closed_list = []

    for port, service in COMMON_PORTS.items():
        is_open = scan_port(host, port)
        entry = {
            "port": port,
            "service": service,
            "status": "open" if is_open else "closed"
        }

        results.append(entry)

        if is_open:
            open_list.append(entry)
        else:
            closed_list.append(entry)

    return {
        "host": host,
        "open_ports": open_list,
        "closed_ports": closed_list,
        "all_ports": results,
        "error": None
    }
