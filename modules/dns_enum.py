import socket
import dns.resolver
from colorama import Fore, Style
import tldextract

def run(url):
    print(Fore.GREEN + "[*] Informações de DNS e IP" + Style.RESET_ALL)

    try:
        # Extrai o domínio principal da URL (sem subdomínios)
        domain = tldextract.extract(url).registered_domain

        # Resolve o IP associado ao domínio
        ip_address = socket.gethostbyname(domain)
        print(f"    [>] Endereço IP: {ip_address}")
    except Exception as e:
        print(f"    [!] Erro ao resolver o IP: {e}")
        return

    try:
        # Tenta resolver registros do tipo A (IPv4)
        ipv4_records = dns.resolver.resolve(domain, 'A')
        for record in ipv4_records:
            print(f"    [>] Registro do tipo A (IPv4): {record}")
    except Exception as e:
        print(f"    [!] Nenhum registro do tipo A encontrado: {e}")
