import requests
import tldextract
from colorama import Fore, Style

def get_subdomains_crtsh(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    try:
        response = requests.get(url, timeout=10)
        if not response.ok:
            print(Fore.RED + "    [!] Falha ao consultar subdomínios no crt.sh" + Style.RESET_ALL)
            return []

        data = response.json()
        subdomains = set()

        for entry in data:
            name = entry.get("name_value", "")
            if domain in name:
                for sub in name.split("\n"):
                    if "*" not in sub:
                        subdomains.add(sub.strip())

        return sorted(subdomains)

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"    [!] Erro ao buscar subdomínios: {e}" + Style.RESET_ALL)
        return []

def check_subdomain_reachability(subdomains, use_https=True):
    protocol = "https" if use_https else "http"

    for sub in subdomains:
        url = f"{protocol}://{sub}"
        try:
            response = requests.get(url, timeout=5)
            status = response.status_code
            if status == 200:
                print(Fore.GREEN + f"    [+] Subdomínio ativo: {url} (Status: {status})" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + f"    [-] {url} respondeu com status {status}" + Style.RESET_ALL)
        except requests.exceptions.RequestException:
            print(Fore.RED + f"    [x] {url} não acessível." + Style.RESET_ALL)

def run(url, use_https=True):
    print(Fore.CYAN + "\n[*] Subdomain Enumeration via crt.sh" + Style.RESET_ALL)

    extracted = tldextract.extract(url)
    domain = extracted.registered_domain

    if not domain:
        print(Fore.RED + "    [!] URL inválida." + Style.RESET_ALL)
        return

    print(f"    [>] Domínio base: {domain}")
    subdomains = get_subdomains_crtsh(domain)

    if not subdomains:
        print("    [!] Nenhum subdomínio encontrado.")
        return

    print(Fore.GREEN + f"\n    [+] {len(subdomains)} subdomínios encontrados:" + Style.RESET_ALL)
    for sub in subdomains:
        print(f"        - {sub}")

    print(Fore.CYAN + "\n[*] Verificando acessibilidade dos subdomínios..." + Style.RESET_ALL)
    check_subdomain_reachability(subdomains, use_https=use_https)
