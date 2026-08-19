from utils.colors import CYAN, WHITE, GRAY, RESET
from modules.generators import (
    gerar_cpf,
    gerar_cnpj,
    gerar_telefone,
    gerar_uuid,
    gerar_senha
)


def menu_geradores():

    while True:
        print()
        print(CYAN + "╔══════════════════════════════════════╗")
        print("║              GERADORES               ║")
        print("╠══════════════════════════════════════╣")
        print(WHITE + "║ [1] Gerar CPF                        ║")
        print("║ [2] Gerar CNPJ                       ║")
        print("║ [3] Gerar Telefone                   ║")
        print("║ [4] Gerar UUID                       ║")
        print("║ [5] Gerar Senha                      ║")
        print(GRAY + "║ [0] Voltar                            ║")
        print(CYAN + "╚══════════════════════════════════════╝" + RESET)

        opcao = input("\nCONKS@Geradores > ").strip()

        if opcao == "1":
            print(f"\n[+] CPF: {gerar_cpf()}")

        elif opcao == "2":
            print(f"\n[+] CNPJ: {gerar_cnpj()}")

        elif opcao == "3":
            print(f"\n[+] Telefone: {gerar_telefone()}")

        elif opcao == "4":
            print(f"\n[+] UUID: {gerar_uuid()}")

        elif opcao == "5":
            print(f"\n[+] Senha: {gerar_senha()}")

        elif opcao == "0":
            break

        else:
            print("\n[!] Opção inválida.")

        input("\nPressione ENTER para continuar...")