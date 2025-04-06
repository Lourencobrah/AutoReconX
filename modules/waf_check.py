import requests
from colorama import Fore, Style

def run(url):
    print(Fore.GREEN + "\n[*] WAF Detection (simples)" + Style.RESET_ALL)
    try:
        res = requests.get(url, timeout=10)  # Timeout aumentado para 10 segundos
        headers = res.headers

        waf_headers = ["x-sucuri-id", "x-sucuri-cache", "x-fireeye", "x-cdn", "server"]
        found = False

        for h in waf_headers:
            if h in headers:
                print(f"    [>] Possível WAF detectado via header: {h} → {headers[h]}")
                found = True
        if not found:
            print("    [-] Nenhum WAF visível detectado.")
    except requests.exceptions.Timeout:
        print("    [!] Tempo de resposta excedido. Tente novamente com mais tempo.")
    except requests.exceptions.RequestException as e:
        print(f"    [!] Erro na requisição: {e}")
