from modules import dns_enum, http_enum, waf_check, tech_detect, subdomain_enum, ssl_info, nmap_detect 
from colorama import Fore, Style
from urllib.parse import urlparse

def main():
    try:
        print(Fore.CYAN + "\n[ AutoReconX - Lourencobrah Edition ]\n" + Style.RESET_ALL)
        url = input("Informe a URL (ex: exemplo.com): ").strip()

        # Detecta automaticamente se é http ou https
        if not url.startswith("http"):
            url = "https://" + url  # Prioriza https por segurança

        parsed_url = urlparse(url)
        use_https = parsed_url.scheme == "https"
        domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path

        print(Fore.YELLOW + f"\n[+] Iniciando enumeração para: {url}\n" + Style.RESET_ALL)
        
        dns_enum.run(url)
        waf_check.run(url)
        http_enum.run(url)
        subdomain_enum.run(url, use_https=use_https)  # <- Sem api_key aqui!
        tech_detect.run(url)
        ssl_info.run(url)
        nmap_detect.run(url)

    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Execução interrompida pelo usuário!" + Style.RESET_ALL)
        print("[*] Finalizando...")
        exit()

if __name__ == "__main__":
    main()
