# 🕵️ AutoReconX - Lourencobrah Edition

> Reconhecimento automático de alvos para análise de superfície de ataque, focado em testes de segurança ofensiva.

AutoReconX é uma ferramenta de reconhecimento automatizado feita em Python que combina múltiplas etapas de enumeração e footprinting em um único fluxo. Seu objetivo é facilitar a vida de profissionais de segurança, bug hunters e entusiastas, acelerando a coleta de informações públicas sobre um domínio.

---

## ⚙️ Funcionalidades

- 🔍 Resolução de DNS e IP
- 🛡️ Detecção de WAFs via headers
- 📡 Análise de headers HTTP
- 🌐 Enumeração de subdomínios via [crt.sh](https://crt.sh)
- ✅ Verificação da acessibilidade de subdomínios
- 🔐 Coleta de informações de SSL/TLS (incluindo extração do certificado)
- 🧠 Fingerprint básico via hash do favicon
- 🌍 Geolocalização e dados do servidor (em progresso)
- 🔎 Port scan básico (via socket)

---

## 🚀 Como usar

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/AutoReconX.git
cd AutoReconX
```

Crie um ambiente virtual (opcional):

```
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

Instale as dependencias:

```
pip install -r requirements.txt
```

Execute a ferramenta:

```
python main.py
```

E por fim, informe o domínio no formato: exemplo.com.br (sem http:// ou https://).

---

## 📦 Dependências principais

- requests
- dnspython
- socket
- ssl
- colorama
- beaultifulsoup4
- cryptography
- idna

(Todas listadas em requirements.txt)

---

## 🧠 Autor

Desenvolvido com 💻 e ☕ por Guilherme Lourenço (a.k.a. lourencobrah)

📫 Contato: https://www.linkedin.com/in/lourencovicente/

---

## ⚠️ Aviso Legal

> Esta ferramenta foi criada para fins de pesquisa em segurança. O uso não autorizado contra sistemas que você não possui permissão pode ser considerado ilegal. Utilize com responsabilidade.
