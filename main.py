import json
from modules import dns_enum, http_enum, waf_check, tech_detect, subdomain_enum, ssl_info, nmap_detect
from colorama import Fore, Style
from urllib.parse import urlparse

MODULES = {
    "dns": dns_enum,
    "waf": waf_check,
    "http": http_enum,
    "subdomains": subdomain_enum,
    "technologies": tech_detect,
    "ssl": ssl_info,
    "ports": nmap_detect,
}

def main():
    print(Fore.CYAN + "\n[ AutoReconX ]\n" + Style.RESET_ALL)
    
    url = input("Informe a URL (ex: exemplo.com): ").strip()
    if not url.startswith("http"):
        url = "https://" + url

    parsed = urlparse(url)
    use_https = parsed.scheme == "https"
    domain = parsed.netloc or parsed.path

    print(Fore.YELLOW + f"\n[+] Iniciando enumeração para: {url}\n" + Style.RESET_ALL)

    result = {
        "target": url,
        "domain": domain,
        "https": use_https
    }

    for key, module in MODULES.items():
        try:
            if key == "subdomains":
                result[key] = module.run(url, use_https=use_https) or []
            else:
                result[key] = module.run(url) or {}
        except Exception as e:
            result[key] = {"error": str(e)}

    print(Fore.GREEN + "\n[+] Resultado Final (JSON):\n" + Style.RESET_ALL)
    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
