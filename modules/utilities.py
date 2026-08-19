# ==========================================
# CONKS CYBER
# modules/utilities.py
# ==========================================

import os
import platform
import socket
import shutil
import subprocess
import sys
from datetime import datetime


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


# ==========================================
# LIMPAR TELA
# ==========================================

def limpar_tela():
    os.system("clear")


# ==========================================
# MENSAGENS
# ==========================================

def sucesso(texto):
    print(f"{GREEN}[+] {texto}{RESET}")


def erro(texto):
    print(f"{RED}[-] {texto}{RESET}")


def info(texto):
    print(f"{BLUE}[i] {texto}{RESET}")


def aviso(texto):
    print(f"{YELLOW}[!] {texto}{RESET}")


# ==========================================
# INFORMAÇÕES DO SISTEMA
# ==========================================

def informacoes_sistema():

    limpar_tela()

    print(
        f"{BLUE}{BOLD}"
        "╔══════════════════════════════════════╗"
        f"{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "║          INFORMAÇÕES DO SISTEMA     ║"
        f"{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "╠══════════════════════════════════════╣"
        f"{RESET}"
    )

    sistema = platform.system()
    versao = platform.release()
    arquitetura = platform.machine()
    python = platform.python_version()
    hostname = socket.gethostname()

    dados = [
        ("Sistema", sistema),
        ("Versão", versao),
        ("Arquitetura", arquitetura),
        ("Python", python),
        ("Hostname", hostname)
    ]

    for nome, valor in dados:

        print(
            f"{WHITE}║ {nome:<15}: "
            f"{str(valor)[:20]:<20} ║{RESET}"
        )

    print(
        f"{BLUE}{BOLD}"
        "╚══════════════════════════════════════╝"
        f"{RESET}"
    )


# ==========================================
# USO DE ARMAZENAMENTO
# ==========================================

def uso_armazenamento():

    limpar_tela()

    print(
        f"{BLUE}{BOLD}"
        "╔══════════════════════════════════════╗"
        f"{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "║          ARMAZENAMENTO               ║"
        f"{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "╠══════════════════════════════════════╣"
        f"{RESET}"
    )

    try:

        total, usado, livre = shutil.disk_usage("/")

        gb = 1024 ** 3

        total_gb = total / gb
        usado_gb = usado / gb
        livre_gb = livre / gb

        print(
            f"{WHITE}║ Total: "
            f"{total_gb:.2f} GB"
            f"{'':>18}║{RESET}"
        )

        print(
            f"{WHITE}║ Usado: "
            f"{usado_gb:.2f} GB"
            f"{'':>18}║{RESET}"
        )

        print(
            f"{WHITE}║ Livre: "
            f"{livre_gb:.2f} GB"
            f"{'':>18}║{RESET}"
        )

    except OSError:

        erro(
            "Não foi possível consultar o armazenamento."
        )

    print(
        f"{BLUE}{BOLD}"
        "╚══════════════════════════════════════╝"
        f"{RESET}"
    )


# ==========================================
# DATA E HORA
# ==========================================

def data_hora():

    limpar_tela()

    agora = datetime.now()

    print(
        f"{BLUE}{BOLD}"
        "╔══════════════════════════════════════╗"
        f"{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "║             DATA E HORA              ║"
        f"{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "╠══════════════════════════════════════╣"
        f"{RESET}"
    )

    print(
        f"{WHITE}║ Data: "
        f"{agora.strftime('%d/%m/%Y'):<28}║{RESET}"
    )

    print(
        f"{WHITE}║ Hora: "
        f"{agora.strftime('%H:%M:%S'):<28}║{RESET}"
    )

    print(
        f"{WHITE}║ Dia: "
        f"{agora.strftime('%A'):<29}║{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "╚══════════════════════════════════════╝"
        f"{RESET}"
    )


# ==========================================
# TESTE DE PING
# ==========================================

