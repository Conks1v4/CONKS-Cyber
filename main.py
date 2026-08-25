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


# ==========================================
# CONFIGURAÇÃO DAS CAIXAS
# ==========================================

LARGURA = 38


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

        # ==================================
        # ERRO
        # ==================================

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

        # ==================================
        # JÁ ESTÁ ATUALIZADO
        # ==================================

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

        # ==================================
        # ATUALIZAÇÃO CONCLUÍDA
        # ==================================

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

        # ==================================
        # REINICIAR O PYTHON
        # ==================================

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
            "[7] ⚡ Shoot Down",
            RED,
            True
        )

        linha_caixa(
            "[8] Atualizar painel",
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
                    "Módulo de validadores "
                    "não encontrado."
                )

                input(
                    "\nPressione ENTER "
                    "para continuar..."
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
                    "Módulo de utilidades "
                    "não encontrado."
                )

                input(
                    "\nPressione ENTER "
                    "para continuar..."
                )

        # ==================================
        # SHOOT DOWN (NOVO!)
        # ==================================

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

        # ==================================
        # ATUALIZAR
        # ==================================

        elif opcao == "8":

            atualizar_painel()

        # ==================================
        # SAIR
        # ==================================

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

        # ==================================
        # OPÇÃO INVÁLIDA
        # ==================================

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