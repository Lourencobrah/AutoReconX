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
        ip = socket.gethostbyname(hostname)
        return ip
    except:
        return "Desconhecido"

def get_favicon_hash(url):
    try:
        favicon_url = url.rstrip('/') + '/favicon.ico'
        res = requests.get(favicon_url, timeout=5)
        if res.status_code == 200:
            hash_value = hashlib.md5(res.content).hexdigest()
            return hash_value
    except:
        return None

def get_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string.strip() if soup.title else 'Sem título'
    return title

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

    # Servidores e tecnologias backend
    if 'apache' in server:
        data = {'String': server}
        versions = re.findall(r'apache/?([0-9.]+)?', server)
        os_match = re.findall(r'\((.*?)\)', server)
        if versions:
            data['Version'] = versions[0]
        if os_match:
            data['OS'] = os_match[0]
        add_plugin('Apache', data, 'Servidor web open-source.')
        summary.append(f"HTTPServer[{data.get('OS', 'Desconhecido')}][{server}]")

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

    # CMS detection
    if 'wp-content' in html or 'wordpress' in powered:
        add_plugin('WordPress', description='Sistema de gerenciamento de conteúdo (CMS) popular.')
    if 'joomla' in html:
        add_plugin('Joomla', description='CMS gratuito e de código aberto.')
    if 'drupal' in html:
        add_plugin('Drupal', description='CMS flexível e robusto.')

    # Frameworks JavaScript
    if any('react' in s or '__react' in html for s in scripts):
        add_plugin('React.js', description='Biblioteca JavaScript para interfaces de usuário.')
    if any('vue' in s or 'vue.js' in html for s in scripts):
        add_plugin('Vue.js', description='Framework progressivo para construção de interfaces.')
    if 'angular' in html or any('angular' in s for s in scripts):
        add_plugin('Angular', description='Framework web baseado em TypeScript.')

    # jQuery
    if any('jquery' in s for s in scripts):
        add_plugin('jQuery', {'Website': 'http://jquery.com/'}, 'JavaScript rápido para DOM e AJAX.')

    # Analytics e rastreamento
    if 'google-analytics' in html or 'gtag(' in html:
        add_plugin('Google Analytics', description='Ferramenta de análise de tráfego web do Google.')

    if 'googletagmanager.com' in html:
        add_plugin('Google Tag Manager', description='Gerenciador de tags do Google.')

    if 'facebook.net' in html or 'fbq(' in html:
        add_plugin('Facebook Pixel', description='Ferramenta de rastreamento da Meta.')

    # CDN e serviços externos
    if 'cloudflare' in server or 'cf-ray' in headers:
        add_plugin('Cloudflare', description='CDN e proteção contra DDoS.')

    if 'fonts.googleapis.com' in html:
        add_plugin('Google Fonts', description='Serviço de fontes da Google.')

    # HTML5 Doctype
    if '<!doctype html>' in html.lower():
        add_plugin('HTML5', description='HTML versão 5 detectado via doctype.')

    # X-UA-Compatible
    if 'x-ua-compatible' in headers or 'x-ua-compatible' in html:
        value = headers.get('X-UA-Compatible', 'IE=edge')
        add_plugin('X-UA-Compatible', {'String': value}, 'Compatibilidade com IE.')

    # Favicon hash (usado por Shodan e outros)
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

    # Script tag summary
    if scripts:
        add_plugin('Script', {'Scripts detectados': len(scripts)}, 'Scripts externos encontrados.')

    return summary, plugins

def run(url):
    print(Fore.GREEN + "\n[*] Web Tools Analyzer" + Style.RESET_ALL)
    try:
        res = requests.get(url, timeout=5)
        headers = res.headers
        html = res.text
        scripts = [s.get('src', '') for s in BeautifulSoup(html, 'html.parser').find_all('script') if s.get('src')]
        ip = get_ip(url)
        title = get_title(html)
        favicon_hash = get_favicon_hash(url)

        # Resumo e plugins
        summary, plugins = detect_plugins(headers, html.lower(), scripts, favicon_hash)

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
        print(Fore.RED + f"\n[!] Erro ao requisitar o site: {e}" + Style.RESET_ALL)
