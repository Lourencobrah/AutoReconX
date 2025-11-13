import socket
import dns.resolver
from colorama import Fore, Style
import tldextract

def run(url):
    print(Fore.GREEN + "[*] Informações de DNS e IP" + Style.RESET_ALL)

    result = {
        "domain": None,
        "ip": None,
        "a_records": [],
        "error": None
    }

    try:
        domain = tldextract.extract(url).registered_domain
        result["domain"] = domain

        ip_address = socket.gethostbyname(domain)
        result["ip"] = ip_address
        print(f"    [>] Endereço IP: {ip_address}")

    except Exception as e:
        print(f"    [!] Erro ao resolver o IP: {e}")
        result["error"] = f"IP resolution error: {e}"
        return result

    try:
        ipv4_records = dns.resolver.resolve(domain, 'A')
        for record in ipv4_records:
            record_ip = str(record)
            result["a_records"].append(record_ip)
            print(f"    [>] Registro do tipo A (IPv4): {record_ip}")

    except Exception as e:
        print(f"    [!] Nenhum registro do tipo A encontrado: {e}")
        result["a_records_error"] = str(e)

    return result
