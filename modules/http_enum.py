import requests
from colorama import Fore, Style

def run(url):
    print(Fore.GREEN + "\n[*] HTTP Headers & Status" + Style.RESET_ALL)

    result = {
        "status_code": None,
        "headers": {},
        "error": None
    }

    try:
        res = requests.get(url, timeout=10)
        result["status_code"] = res.status_code
        result["headers"] = dict(res.headers)

        print(f"    [>] Status: {res.status_code}")
        print("    [>] Headers:")
        for k, v in res.headers.items():
            print(f"       - {k}: {v}")

    except requests.exceptions.Timeout:
        msg = "Timeout: servidor ultrapassou limite de 10s."
        print(f"    [!] {msg}")
        result["error"] = msg

    except requests.exceptions.RequestException as e:
        print(f"    [!] Erro na requisição: {e}")
        result["error"] = str(e)

    return result
