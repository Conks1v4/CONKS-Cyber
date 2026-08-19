# ==========================================
# CONKS CYBER
# main.py
# ==========================================

import os
import sys
import socket
import urllib.request
import urllib.error

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
    print(f"{RED}[!] {texto}{RESET}")


def info(texto):
    print(f"{BLUE}[i] {texto}{RESET}")


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

    print(
        f"\n{BLUE}{BOLD}"
        "╔══════════════════════════════════════╗"
        f"{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "║          TESTE DE CONEXÃO            ║"
        f"{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "╠══════════════════════════════════════╣"
        f"{RESET}"
    )

    servidores = [
        ("Google", "google.com", 443),
        ("Cloudflare", "cloudflare.com", 443),
        ("GitHub", "github.com", 443)
    ]

    online = False

    for nome, host, porta in servidores:

        try:

            socket.create_connection(
                (host, porta),
                timeout=3
            )

            print(
                f"{GREEN}[+] {nome:<15} ONLINE{RESET}"
            )

            online = True

        except (
            socket.timeout,
            socket.gaierror,
            OSError
        ):

            print(
                f"{RED}[-] {nome:<15} OFFLINE{RESET}"
            )

    print(
        f"{BLUE}{BOLD}"
        "╚══════════════════════════════════════╝"
        f"{RESET}"
    )

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

    print(
        f"\n{BLUE}{BOLD}"
        "╔══════════════════════════════════════╗"
        f"{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "║           MEU IP PÚBLICO             ║"
        f"{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "╚══════════════════════════════════════╝"
        f"{RESET}"
    )

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
                    "User-Agent": "CONKS-Cyber/1.0"
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

                print(
                    f"\n{GREEN}{BOLD}"
                    f"IP público: {ip}"
                    f"{RESET}"
                )

                return

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            OSError
        ):

            continue

    erro(
        "Não foi possível obter o IP público."
    )


# ==========================================
# MENU REDE
# ==========================================

def menu_rede():

    while True:

        print(
            f"\n{BLUE}{BOLD}"
            "╔══════════════════════════════════════╗"
            f"{RESET}"
        )

        print(
            f"{BLUE}{BOLD}"
            "║                 REDE                 ║"
            f"{RESET}"
        )

        print(
            f"{BLUE}{BOLD}"
            "╠══════════════════════════════════════╣"
            f"{RESET}"
        )

        print(
            f"{WHITE}║ [1] Meu IP público                   ║{RESET}"
        )

        print(
            f"{WHITE}║ [2] Testar conexão                   ║{RESET}"
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

            erro("Opção inválida.")

        if opcao != "0":

            input(
                f"\n{GRAY}"
                "Pressione ENTER para continuar..."
                f"{RESET}"
            )


# ==========================================
# MENU PRINCIPAL
# ==========================================

def menu_principal():

    while True:

        limpar_tela()

        banner()

        print(
            f"{BLUE}{BOLD}"
            "╔══════════════════════════════════════╗"
            f"{RESET}"
        )

        print(
            f"{BLUE}{BOLD}"
            "║             MENU PRINCIPAL           ║"
            f"{RESET}"
        )

        print(
            f"{BLUE}{BOLD}"
            "╠══════════════════════════════════════╣"
            f"{RESET}"
        )

        print(
            f"{WHITE}║ [1] Geradores                        ║{RESET}"
        )

        print(
            f"{WHITE}║ [2] Consultas                        ║{RESET}"
        )

        print(
            f"{WHITE}║ [3] OSINT                            ║{RESET}"
        )

        print(
            f"{WHITE}║ [4] Rede                             ║{RESET}"
        )

        print(
            f"{WHITE}║ [5] Validadores                      ║{RESET}"
        )

        print(
            f"{WHITE}║ [6] Utilidades                       ║{RESET}"
        )

        print(
            f"{WHITE}║                                      ║{RESET}"
        )

        print(
            f"{RED}{BOLD}"
            "║ [0] Sair                             ║"
            f"{RESET}"
        )

        print(
            f"{BLUE}{BOLD}"
            "╚══════════════════════════════════════╝"
            f"{RESET}"
        )

        opcao = input(
            f"\n{BLUE}{BOLD}"
            "CONKS@Cyber > "
            f"{RESET}"
        ).strip()

        # ==================================
        # GERADORES
        # ==================================

        if opcao == "1":

            limpar_tela()

            menu_geradores()

        # ==================================
        # CONSULTAS
        # ==================================

        elif opcao == "2":

            limpar_tela()

            menu_consultas()

        # ==================================
        # OSINT
        # ==================================

        elif opcao == "3":

            limpar_tela()

            menu_osint()

        # ==================================
        # REDE
        # ==================================

        elif opcao == "4":

            limpar_tela()

            menu_rede()

        # ==================================
        # VALIDADORES
        # ==================================

        elif opcao == "5":

            limpar_tela()

            try:

                from modules.validators import (
                    menu_validadores
                )

                menu_validadores()

            except ImportError:

                erro(
                    "Módulo de validadores não encontrado."
                )

                input(
                    "\nPressione ENTER para continuar..."
                )

        # ==================================
        # UTILIDADES
        # ==================================

        elif opcao == "6":

            limpar_tela()

            try:

                from modules.utilities import (
                    menu_utilidades
                )

                menu_utilidades()

            except ImportError:

                erro(
                    "Módulo de utilidades não encontrado."
                )

                input(
                    "\nPressione ENTER para continuar..."
                )

        # ==================================
        # SAIR
        # ==================================

        elif opcao == "0":

            limpar_tela()

            print(
                f"\n{RED}{BOLD}"
                "╔══════════════════════════════════════╗"
                f"{RESET}"
            )

            print(
                f"{RED}{BOLD}"
                "║        CONKS CYBER ENCERRADO        ║"
                f"{RESET}"
            )

            print(
                f"{RED}{BOLD}"
                "╚══════════════════════════════════════╝"
                f"{RESET}\n"
            )

            sys.exit(0)

        # ==================================
        # OPÇÃO INVÁLIDA
        # ==================================

        else:

            erro("Opção inválida.")

            input(
                f"\n{GRAY}"
                "Pressione ENTER para continuar..."
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


if __name__ == "__main__":
    main()