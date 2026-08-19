# ==========================================
# CONKS CYBER
# modules/utilities.py
# ==========================================

import os
import platform
import socket
import shutil
import subprocess
import uuid
import secrets
import string
import math
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


def aviso(texto):
    print(f"{YELLOW}[!] {texto}{RESET}")


def info(texto):
    print(f"{BLUE}[i] {texto}{RESET}")


# ==========================================
# PAUSA
# ==========================================

def pausar():
    input(
        f"\n{GRAY}"
        "Pressione ENTER para continuar..."
        f"{RESET}"
    )


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
        "║        INFORMAÇÕES DO SISTEMA        ║"
        f"{RESET}"
    )
    print(
        f"{BLUE}{BOLD}"
        "╠══════════════════════════════════════╣"
        f"{RESET}"
    )

    dados = [
        ("Sistema", platform.system()),
        ("Versão", platform.release()),
        ("Arquitetura", platform.machine()),
        ("Python", platform.python_version()),
        ("Hostname", socket.gethostname())
    ]

    for nome, valor in dados:
        valor = str(valor)[:20]

        print(
            f"{WHITE}║ {nome:<15}: {valor:<20} ║{RESET}"
        )

    print(
        f"{BLUE}{BOLD}"
        "╚══════════════════════════════════════╝"
        f"{RESET}"
    )


# ==========================================
# ARMAZENAMENTO
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
        "║           ARMAZENAMENTO              ║"
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

        print(
            f"{WHITE}║ Total:    {total / gb:>8.2f} GB             ║{RESET}"
        )

        print(
            f"{WHITE}║ Usado:    {usado / gb:>8.2f} GB             ║{RESET}"
        )

        print(
            f"{WHITE}║ Livre:    {livre / gb:>8.2f} GB             ║{RESET}"
        )

        porcentagem = (
            usado / total * 100
            if total
            else 0
        )

        print(
            f"{WHITE}║ Uso:      {porcentagem:>8.2f}%              ║{RESET}"
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
        "║              DATA E HORA             ║"
        f"{RESET}"
    )
    print(
        f"{BLUE}{BOLD}"
        "╠══════════════════════════════════════╣"
        f"{RESET}"
    )

    print(
        f"{WHITE}║ Data: {agora.strftime('%d/%m/%Y'):<28} ║{RESET}"
    )

    print(
        f"{WHITE}║ Hora: {agora.strftime('%H:%M:%S'):<28} ║{RESET}"
    )

    print(
        f"{WHITE}║ Timestamp: {int(agora.timestamp()):<21} ║{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "╚══════════════════════════════════════╝"
        f"{RESET}"
    )


# ==========================================
# CALCULADORA
# ==========================================

def calculadora():

    while True:

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
            f"{WHITE}║ Exemplos:                            ║{RESET}"
        )
        print(
            f"{WHITE}║ 10 + 5                               ║{RESET}"
        )
        print(
            f"{WHITE}║ 20 * 3                               ║{RESET}"
        )
        print(
            f"{WHITE}║ (10 + 5) / 3                         ║{RESET}"
        )
        print(
            f"{WHITE}║ 2 ** 8                               ║{RESET}"
        )
        print(
            f"{WHITE}║ digite 0 para voltar                 ║{RESET}"
        )

        print(
            f"{BLUE}{BOLD}"
            "╚══════════════════════════════════════╝"
            f"{RESET}"
        )

        expressao = input(
            f"\n{BLUE}{BOLD}"
            "CONKS@Calculadora > "
            f"{RESET}"
        ).strip()

        if expressao == "0":
            return

        if not expressao:
            erro("Digite uma expressão.")
            pausar()
            continue

        permitidos = set(
            "0123456789+-*/().% "
        )

        if any(
            caractere not in permitidos
            for caractere in expressao
        ):

            erro(
                "A expressão contém caracteres não permitidos."
            )

            pausar()
            continue

        try:

            resultado = eval(
                expressao,
                {
                    "__builtins__": {}
                },
                {}
            )

            if isinstance(resultado, float):

                resultado = round(
                    resultado,
                    10
                )

            print(
                f"\n{GREEN}{BOLD}"
                f"[+] Resultado: {resultado}"
                f"{RESET}"
            )

        except ZeroDivisionError:

            erro(
                "Não é possível dividir por zero."
            )

        except Exception:

            erro(
                "Expressão inválida."
            )

        pausar()


# ==========================================
# GERADOR DE SENHA
# ==========================================

