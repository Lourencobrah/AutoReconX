import socket
from urllib.parse import urlparse
from colorama import Fore, Style

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
    print(Fore.GREEN + "\n[*] Port Scan (Basic Python Scanner)" + Style.RESET_ALL)

    parsed_url = urlparse(url)
    host = parsed_url.hostname

    if not host:
        print(Fore.RED + "[!] Host inválido." + Style.RESET_ALL)
        return

    print(f"[+] Escaneando host: {host}")
    for port, service in COMMON_PORTS.items():
        if scan_port(host, port):
            print(Fore.CYAN + f"    [OPEN] Porta {port} ({service})" + Style.RESET_ALL)
        else:
            print(Fore.LIGHTBLACK_EX + f"    [CLOSED] Porta {port} ({service})" + Style.RESET_ALL)