def testar_ping():

    limpar_tela()

    host = input(
        "\nDigite o domínio ou IP: "
    ).strip()

    if not host:

        erro("Digite um endereço.")

        return

    print(
        f"\n{BLUE}[~] Testando conexão...{RESET}"
    )

    sistema = platform.system().lower()

    if sistema == "windows":

        comando = [
            "ping",
            "-n",
            "1",
            host
        ]

    else:

        comando = [
            "ping",
            "-c",
            "1",
            host
        ]

    try:

        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=10
        )

        if resultado.returncode == 0:

            sucesso(
                f"{host} respondeu ao ping."
            )

        else:

            erro(
                f"{host} não respondeu ao ping."
            )

    except FileNotFoundError:

        erro(
            "O comando ping não está disponível."
        )

    except subprocess.TimeoutExpired:

        erro(
            "Tempo limite excedido."
        )

    except OSError as exc:

        erro(
            f"Erro ao executar ping: {exc}"
        )


# ==========================================
# RESOLVER DNS
# ==========================================

def resolver_dns():

    limpar_tela()

    dominio = input(
        "\nDigite o domínio: "
    ).strip()

    if not dominio:

        erro("Digite um domínio.")

        return

    try:

        infos = socket.getaddrinfo(
            dominio,
            None
        )

        ips = []

        for info_item in infos:

            endereco = info_item[4][0]

            if endereco not in ips:

                ips.append(endereco)

        print(
            f"\n{BLUE}{BOLD}"
            "╔══════════════════════════════════════╗"
            f"{RESET}"
        )

        print(
            f"{BLUE}{BOLD}"
            "║              DNS LOOKUP              ║"
            f"{RESET}"
        )

        print(
            f"{BLUE}{BOLD}"
            "╠══════════════════════════════════════╣"
            f"{RESET}"
        )

        print(
            f"{WHITE}║ Domínio: "
            f"{dominio:<26}║{RESET}"
        )

        for ip in ips:

            print(
                f"{GREEN}║ IP: "
                f"{ip:<31}║{RESET}"
            )

        print(
            f"{BLUE}{BOLD}"
            "╚══════════════════════════════════════╝"
            f"{RESET}"
        )

    except socket.gaierror:

        erro(
            "Não foi possível resolver o domínio."
        )


# ==========================================
# VERIFICAR PORTA
# ==========================================

def verificar_porta():

    limpar_tela()

    host = input(
        "\nHost/IP: "
    ).strip()

    if not host:

        erro("Digite um host.")

        return

    porta_texto = input(
        "Porta: "
    ).strip()

    try:

        porta = int(porta_texto)

        if porta < 1 or porta > 65535:

            raise ValueError

    except ValueError:

        erro(
            "A porta deve estar entre 1 e 65535."
        )

        return

    print(
        f"\n{BLUE}[~] Verificando porta {porta}...{RESET}"
    )

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as sock:

            sock.settimeout(3)

            resultado = sock.connect_ex(
                (host, porta)
            )

        if resultado == 0:

            sucesso(
                f"Porta {porta} acessível em {host}."
            )

        else:

            aviso(
                f"Porta {porta} não está acessível."
            )

    except socket.gaierror:

        erro(
            "Host inválido ou não resolvido."
        )

    except OSError as exc:

        erro(
            f"Erro de conexão: {exc}"
        )


# ==========================================
# CALCULADORA
# ==========================================

def calculadora():

    limpar_tela()

    print(
        f"{BLUE}{BOLD}"
        "╔══════════════════════════════════════╗"
        f"{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "║             CALCULADORA              ║"
        f"{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "╠══════════════════════════════════════╣"
        f"{RESET}"
    )

    print(
        f"{WHITE}║ Digite uma expressão simples.        ║{RESET}"
    )

    print(
        f"{WHITE}║ Exemplos: 10 + 5 / 20 * 3            ║{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "╚══════════════════════════════════════╝"
        f"{RESET}"
    )

    expressao = input(
        "\nExpressão: "
    ).strip()

    if not expressao:

        erro("Nenhuma expressão informada.")

        return

    permitidos = set(
        "0123456789+-*/().% "
    )

    if any(
        caractere not in permitidos
        for caractere in expressao
    ):

        erro(
            "Expressão contém caracteres não permitidos."
        )

        return

    try:

        resultado = eval(
            expressao,
            {
                "__builtins__": {}
            },
            {}
        )

        print(
            f"\n{GREEN}{BOLD}"
            f"Resultado: {resultado}"
            f"{RESET}"
        )

    except Exception:

        erro(
            "Não foi possível calcular a expressão."
        )


