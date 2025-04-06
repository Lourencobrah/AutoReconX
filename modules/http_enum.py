import requests
from colorama import Fore, Style

def run(url):
    print(Fore.GREEN + "\n[*] HTTP Headers & Status" + Style.RESET_ALL)
    try:
        res = requests.get(url, timeout=10)  # Timeout aumentado para 10 segundos
        print(f"    [>] Status: {res.status_code}")
        print("    [>] Headers:")
        for k, v in res.headers.items():
            print(f"       - {k}: {v}")
    except requests.exceptions.Timeout:
        print("    [!] Tempo de resposta excedido. Tente novamente com mais tempo.")
    except requests.exceptions.RequestException as e:
        print(f"    [!] Erro na requisição: {e}")