def gerar_senha():

    limpar_tela()

    print(
        f"{BLUE}{BOLD}"
        "╔══════════════════════════════════════╗"
        f"{RESET}"
    )
    print(
        f"{BLUE}{BOLD}"
        "║           GERADOR DE SENHA           ║"
        f"{RESET}"
    )
    print(
        f"{BLUE}{BOLD}"
        "╠══════════════════════════════════════╣"
        f"{RESET}"
    )

    entrada = input(
        "\nTamanho da senha [padrão 16]: "
    ).strip()

    if not entrada:
        tamanho = 16
    else:

        try:
            tamanho = int(entrada)
        except ValueError:
            erro("Digite um número válido.")
            return

    if tamanho < 4 or tamanho > 128:

        erro(
            "O tamanho deve estar entre 4 e 128."
        )

        return

    caracteres = (
        string.ascii_letters +
        string.digits +
        "!@#$%&*+-_"
    )

    senha = "".join(
        secrets.choice(caracteres)
        for _ in range(tamanho)
    )

    print(
        f"\n{GREEN}{BOLD}"
        f"Senha: {senha}"
        f"{RESET}"
    )


# ==========================================
# UUID
# ==========================================

def gerar_uuid():

    limpar_tela()

    identificador = uuid.uuid4()

    print(
        f"{BLUE}{BOLD}"
        "╔══════════════════════════════════════╗"
        f"{RESET}"
    )
    print(
        f"{BLUE}{BOLD}"
        "║              GERAR UUID              ║"
        f"{RESET}"
    )
    print(
        f"{BLUE}{BOLD}"
        "╠══════════════════════════════════════╣"
        f"{RESET}"
    )

    print(
        f"{GREEN}UUID: {identificador}{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "╚══════════════════════════════════════╝"
        f"{RESET}"
    )


# ==========================================
# CONVERSOR DE UNIDADES
# ==========================================

def conversor_unidades():

    while True:

        limpar_tela()

        print(
            f"{BLUE}{BOLD}"
            "╔══════════════════════════════════════╗"
            f"{RESET}"
        )
        print(
            f"{BLUE}{BOLD}"
            "║          CONVERSOR DE UNIDADES       ║"
            f"{RESET}"
        )
        print(
            f"{BLUE}{BOLD}"
            "╠══════════════════════════════════════╣"
            f"{RESET}"
        )

        print(
            f"{WHITE}║ [1] Metros → Quilômetros             ║{RESET}"
        )
        print(
            f"{WHITE}║ [2] Quilômetros → Metros             ║{RESET}"
        )
        print(
            f"{WHITE}║ [3] Bytes → KB/MB/GB                 ║{RESET}"
        )
        print(
            f"{WHITE}║ [4] Celsius → Fahrenheit             ║{RESET}"
        )
        print(
            f"{WHITE}║ [5] Fahrenheit → Celsius              ║{RESET}"
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
            "\nCONKS@Conversor > "
        ).strip()

        if opcao == "0":
            return

        try:

            valor = float(
                input("Valor: ").strip()
            )

        except ValueError:

            erro("Valor inválido.")
            pausar()
            continue

        if opcao == "1":

            print(
                f"{GREEN}{valor / 1000:g} km{RESET}"
            )

        elif opcao == "2":

            print(
                f"{GREEN}{valor * 1000:g} m{RESET}"
            )

        elif opcao == "3":

            print(
                f"{GREEN}"
                f"{valor / 1024:.2f} KB | "
                f"{valor / 1024**2:.2f} MB | "
                f"{valor / 1024**3:.2f} GB"
                f"{RESET}"
            )

        elif opcao == "4":

            resultado = (
                valor * 9 / 5
            ) + 32

            print(
                f"{GREEN}{resultado:.2f} °F{RESET}"
            )

        elif opcao == "5":

            resultado = (
                valor - 32
            ) * 5 / 9

            print(
                f"{GREEN}{resultado:.2f} °C{RESET}"
            )

        else:

            erro("Opção inválida.")

        pausar()


# ==========================================
# TESTAR PING
# ==========================================

def testar_ping():

    limpar_tela()

    host = input(
        "\nDigite o domínio ou IP: "
    ).strip()

    if not host:

        erro("Digite um endereço.")
        return

    sistema = platform.system().lower()

    comando = (
        ["ping", "-n", "1", host]
        if sistema == "windows"
        else ["ping", "-c", "1", host]
    )

    print(
        f"\n{BLUE}[~] Testando {host}...{RESET}"
    )

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
                f"{host} não respondeu."
            )

    except FileNotFoundError:

        erro(
            "O comando ping não está disponível."
        )

    except subprocess.TimeoutExpired:

        erro(
            "Tempo limite excedido."
        )