# ==========================================
# VERIFICAR ARQUIVO/DIRETÓRIO
# ==========================================

def verificar_caminho():

    limpar_tela()

    caminho = input(
        "\nDigite o caminho: "
    ).strip()

    if not caminho:

        erro("Digite um caminho.")

        return

    caminho = os.path.expanduser(
        caminho
    )

    if os.path.isfile(caminho):

        try:

            tamanho = os.path.getsize(
                caminho
            )

            print(
                f"\n{GREEN}[+] Arquivo encontrado.{RESET}"
            )

            print(
                f"{WHITE}Caminho: {caminho}{RESET}"
            )

            print(
                f"{WHITE}Tamanho: {tamanho} bytes{RESET}"
            )

        except OSError:

            erro(
                "Não foi possível obter informações do arquivo."
            )

    elif os.path.isdir(caminho):

        try:

            quantidade = len(
                os.listdir(caminho)
            )

            print(
                f"\n{GREEN}[+] Diretório encontrado.{RESET}"
            )

            print(
                f"{WHITE}Caminho: {caminho}{RESET}"
            )

            print(
                f"{WHITE}Itens: {quantidade}{RESET}"
            )

        except OSError:

            erro(
                "Não foi possível ler o diretório."
            )

    else:

        aviso(
            "Arquivo ou diretório não encontrado."
        )


# ==========================================
# MENU UTILIDADES
# ==========================================

def menu_utilidades():

    while True:

        limpar_tela()

        print(
            f"{BLUE}{BOLD}"
            "╔══════════════════════════════════════╗"
            f"{RESET}"
        )

        print(
            f"{BLUE}{BOLD}"
            "║             UTILIDADES              ║"
            f"{RESET}"
        )

        print(
            f"{BLUE}{BOLD}"
            "╠══════════════════════════════════════╣"
            f"{RESET}"
        )

        print(
            f"{WHITE}║ [1] Informações do sistema           ║{RESET}"
        )

        print(
            f"{WHITE}║ [2] Uso de armazenamento             ║{RESET}"
        )

        print(
            f"{WHITE}║ [3] Data e hora                      ║{RESET}"
        )

        print(
            f"{WHITE}║ [4] Testar ping                      ║{RESET}"
        )

        print(
            f"{WHITE}║ [5] Resolver DNS                     ║{RESET}"
        )

        print(
            f"{WHITE}║ [6] Verificar porta                  ║{RESET}"
        )

        print(
            f"{WHITE}║ [7] Calculadora                      ║{RESET}"
        )

        print(
            f"{WHITE}║ [8] Verificar arquivo/diretório      ║{RESET}"
        )

        print(
            f"{RED}║ [0] Voltar                           ║{RESET}"
        )

        print(
            f"{BLUE}{BOLD}"
            "╚══════════════════════════════════════╝"
            f"{RESET}"
        )

        opcao = input(
            f"\n{BLUE}{BOLD}"
            "CONKS@Utilidades > "
            f"{RESET}"
        ).strip()

        if opcao == "1":

            informacoes_sistema()

        elif opcao == "2":

            uso_armazenamento()

        elif opcao == "3":

            data_hora()

        elif opcao == "4":

            testar_ping()

        elif opcao == "5":

            resolver_dns()

        elif opcao == "6":

            verificar_porta()

        elif opcao == "7":

            calculadora()

        elif opcao == "8":

            verificar_caminho()

        elif opcao == "0":

            break

        else:

            erro("Opção inválida.")

        if opcao != "0":

            input(
                f"\n{GRAY}"
                "Pressione ENTER para continuar..."
                f"{RESET}"
            )