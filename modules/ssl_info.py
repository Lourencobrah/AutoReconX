import ssl
import socket
from colorama import Fore, Style

def run(url):
    print(Fore.GREEN + "\n[*] SSL/TLS Information" + Style.RESET_ALL)

    result = {
        "certificate": None,
        "issuer": None,
        "subject": None,
        "valid_from": None,
        "valid_to": None,
        "error": None
    }

    try:
        hostname = url.replace("https://", "").replace("http://", "").split("/")[0]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                result.update({
                    "certificate": cert,
                    "issuer": dict(x[0] for x in cert.get("issuer", [])),
                    "subject": dict(x[0] for x in cert.get("subject", [])),
                    "valid_from": cert.get("notBefore"),
                    "valid_to": cert.get("notAfter")
                })
                print(f"    [>] Certificado SSL encontrado para {url}")
                print(f"    [>] Validade: {result['valid_from']} → {result['valid_to']}")
                print(f"    [>] Issuer: {result['issuer']}")
                print(f"    [>] Subject: {result['subject']}")

    except Exception as e:
        msg = f"Erro ao verificar SSL: {e}"
        print(Fore.RED + f"    [!] {msg}" + Style.RESET_ALL)
        result["error"] = msg

    return result
