# ==========================================
# ATUALIZAR PAINEL
# ==========================================

def atualizar_painel():

    limpar_tela()

    print(
        f"{BLUE}{BOLD}"
        "╔══════════════════════════════════════╗"
        f"{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "║          ATUALIZAR PAINEL            ║"
        f"{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "╠══════════════════════════════════════╣"
        f"{RESET}"
    )

    print(
        f"{WHITE}║      CONKS CYBER UPDATE SYSTEM       ║{RESET}"
    )

    print(
        f"{WHITE}║                                      ║{RESET}"
    )

    print(
        f"{BLUE}{BOLD}"
        "╚══════════════════════════════════════╝"
        f"{RESET}"
    )

    print(
        f"\n{BLUE}[~] Verificando atualizações...{RESET}"
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
                f"\n{RED}[-] Não foi possível "
                f"atualizar o painel.{RESET}"
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
            or "Already up-to-date" in saida
        ):

            print(
                f"\n{YELLOW}{BOLD}"
                "╔══════════════════════════════════════╗"
                f"{RESET}"
            )

            print(
                f"{YELLOW}{BOLD}"
                "║                                      ║"
                f"{RESET}"
            )

            print(
                f"{YELLOW}{BOLD}"
                "║  O PAINEL ESTÁ NA VERSÃO MAIS       ║"
                f"{RESET}"
            )

            print(
                f"{YELLOW}{BOLD}"
                "║  RECENTE                             ║"
                f"{RESET}"
            )

            print(
                f"{YELLOW}{BOLD}"
                "║                                      ║"
                f"{RESET}"
            )

            print(
                f"{YELLOW}{BOLD}"
                "╚══════════════════════════════════════╝"
                f"{RESET}"
            )

            input(
                f"\n{GRAY}"
                "Pressione ENTER para voltar..."
                f"{RESET}"
            )

            return

        # ==================================
        # ATUALIZAÇÃO ENCONTRADA
        # ==================================

        print(
            f"\n{GREEN}{BOLD}"
            "╔══════════════════════════════════════╗"
            f"{RESET}"
        )

        print(
            f"{GREEN}{BOLD}"
            "║       ATUALIZAÇÃO CONCLUÍDA!        ║"
            f"{RESET}"
        )

        print(
            f"{GREEN}{BOLD}"
            "╠══════════════════════════════════════╣"
            f"{RESET}"
        )

        print(
            f"{GREEN}"
            "║ O painel foi atualizado com sucesso.║"
            f"{RESET}"
        )

        print(
            f"{GREEN}{BOLD}"
            "╚══════════════════════════════════════╝"
            f"{RESET}"
        )

        print(
            f"\n{BLUE}[~] Reiniciando o painel...{RESET}"
        )

        time.sleep(2)

        # ==================================
        # REINICIAR COM O ARQUIVO ATUALIZADO
        # ==================================

        os.execv(
            sys.executable,
            [sys.executable] + sys.argv
        )

    except subprocess.TimeoutExpired:

        print(
            f"\n{RED}[-] A atualização demorou "
            f"demais e foi cancelada.{RESET}"
        )

        input(
            f"\n{GRAY}"
            "Pressione ENTER para voltar..."
            f"{RESET}"
        )

    except FileNotFoundError:

        print(
            f"\n{RED}[-] Git não está instalado "
            f"neste dispositivo.{RESET}"
        )

        input(
            f"\n{GRAY}"
            "Pressione ENTER para voltar..."
            f"{RESET}"
        )

    except Exception as erro_inesperado:

        print(
            f"\n{RED}[-] Erro ao atualizar: "
            f"{erro_inesperado}{RESET}"
        )

        input(
            f"\n{GRAY}"
            "Pressione ENTER para voltar..."
            f"{RESET}"
        )
if __name__ == "__main__":
    main()