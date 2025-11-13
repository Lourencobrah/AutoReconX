import requests
from colorama import Fore, Style

def run(url):
    print(Fore.GREEN + "\n[*] WAF Detection (simples)" + Style.RESET_ALL)

    result = {
        "detected": False,
        "headers_found": {},
        "error": None
    }

    try:
        res = requests.get(url, timeout=10)
        headers = res.headers

        waf_headers = [
            "x-sucuri-id", "x-sucuri-cache",
            "x-fireeye", "x-cdn", "server"
        ]

        for h in waf_headers:
            if h in headers:
                value = headers[h]
                print(f"    [>] Possível WAF detectado via header: {h} → {value}")

                result["detected"] = True
                result["headers_found"][h] = value

        if not result["detected"]:
            print("    [-] Nenhum WAF visível detectado.")

    except requests.exceptions.Timeout:
        msg = "Timeout: servidor ultrapassou limite de 10s."
        print(f"    [!] {msg}")
        result["error"] = msg

    except requests.exceptions.RequestException as e:
        print(f"    [!] Erro na requisição: {e}")
        result["error"] = str(e)

    return result