# ==========================================
# DNS
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

        for item in infos:

            ip = item[4][0]

            if ip not in ips:
                ips.append(ip)

        print(
            f"\n{GREEN}{BOLD}"
            f"[+] {dominio}"
            f"{RESET}"
        )

        for ip in ips:

            print(
                f"{WHITE}  └─ {ip}{RESET}"
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

    try:

        porta = int(
            input("Porta: ").strip()
        )

        if not 1 <= porta <= 65535:

            raise ValueError

    except ValueError:

        erro(
            "Porta inválida."
        )

        return

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
            "Host não encontrado."
        )


# ==========================================
# VERIFICAR ARQUIVO
# ==========================================

def verificar_caminho():

    limpar_tela()

    caminho = input(
        "\nCaminho: "
    ).strip()

    if not caminho:

        erro("Digite um caminho.")
        return

    caminho = os.path.expanduser(caminho)

    if os.path.isfile(caminho):

        tamanho = os.path.getsize(caminho)

        sucesso("Arquivo encontrado.")

        print(
            f"{WHITE}Caminho: {caminho}{RESET}"
        )

        print(
            f"{WHITE}Tamanho: {tamanho} bytes{RESET}"
        )

    elif os.path.isdir(caminho):

        try:

            quantidade = len(
                os.listdir(caminho)
            )

            sucesso("Diretório encontrado.")

            print(
                f"{WHITE}Caminho: {caminho}{RESET}"
            )

            print(
                f"{WHITE}Itens: {quantidade}{RESET}"
            )

        except OSError:

            erro(
                "Não foi possível acessar o diretório."
            )

    else:

        aviso(
            "Arquivo ou diretório não encontrado."
        )


# ==========================================
# CONECTIVIDADE
# ==========================================

def verificar_conectividade():

    limpar_tela()

    destinos = [
        ("Google", "google.com", 443),
        ("Cloudflare", "cloudflare.com", 443),
        ("GitHub", "github.com", 443)
    ]

    print(
        f"{BLUE}{BOLD}"
        "╔══════════════════════════════════════╗"
        f"{RESET}"
    )
    print(
        f"{BLUE}{BOLD}"
        "║         TESTE DE CONECTIVIDADE      ║"
        f"{RESET}"
    )
    print(
        f"{BLUE}{BOLD}"
        "╠══════════════════════════════════════╣"
        f"{RESET}"
    )

    for nome, host, porta in destinos:

        try:

            with socket.create_connection(
                (host, porta),
                timeout=3
            ):

                print(
                    f"{GREEN}[+] {nome:<15} ONLINE{RESET}"
                )

        except OSError:

            print(
                f"{RED}[-] {nome:<15} OFFLINE{RESET}"
            )

    print(
        f"{BLUE}{BOLD}"
        "╚══════════════════════════════════════╝"
        f"{RESET}"
    )


# ==========================================
# TIMESTAMP
# ==========================================

def timestamp():

    limpar_tela()

    agora = datetime.now()

    unix = int(
        agora.timestamp()
    )

    print(
        f"{GREEN}{BOLD}"
        f"Timestamp atual: {unix}"
        f"{RESET}"
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

        opcoes = [
            "[1] Informações do sistema",
            "[2] Uso de armazenamento",
            "[3] Data e hora",
            "[4] Calculadora",
            "[5] Gerador de senha",
            "[6] Gerar UUID",
            "[7] Conversor de unidades",
            "[8] Testar ping",
            "[9] Resolver DNS",
            "[10] Verificar porta",
            "[11] Verificar arquivo/diretório",
            "[12] Testar conectividade",
            "[13] Timestamp Unix"
        ]

        for opcao in opcoes:

            print(
                f"{WHITE}║ {opcao:<36} ║{RESET}"
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
            calculadora()

        elif opcao == "5":
            gerar_senha()

        elif opcao == "6":
            gerar_uuid()

        elif opcao == "7":
            conversor_unidades()

        elif opcao == "8":
            testar_ping()

        elif opcao == "9":
            resolver_dns()

        elif opcao == "10":
            verificar_porta()

        elif opcao == "11":
            verificar_caminho()

        elif opcao == "12":
            verificar_conectividade()

        elif opcao == "13":
            timestamp()

        elif opcao == "0":
            break

        else:
            erro("Opção inválida.")

        if opcao != "0":
            pausar()