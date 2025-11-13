import requests
import tldextract
from colorama import Fore, Style

def get_subdomains_crtsh(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    subdomains = set()
    error = None

    try:
        response = requests.get(url, timeout=10)
        if not response.ok:
            error = f"Falha ao consultar subdomínios no crt.sh (status {response.status_code})"
            print(Fore.RED + f"    [!] {error}" + Style.RESET_ALL)
            return list(subdomains), error

        data = response.json()
        for entry in data:
            name = entry.get("name_value", "")
            if domain in name:
                for sub in name.split("\n"):
                    if "*" not in sub:
                        subdomains.add(sub.strip())

    except requests.exceptions.RequestException as e:
        error = f"Erro ao buscar subdomínios: {e}"
        print(Fore.RED + f"    [!] {error}" + Style.RESET_ALL)

    return sorted(subdomains), error

def check_subdomain_reachability(subdomains, use_https=True):
    protocol = "https" if use_https else "http"
    reachable = {}

    for sub in subdomains:
        url = f"{protocol}://{sub}"
        try:
            response = requests.get(url, timeout=5)
            reachable[sub] = response.status_code
            if response.status_code == 200:
                print(Fore.GREEN + f"    [+] Subdomínio ativo: {url} (Status: {response.status_code})" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + f"    [-] {url} respondeu com status {response.status_code}" + Style.RESET_ALL)
        except requests.exceptions.RequestException:
            reachable[sub] = None
            print(Fore.RED + f"    [x] {url} não acessível." + Style.RESET_ALL)

    return reachable

def run(url, use_https=True):
    print(Fore.CYAN + "\n[*] Subdomain Enumeration via crt.sh" + Style.RESET_ALL)

    extracted = tldextract.extract(url)
    domain = extracted.registered_domain
    result = {
        "domain": domain,
        "subdomains": [],
        "reachable": {},
        "error": None
    }

    if not domain:
        msg = "URL inválida."
        print(Fore.RED + f"    [!] {msg}" + Style.RESET_ALL)
        result["error"] = msg
        return result

    print(f"    [>] Domínio base: {domain}")
    subdomains, error = get_subdomains_crtsh(domain)
    result["subdomains"] = subdomains
    if error:
        result["error"] = error

    if not subdomains:
        print("    [!] Nenhum subdomínio encontrado.")
        return result

    print(Fore.GREEN + f"\n    [+] {len(subdomains)} subdomínios encontrados:" + Style.RESET_ALL)
    for sub in subdomains:
        print(f"        - {sub}")

    print(Fore.CYAN + "\n[*] Verificando acessibilidade dos subdomínios..." + Style.RESET_ALL)
    reachable = check_subdomain_reachability(subdomains, use_https=use_https)
    result["reachable"] = reachable

    return result
