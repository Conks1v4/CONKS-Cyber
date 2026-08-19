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
# DIRETÓRIO DO PROJETO
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ==========================================
# LIMPAR TELA
# ==========================================

def limpar_tela():

    os.system("clear")


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
        f"{YELLOW}[!] {texto}{RESET}"
    )


def info(texto):

    print(
        f"{BLUE}[i] {texto}{RESET}"
    )


# ==========================================
# CAIXA PADRÃO
# ==========================================

LARGURA = 38


def caixa(titulo, linhas=None, cor=BLUE):

    if linhas is None:
        linhas = []

    print(
        f"{cor}{BOLD}"
        "╔══════════════════════════════════════╗"
        f"{RESET}"
    )

    titulo_formatado = titulo.center(
        LARGURA - 2
    )

    print(
        f"{cor}{BOLD}"
        f"║{titulo_formatado}║"
        f"{RESET}"
    )

    print(
        f"{cor}{BOLD}"
        "╠══════════════════════════════════════╣"
        f"{RESET}"
    )

    for texto, cor_linha in linhas:

        texto = str(texto)

        if len(texto) > LARGURA - 2:

            texto = texto[
                :LARGURA - 5
            ] + "..."

        linha = (
            "║ "
            + texto.ljust(LARGURA - 3)
            + " ║"
        )

        print(
            f"{cor_linha}{linha}{RESET}"
        )

    print(
        f"{cor}{BOLD}"
        "╚══════════════════════════════════════╝"
        f"{RESET}"
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

    servidores = [
        ("Google", "google.com", 443),
        ("Cloudflare", "cloudflare.com", 443),
        ("GitHub", "github.com", 443)
    ]

    limpar_tela()

    linhas = []

    online = False

    for nome, host, porta in servidores:

        try:

            conexao = socket.create_connection(
                (host, porta),
                timeout=3
            )

            conexao.close()

            linhas.append(
                (
                    f"[+] {nome:<15} ONLINE",
                    GREEN
                )
            )

            online = True

        except (
            socket.timeout,
            socket.gaierror,
            OSError
        ):

            linhas.append(
                (
                    f"[-] {nome:<15} OFFLINE",
                    RED
                )
            )

    caixa(
        "TESTE DE CONEXÃO",
        linhas
    )

    print()

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

    limpar_tela()

    caixa(
        "MEU IP PÚBLICO"
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

                print()

                sucesso(
                    f"IP público: {ip}"
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
# ATUALIZAR PAINEL
# ==========================================

def atualizar_painel():

    limpar_tela()

    caixa(
        "ATUALIZAR PAINEL",
        [
            (
                "CONKS CYBER UPDATE SYSTEM",
                WHITE
            ),
            (
                "Verificando GitHub...",
                BLUE
            )
        ]
    )

    print()

    print(
        f"{BLUE}{BOLD}"
        "[~] Preparando atualização..."
        f"{RESET}"
    )

    time.sleep(0.5)

    # --------------------------------------
    # Verificar se é um repositório Git
    # --------------------------------------

    git_dir = os.path.join(
        BASE_DIR,
        ".git"
    )

    if not os.path.isdir(git_dir):

        erro(
            "Este diretório não é um repositório Git."
        )

        aviso(
            "Verifique se o painel foi baixado corretamente."
        )

        input(
            f"\n{GRAY}"
            "Pressione ENTER para voltar..."
            f"{RESET}"
        )

        return

    print(
        f"{BLUE}[~] Buscando atualizações...{RESET}"
    )

    try:

        # ----------------------------------
        # git fetch
        # ----------------------------------

        fetch = subprocess.run(
            [
                "git",
                "fetch",
                "origin"
            ],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )

        if fetch.returncode != 0:

            erro(
                "Não foi possível verificar o GitHub."
            )

            if fetch.stderr.strip():

                print(
                    f"\n{GRAY}"
                    f"{fetch.stderr.strip()}"
                    f"{RESET}"
                )

            input(
                f"\n{GRAY}"
                "Pressione ENTER para voltar..."
                f"{RESET}"
            )

            return

        print(
            f"{GREEN}[+] GitHub conectado.{RESET}"
        )

        time.sleep(0.4)

        # ----------------------------------
        # Verificar diferenças
        # ----------------------------------

        comparacao = subprocess.run(
            [
                "git",
                "rev-list",
                "--count",
                "HEAD..origin/main"
            ],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )

        if comparacao.returncode != 0:

            erro(
                "Não foi possível verificar a versão."
            )

            input(
                f"\n{GRAY}"
                "Pressione ENTER para voltar..."
                f"{RESET}"
            )

            return

        try:

            quantidade = int(
                comparacao.stdout.strip()
                or "0"
            )

        except ValueError:

            quantidade = 0

        # ----------------------------------
        # Já está atualizado
        # ----------------------------------

        if quantidade == 0:

            print()

            caixa(
                "PAINEL ATUALIZADO",
                [
                    (
                        "O painel está na versão mais recente.",
                        YELLOW
                    )
                ],
                YELLOW
            )

            input(
                f"\n{GRAY}"
                "Pressione ENTER para voltar..."
                f"{RESET}"
            )

            return

        # ----------------------------------
        # Existem atualizações
        # ----------------------------------

        print()

        print(
            f"{YELLOW}{BOLD}"
            f"[!] {quantidade} atualização(ões) encontrada(s)."
            f"{RESET}"
        )

        print(
            f"{BLUE}[~] Baixando atualizações...{RESET}"
        )

        time.sleep(0.5)

        # ----------------------------------
        # Git pull
        # ----------------------------------

        resultado = subprocess.run(
            [
                "git",
                "pull",
                "--ff-only",
                "origin",
                "main"
            ],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )

        if resultado.returncode != 0:

            erro(
                "Não foi possível aplicar a atualização."
            )

            saida = (
                resultado.stdout +
                resultado.stderr
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

        print(
            f"{GREEN}[+] Arquivos atualizados.{RESET}"
        )

        print(
            f"{GREEN}[+] Atualização concluída!{RESET}"
        )

        print()

        caixa(
            "ATUALIZAÇÃO CONCLUÍDA",
            [
                (
                    "O CONKS Cyber foi atualizado.",
                    GREEN
                ),
                (
                    "Reinicie o painel para carregar tudo.",
                    WHITE
                )
            ],
            GREEN
        )

        if resultado.stdout.strip():

            print(
                f"\n{GRAY}"
                f"{resultado.stdout.strip()}"
                f"{RESET}"
            )

    except subprocess.TimeoutExpired:

        erro(
            "A atualização demorou demais."
        )

    except FileNotFoundError:

        erro(
            "Git não está instalado neste dispositivo."
        )

        print(
            f"{GRAY}"
            "No Termux, instale com: pkg install git"
            f"{RESET}"
        )

    except Exception as erro_inesperado:

        erro(
            f"Erro ao atualizar: {erro_inesperado}"
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

        caixa(
            "REDE",
            [
                (
                    "[1] Meu IP público",
                    WHITE
                ),
                (
                    "[2] Testar conexão",
                    WHITE
                ),
                (
                    "[0] Voltar",
                    RED
                )
            ]
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

            erro(
                "Opção inválida."
            )

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

        caixa(
            "MENU PRINCIPAL",
            [
                (
                    "[1] Geradores",
                    WHITE
                ),
                (
                    "[2] Consultas",
                    WHITE
                ),
                (
                    "[3] OSINT",
                    WHITE
                ),
                (
                    "[4] Rede",
                    WHITE
                ),
                (
                    "[5] Validadores",
                    WHITE
                ),
                (
                    "[6] Utilidades",
                    WHITE
                ),
                (
                    "[7] Atualizar painel",
                    WHITE
                ),
                (
                    "",
                    WHITE
                ),
                (
                    "[0] Sair",
                    RED
                )
            ]
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
        # ATUALIZAR
        # ==================================

        elif opcao == "7":

            atualizar_painel()

        # ==================================
        # SAIR
        # ==================================

        elif opcao == "0":

            limpar_tela()

            caixa(
                "CONKS CYBER",
                [
                    (
                        "CONKS Cyber encerrado.",
                        RED
                    )
                ],
                RED
            )

            print()

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


# ==========================================
# EXECUÇÃO
# ==========================================

if __name__ == "__main__":

    main()