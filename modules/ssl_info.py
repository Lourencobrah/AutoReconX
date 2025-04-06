import ssl
import socket
from colorama import Fore, Style

def run(url):
    print(Fore.GREEN + "\n[*] SSL/TLS Information" + Style.RESET_ALL)
    try:
        hostname = url.replace("https://", "").replace("http://", "")
        cert = ssl.get_server_certificate((hostname, 443))
        print(f"    [>] Certificado SSL encontrado para {url}")
        print(f"    [>] Detalhes do certificado: {cert}")
    except Exception as e:
        print(f"    [!] Erro ao verificar SSL: {e}")
