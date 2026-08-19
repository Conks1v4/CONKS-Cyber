from utils.validators import (
    validar_cpf,
    validar_cnpj,
    validar_ip,
    validar_uuid
)


def menu_validadores():

    while True:

        print("\n╔══════════════════════════════════════╗")
        print("║             VALIDADORES              ║")
        print("╠══════════════════════════════════════╣")
        print("║ [1] Validar CPF                      ║")
        print("║ [2] Validar CNPJ                     ║")
        print("║ [3] Validar IP                       ║")
        print("║ [4] Validar UUID                     ║")
        print("║ [0] Voltar                            ║")
        print("╚══════════════════════════════════════╝")

        opcao = input("\nCONKS@Validadores > ").strip()

        if opcao == "1":
            valor = input("Digite o CPF: ")
            resultado = validar_cpf(valor)

            if resultado:
                print("\n[+] CPF válido.")
            else:
                print("\n[-] CPF inválido.")

        elif opcao == "2":
            valor = input("Digite o CNPJ: ")
            resultado = validar_cnpj(valor)

            if resultado:
                print("\n[+] CNPJ válido.")
            else:
                print("\n[-] CNPJ inválido.")

        elif opcao == "3":
            valor = input("Digite o IP: ")
            resultado = validar_ip(valor)

            if resultado:
                print("\n[+] IP válido.")
            else:
                print("\n[-] IP inválido.")

        elif opcao == "4":
            valor = input("Digite o UUID: ")
            resultado = validar_uuid(valor)

            if resultado:
                print("\n[+] UUID válido.")
            else:
                print("\n[-] UUID inválido.")

        elif opcao == "0":
            break

        else:
            print("\n[!] Opção inválida.")

        input("\nPressione ENTER para continuar...")