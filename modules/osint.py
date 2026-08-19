from modules.network import (
    consultar_dns,
    consultar_dominio
)


def menu_osint():

    while True:

        print("\n╔══════════════════════════════════════╗")
        print("║                OSINT                ║")
        print("╠══════════════════════════════════════╣")
        print("║ [1] Informações de domínio          ║")
        print("║ [2] Consulta DNS                    ║")
        print("║ [0] Voltar                          ║")
        print("╚══════════════════════════════════════╝")

        opcao = input("\nCONKS@OSINT > ").strip()

        if opcao == "1":

            dominio = input("\nDomínio: ").strip()

            if not dominio:
                print("\n[!] Digite um domínio.")
                input("\nPressione ENTER para continuar...")
                continue

            resultado = consultar_dominio(dominio)

            if resultado:
                print("\n[+] Domínio:", resultado["dominio"])
                print("[+] IP:", resultado["ip"])
            else:
                print("\n[-] Não foi possível resolver o domínio.")

        elif opcao == "2":

            dominio = input("\nDomínio: ").strip()

            if not dominio:
                print("\n[!] Digite um domínio.")
                input("\nPressione ENTER para continuar...")
                continue

            resultado = consultar_dns(dominio)

            if resultado:
                print("\n[+] Domínio:", resultado["dominio"])

                if resultado["aliases"]:
                    print("[+] Aliases:")
                    for alias in resultado["aliases"]:
                        print("   -", alias)

                print("[+] IPs:")
                for ip in resultado["ips"]:
                    print("   -", ip)

            else:
                print("\n[-] Não foi possível consultar o DNS.")

        elif opcao == "0":
            break

        else:
            print("\n[!] Opção inválida.")

        input("\nPressione ENTER para continuar...")