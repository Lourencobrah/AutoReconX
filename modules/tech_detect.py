import requests
from colorama import Fore, Style
from bs4 import BeautifulSoup
import hashlib
import re
import socket
from urllib.parse import urlparse

def get_ip(url):
    try:
        hostname = urlparse(url).hostname
        return socket.gethostbyname(hostname)
    except:
        return "Desconhecido"

def get_favicon_hash(url):
    try:
        favicon_url = url.rstrip('/') + '/favicon.ico'
        res = requests.get(favicon_url, timeout=5)
        if res.status_code == 200:
            return hashlib.md5(res.content).hexdigest()
    except:
        return None

def get_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.title.string.strip() if soup.title else 'Sem título'

def detect_plugins(headers, html, scripts, favicon_hash):
    summary = []
    plugins = []

    def add_plugin(name, data=None, description=None):
        summary.append(name)
        plugins.append({
            'name': name,
            'data': data or {},
            'description': description
        })

    server = headers.get('Server', '').lower()
    powered = headers.get('X-Powered-By', '').lower()

    # Detect frameworks e servidores
    if 'apache' in server:
        data = {'String': server}
        add_plugin('Apache', data, 'Servidor web open-source.')
    if 'nginx' in server:
        add_plugin('Nginx', {'String': server}, 'Servidor web leve e de alto desempenho.')
    if 'express' in powered or 'express' in html:
        add_plugin('Express.js', description='Framework web para Node.js.')
    if 'php' in powered or '.php' in html:
        add_plugin('PHP', description='Linguagem de script amplamente usada para web.')
    if 'laravel' in html:
        add_plugin('Laravel', description='Framework PHP moderno e elegante.')
    if 'django' in powered or 'csrftoken' in headers:
        add_plugin('Django', description='Framework web de alto nível em Python.')

    # CMS
    if 'wp-content' in html or 'wordpress' in powered:
        add_plugin('WordPress', description='CMS popular.')
    if 'joomla' in html:
        add_plugin('Joomla', description='CMS gratuito e open-source.')
    if 'drupal' in html:
        add_plugin('Drupal', description='CMS flexível e robusto.')

    # JS frameworks
    if any('react' in s or '__react' in html for s in scripts):
        add_plugin('React.js', description='Biblioteca JavaScript para UI.')
    if any('vue' in s or 'vue.js' in html for s in scripts):
        add_plugin('Vue.js', description='Framework progressivo para UI.')
    if 'angular' in html or any('angular' in s for s in scripts):
        add_plugin('Angular', description='Framework web baseado em TypeScript.')
    if any('jquery' in s for s in scripts):
        add_plugin('jQuery', {'Website': 'http://jquery.com/'}, 'JavaScript rápido para DOM e AJAX.')

    # Analytics / Tracking
    if 'google-analytics' in html or 'gtag(' in html:
        add_plugin('Google Analytics')
    if 'googletagmanager.com' in html:
        add_plugin('Google Tag Manager')
    if 'facebook.net' in html or 'fbq(' in html:
        add_plugin('Facebook Pixel')

    # CDN / Serviços externos
    if 'cloudflare' in server or 'cf-ray' in headers:
        add_plugin('Cloudflare', description='CDN e proteção DDoS.')
    if 'fonts.googleapis.com' in html:
        add_plugin('Google Fonts')

    # HTML5
    if '<!doctype html>' in html.lower():
        add_plugin('HTML5', description='HTML versão 5 detectado via doctype.')

    # Favicon
    favicon_db = {
        'd41d8cd98f00b204e9800998ecf8427e': 'Possível favicon vazio',
        '3e1c3f44ffb34a2f3af22cbd0a4f395e': 'Painel phpMyAdmin',
        'b14f9769b212d233cf39e93429fc1c29': 'Joomla CMS',
        '9e107d9d372bb6826bd81d3542a419d6': 'Painel genérico',
    }
    if favicon_hash and favicon_hash in favicon_db:
        add_plugin('Favicon Fingerprint', {'Hash': favicon_hash}, favicon_db[favicon_hash])
    elif favicon_hash:
        add_plugin('Favicon Hash', {'Hash': favicon_hash}, 'Hash MD5 do favicon extraído.')

    # Scripts count
    if scripts:
        add_plugin('Script', {'Scripts detectados': len(scripts)}, 'Scripts externos encontrados.')

    return summary, plugins

def run(url):
    print(Fore.GREEN + "\n[*] Web Tools Analyzer" + Style.RESET_ALL)
    result = {
        "ip": None,
        "title": None,
        "summary": [],
        "plugins": [],
        "error": None
    }

    try:
        res = requests.get(url, timeout=5)
        headers = res.headers
        html = res.text
        scripts = [s.get('src', '') for s in BeautifulSoup(html, 'html.parser').find_all('script') if s.get('src')]
        ip = get_ip(url)
        title = get_title(html)
        favicon_hash = get_favicon_hash(url)

        summary, plugins = detect_plugins(headers, html.lower(), scripts, favicon_hash)

        result.update({
            "ip": ip,
            "title": title,
            "summary": summary,
            "plugins": plugins
        })

        # Prints mantidos
        print(Fore.YELLOW + f"    Status    : {res.status_code} {res.reason}")
        print(f"    Title     : {title}")
        print(f"    IP        : {ip}")
        print(f"    Country   : DESCONHECIDO, ZZ" + Style.RESET_ALL)

        print(Fore.CYAN + "\n    Summary   : " + ', '.join(summary) + Style.RESET_ALL)

        print(Fore.MAGENTA + "\n    Detected Plugins:" + Style.RESET_ALL)
        for plugin in plugins:
            print(f"     [ {plugin['name']} ]")
            if plugin['description']:
                print(f"      {plugin['description']}")
            for key, val in plugin['data'].items():
                print(f"      {key:<12}: {val}")
            print()

        print(Fore.BLUE + "    HTTP Headers:" + Style.RESET_ALL)
        for k, v in headers.items():
            print(f"      {k}: {v}")

    except requests.exceptions.RequestException as e:
        msg = f"Erro ao requisitar o site: {e}"
        print(Fore.RED + f"\n[!] {msg}" + Style.RESET_ALL)
        result["error"] = msg

    return result
