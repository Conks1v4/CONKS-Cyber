import urllib.request
import urllib.error
import json
import re
import subprocess
import webbrowser
from datetime import datetime
import requests
import os
import webbrowser
import time

from modules.network import (
    consultar_ip,
    consultar_dns,
    consultar_dominio,
    ip_valido,
    dominio_valido
)


# ==========================================
# UTILIDADES DE REQUISIÇÃO
# ==========================================

def requisicao_json(url, timeout=8):
    try:
        requisicao = urllib.request.Request(
            url,
            headers={
                "User-Agent": "CONKS-Cyber/1.0"
            }
        )

        with urllib.request.urlopen(
            requisicao,
            timeout=timeout
        ) as resposta:
            return json.loads(
                resposta.read().decode("utf-8")
            )

    except (
        urllib.error.URLError,
        urllib.error.HTTPError,
        TimeoutError,
        OSError,
        UnicodeError,
        json.JSONDecodeError
    ):
        return None


# ==========================================
# CPF - ABRIR SITES NO NAVEGADOR
# ==========================================

def limpar_cpf(cpf):
    return re.sub(r"\D", "", cpf)


def validar_cpf_local(cpf):
    cpf = limpar_cpf(cpf)

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    soma = sum(
        int(cpf[i]) * (10 - i)
        for i in range(9)
    )

    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    if int(cpf[9]) != digito1:
        return False

    soma = sum(
        int(cpf[i]) * (11 - i)
        for i in range(10)
    )

    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    return int(cpf[10]) == digito2


def validar_data_nascimento(data):
    try:
        nascimento = datetime.strptime(
            data,
            "%d/%m/%Y"
        ).date()

        hoje = datetime.now().date()

        return nascimento <= hoje

    except ValueError:
        return False


def mascarar_cpf(cpf):
    cpf = limpar_cpf(cpf)

    if len(cpf) != 11:
        return cpf

    return "*" * 9 + cpf[-2:]


def abrir_site_no_navegador(url):
    """Abre um site no navegador padrão"""
    try:
        # Tenta abrir no Termux
        try:
            subprocess.Popen(
                ["termux-open-url", url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
        except:
            pass
        
        # Fallback para navegador padrão
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"[-] Erro ao abrir: {str(e)}")
        return False


def consulta_cpf():
    print("\n╔══════════════════════════════════════════╗")
    print("║              CONSULTA CPF               ║")
    print("║        ABRINDO SITES NO NAVEGADOR       ║")
    print("╚══════════════════════════════════════════╝")

    cpf = input("\nCPF (apenas números): ").strip()
    nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()

    if not cpf:
        print("\n[!] Digite um CPF.")
        return

    if not nascimento:
        print("\n[!] Digite a data de nascimento.")
        return

    if not validar_cpf_local(cpf):
        print("\n[-] CPF inválido.")
        return

    if not validar_data_nascimento(nascimento):
        print("\n[-] Data de nascimento inválida.")
        return

    print("\n[+] CPF válido.")
    print("[+] Data de nascimento válida.")
    
    cpf_limpo = limpar_cpf(cpf)
    cpf_formatado = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    
    print("\n" + "="*60)
    print("                     MENU DE CONSULTA")
    print("="*60)
    print("\n[~] Escolha onde deseja consultar o CPF:")
    print("\n[1] Consultar em sites de dados vazados")
    print("[2] Consultar em sites oficiais")
    print("[3] Consultar em sites de busca")
    print("[4] Consultar em redes sociais")
    print("[5] Abrir TODOS os sites")
    print("[6] Voltar")
    
    opcao = input("\nEscolha uma opção: ").strip()
    
    if opcao == "6":
        return
    
    # ==========================================
    # SITES DE DADOS VAZADOS
    # ==========================================
    sites_vazados = [
        ("LeakCheck", f"https://leakcheck.io/search?q={cpf_limpo}"),
        ("DeHashed", f"https://dehashed.com/search?query=cpf:{cpf_limpo}"),
        ("HaveIBeenPwned", f"https://haveibeenpwned.com/account/{cpf_limpo}@gmail.com"),
        ("WeLeakInfo", f"https://weleakinfo.to/search?query={cpf_limpo}"),
        ("SnusBase", f"https://snusbase.com/search?q={cpf_limpo}"),
        ("LeakBase", f"https://leakbase.io/search?q={cpf_limpo}"),
        ("BreachDirectory", f"https://breachdirectory.org/?search={cpf_limpo}"),
        ("Leak-Lookup", f"https://leak-lookup.com/search?q={cpf_limpo}"),
        ("CyberNews", f"https://cybernews.com/personal-data-leak-check/?search={cpf_limpo}"),
    ]
    
    # ==========================================
    # SITES OFICIAIS
    # ==========================================
    sites_oficiais = [
        ("Receita Federal", f"https://www.receita.fazenda.gov.br/PessoaFisica/CPF/ConsultaSituacao/ConsultaPublica.asp"),
        ("SERPRO", f"https://www.serpro.gov.br/"),
        ("Portal da Transparência", f"https://www.portaltransparencia.gov.br/busca?q={cpf_limpo}"),
        ("TSE - Consulta Eleitor", f"https://divulgacandcontas.tse.jus.br/divulga/#/"),
        ("JusBrasil", f"https://www.jusbrasil.com.br/busca?q={cpf_limpo}"),
        ("Diário Oficial", f"https://pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp?busca={cpf_limpo}"),
    ]
    
    # ==========================================
    # SITES DE BUSCA
    # ==========================================
    sites_busca = [
        ("Google", f"https://www.google.com/search?q={cpf_limpo}+cpf+nome+data+nascimento"),
        ("Bing", f"https://www.bing.com/search?q={cpf_limpo}+cpf+nome"),
        ("DuckDuckGo", f"https://duckduckgo.com/?q={cpf_limpo}+cpf+nome"),
        ("Yahoo", f"https://search.yahoo.com/search?p={cpf_limpo}+cpf+nome"),
        ("Yandex", f"https://yandex.com/search/?text={cpf_limpo}+cpf+nome"),
    ]
    
    # ==========================================
    # REDES SOCIAIS
    # ==========================================
    sites_redes = [
        ("Facebook", f"https://www.facebook.com/search/top?q={cpf_limpo}"),
        ("LinkedIn", f"https://www.linkedin.com/search/results/all/?keywords={cpf_limpo}"),
        ("Instagram", f"https://www.instagram.com/web/search/topsearch/?query={cpf_limpo}"),
        ("Twitter", f"https://twitter.com/search?q={cpf_limpo}"),
        ("TikTok", f"https://www.tiktok.com/search?q={cpf_limpo}"),
        ("YouTube", f"https://www.youtube.com/results?search_query={cpf_limpo}"),
        ("Reddit", f"https://www.reddit.com/search/?q={cpf_limpo}"),
        ("Pinterest", f"https://br.pinterest.com/search/pins/?q={cpf_limpo}"),
    ]
    
    # ==========================================
    # SITES PARA CONSULTAR NOME COMPLETO
    # ==========================================
    sites_nome = [
        ("NameCheck", f"https://namecheck.com/?name={cpf_limpo}"),
        ("PeekYou", f"https://www.peekyou.com/{cpf_limpo}"),
        ("Pipl", f"https://pipl.com/search/?q={cpf_limpo}"),
        ("Spokeo", f"https://www.spokeo.com/search?q={cpf_limpo}"),
    ]
    
    # ==========================================
    # ABRIR SITES DE ACORDO COM A OPÇÃO
    # ==========================================
    
    sites_para_abrir = []
    
    if opcao == "1":
        print("\n[~] Abrindo sites de dados vazados...")
        sites_para_abrir = sites_vazados
    
    elif opcao == "2":
        print("\n[~] Abrindo sites oficiais...")
        sites_para_abrir = sites_oficiais
    
    elif opcao == "3":
        print("\n[~] Abrindo sites de busca...")
        sites_para_abrir = sites_busca
    
    elif opcao == "4":
        print("\n[~] Abrindo redes sociais...")
        sites_para_abrir = sites_redes
    
    elif opcao == "5":
        print("\n[~] Abrindo TODOS os sites...")
        sites_para_abrir = sites_vazados + sites_oficiais + sites_busca + sites_redes + sites_nome
    
    else:
        print("\n[!] Opção inválida.")
        return
    
    # ==========================================
    # EXIBE E ABRE OS SITES
    # ==========================================
    print("\n" + "="*60)
    print(f"                    CPF: {cpf_formatado}")
    print("="*60)
    print("\n[i] Preparando para abrir os sites...")
    print("[i] Aguarde alguns segundos...\n")
    
    contador = 0
    for nome, url in sites_para_abrir:
        contador += 1
        print(f"[{contador}] Abrindo {nome}...")
        print(f"    URL: {url}")
        
        try:
            # Abre o site no navegador
            abrir_site_no_navegador(url)
            time.sleep(0.5)  # Pequena pausa entre aberturas
        except Exception as e:
            print(f"    [!] Erro ao abrir: {str(e)[:50]}")
        print()
    
    print("="*60)
    print(f"[+] Total de {len(sites_para_abrir)} sites abertos!")
    print("[i] Verifique as abas do seu navegador")
    print("[i] Procure pelo CPF em cada site")
    
    # ==========================================
    # DICAS DE BUSCA
    # ==========================================
    print("\n" + "="*60)
    print("                     DICAS DE BUSCA")
    print("="*60)
    print("\n[1] Em sites de vazamento, busque por:")
    print(f"    - {cpf_limpo}")
    print(f"    - {cpf_formatado}")
    print(f"    - Seu nome completo")
    print(f"    - Seu email")
    
    print("\n[2] Em redes sociais, procure por:")
    print(f"    - Perfis com seu nome")
    print(f"    - Posts contendo {cpf_limpo}")
    print(f"    - Grupos que você participa")
    
    print("\n[3] Em sites de busca, use:")
    print(f'    - "{cpf_limpo}" site:.gov.br')
    print(f'    - "{cpf_limpo}" filetype:pdf')
    print(f'    - "{cpf_limpo}" -"indisponível"')
    
    print("\n[4] Sites recomendados para consulta:")
    print("    - Receita Federal: Consulta situação do CPF")
    print("    - Portal Transparência: Gastos públicos")
    print("    - TSE: Situação eleitoral")
    print("    - JusBrasil: Processos judiciais")
    
    print("\n" + "="*60)
    print("[!] LEMBRE-SE:")
    print("    - Respeite a LGPD")
    print("    - Use apenas para fins legítimos")
    print("    - Alguns sites podem exigir cadastro")
    print("="*60)


def consulta_cpf_especifico():
    """Consulta CPF em sites específicos escolhidos pelo usuário"""
    print("\n╔══════════════════════════════════════════╗")
    print("║        CONSULTA CPF - ESPECÍFICA       ║")
    print("╚══════════════════════════════════════════╝")
    
    cpf = input("\nCPF (apenas números): ").strip()
    nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()
    
    if not cpf:
        print("\n[!] Digite um CPF.")
        return
    
    if not nascimento:
        print("\n[!] Digite a data de nascimento.")
        return
    
    if not validar_cpf_local(cpf):
        print("\n[-] CPF inválido.")
        return
    
    if not validar_data_nascimento(nascimento):
        print("\n[-] Data de nascimento inválida.")
        return
    
    cpf_limpo = limpar_cpf(cpf)
    
    print("\n[~] Escolha um site específico:")
    print("\n[1] LeakCheck (dados vazados)")
    print("[2] DeHashed (dados vazados)")
    print("[3] HaveIBeenPwned (vazamentos)")
    print("[4] Receita Federal (situação CPF)")
    print("[5] Portal Transparência")
    print("[6] Google (busca geral)")
    print("[7] Facebook (redes sociais)")
    print("[8] LinkedIn (perfis profissionais)")
    print("[9] JusBrasil (processos)")
    print("[10] Abrir todos")
    
    opcao = input("\nEscolha: ").strip()
    
    sites = {
        "1": ("LeakCheck", f"https://leakcheck.io/search?q={cpf_limpo}"),
        "2": ("DeHashed", f"https://dehashed.com/search?query=cpf:{cpf_limpo}"),
        "3": ("HaveIBeenPwned", f"https://haveibeenpwned.com/account/{cpf_limpo}@gmail.com"),
        "4": ("Receita Federal", "https://www.receita.fazenda.gov.br/PessoaFisica/CPF/ConsultaSituacao/ConsultaPublica.asp"),
        "5": ("Portal Transparência", f"https://www.portaltransparencia.gov.br/busca?q={cpf_limpo}"),
        "6": ("Google", f"https://www.google.com/search?q={cpf_limpo}+cpf+nome"),
        "7": ("Facebook", f"https://www.facebook.com/search/top?q={cpf_limpo}"),
        "8": ("LinkedIn", f"https://www.linkedin.com/search/results/all/?keywords={cpf_limpo}"),
        "9": ("JusBrasil", f"https://www.jusbrasil.com.br/busca?q={cpf_limpo}"),
    }
    
    if opcao == "10":
        print("\n[~] Abrindo todos os sites...")
        for nome, url in sites.values():
            print(f"    Abrindo {nome}...")
            abrir_site_no_navegador(url)
            time.sleep(0.3)
        print("\n[+] Todos os sites abertos!")
    elif opcao in sites:
        nome, url = sites[opcao]
        print(f"\n[~] Abrindo {nome}...")
        abrir_site_no_navegador(url)
        print(f"\n[+] {nome} aberto!")
    else:
        print("\n[!] Opção inválida.")


# ==========================================
# CNPJ
# ==========================================

def limpar_cnpj(cnpj):
    return re.sub(r"\D", "", cnpj)


def validar_cnpj_local(cnpj):
    cnpj = limpar_cnpj(cnpj)

    if len(cnpj) != 14:
        return False

    if cnpj == cnpj[0] * 14:
        return False

    numeros = [int(x) for x in cnpj]

    pesos1 = [
        5, 4, 3, 2,
        9, 8, 7, 6,
        5, 4, 3, 2
    ]

    soma = sum(
        numeros[i] * pesos1[i]
        for i in range(12)
    )

    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    if numeros[12] != digito1:
        return False

    pesos2 = [
        6, 5, 4, 3, 2,
        9, 8, 7, 6, 5, 4, 3, 2
    ]

    soma = sum(
        numeros[i] * pesos2[i]
        for i in range(13)
    )

    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    return numeros[13] == digito2


def consultar_cnpj(cnpj):
    cnpj = limpar_cnpj(cnpj)

    if len(cnpj) != 14:
        return None

    url = (
        "https://brasilapi.com.br/api/cnpj/v1/"
        + cnpj
    )

    return requisicao_json(url)


def mostrar_cnpj(dados):
    print("\n╔══════════════════════════════════════════╗")
    print("║             RESULTADO CNPJ             ║")
    print("╠══════════════════════════════════════════╣")

    campos = [
        ("CNPJ", "cnpj"),
        ("Razão Social", "razao_social"),
        ("Nome Fantasia", "nome_fantasia"),
        ("Situação", "descricao_situacao_cadastral"),
        ("Abertura", "data_inicio_atividade"),
        ("Porte", "porte"),
        ("Natureza", "natureza_juridica"),
        ("Município", "municipio"),
        ("UF", "uf"),
        ("CEP", "cep")
    ]

    for nome, chave in campos:
        valor = dados.get(chave)

        if valor:
            print(
                f"║ {nome:<18}: "
                f"{str(valor)[:20]:<20} ║"
            )

    print("╚══════════════════════════════════════════╝")


def consulta_cnpj_menu():
    print("\n╔══════════════════════════════════════════╗")
    print("║             CONSULTA CNPJ               ║")
    print("╚══════════════════════════════════════════╝")
    
    cnpj = input("\nDigite o CNPJ: ").strip()

    if not cnpj:
        print("\n[!] Digite um CNPJ.")
        return

    if not validar_cnpj_local(cnpj):
        print("\n[-] CNPJ inválido.")
        return

    cnpj_limpo = limpar_cnpj(cnpj)
    
    print("\n[~] Abrindo sites para consulta de CNPJ...")
    
    sites_cnpj = [
        ("Receita Federal", "https://www.receita.fazenda.gov.br/pessoaJuridica/cnpj/cnpjreval/Cnpjreval_Resposta.aspx"),
        ("BrasilAPI", f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"),
        ("JusBrasil", f"https://www.jusbrasil.com.br/busca?q={cnpj_limpo}"),
        ("Google", f"https://www.google.com/search?q={cnpj_limpo}+cnpj+nome"),
        ("Portal Transparência", f"https://www.portaltransparencia.gov.br/busca?q={cnpj_limpo}"),
    ]
    
    for nome, url in sites_cnpj:
        print(f"    Abrindo {nome}...")
        abrir_site_no_navegador(url)
        time.sleep(0.3)
    
    print(f"\n[+] {len(sites_cnpj)} sites abertos para consulta de CNPJ!")


# ==========================================
# VEÍCULO
# ==========================================

def limpar_placa(placa):
    return re.sub(r"[^A-Za-z0-9]", "", placa).upper()


def validar_placa(placa):
    placa = limpar_placa(placa)

    modelo_antigo = re.fullmatch(
        r"[A-Z]{3}[0-9]{4}",
        placa
    )

    modelo_mercosul = re.fullmatch(
        r"[A-Z]{3}[0-9][A-Z][0-9]{2}",
        placa
    )

    return bool(
        modelo_antigo or modelo_mercosul
    )


def consulta_veiculo():
    print("\n╔══════════════════════════════════════════╗")
    print("║            CONSULTA VEÍCULO             ║")
    print("╚══════════════════════════════════════════╝")

    placa = input("\nPlaca: ").strip()

    if not placa:
        print("\n[!] Digite uma placa.")
        return

    placa = limpar_placa(placa)

    if not validar_placa(placa):
        print("\n[-] Formato de placa inválido.")
        print("[i] Exemplos: ABC1234 ou ABC1D23")
        return

    print(f"\n[+] Placa reconhecida: {placa}")
    
    print("\n[~] Abrindo sites para consulta de veículo...")
    
    sites_veiculo = [
        ("SENATRAN", "https://www.gov.br/pt-br/servicos/consultar-online-os-dados-de-placa-veicular/"),
        ("Sinesp Cidadão", "https://www.sinesp.gov.br/sinesp-cidadao/"),
        ("Detran", "https://www.detran.xxx.gov.br/"),  # Substitua pelo estado
        ("Google", f"https://www.google.com/search?q={placa}+placa+veiculo"),
    ]
    
    for nome, url in sites_veiculo:
        print(f"    Abrindo {nome}...")
        abrir_site_no_navegador(url)
        time.sleep(0.3)
    
    print(f"\n[+] {len(sites_veiculo)} sites abertos para consulta de veículo!")


# ==========================================
# DOMÍNIO
# ==========================================

def consulta_dominio_menu():
    print("\n╔══════════════════════════════════════════╗")
    print("║            CONSULTA DOMÍNIO             ║")
    print("╚══════════════════════════════════════════╝")
    
    dominio = input("\nDigite o domínio: ").strip()

    if not dominio:
        print("\n[!] Digite um domínio.")
        return

    if not dominio_valido(dominio):
        print("\n[-] Domínio inválido.")
        return

    print(f"\n[~] Abrindo sites para consulta do domínio {dominio}...")
    
    sites_dominio = [
        ("Whois", f"https://who.is/whois/{dominio}"),
        ("Registro.br", f"https://registro.br/tecnologia/ferramentas/whois/?search={dominio}"),
        ("Google", f"https://www.google.com/search?q={dominio}"),
        ("VirusTotal", f"https://www.virustotal.com/gui/domain/{dominio}"),
    ]
    
    for nome, url in sites_dominio:
        print(f"    Abrindo {nome}...")
        abrir_site_no_navegador(url)
        time.sleep(0.3)
    
    print(f"\n[+] {len(sites_dominio)} sites abertos para consulta do domínio!")


# ==========================================
# IP
# ==========================================

def consulta_ip_menu():
    print("\n╔══════════════════════════════════════════╗")
    print("║             CONSULTA IP                 ║")
    print("╚══════════════════════════════════════════╝")
    
    ip = input("\nDigite o IP: ").strip()

    if not ip:
        print("\n[!] Digite um IP.")
        return

    if not ip_valido(ip):
        print("\n[-] IP inválido.")
        return

    print(f"\n[~] Abrindo sites para consulta do IP {ip}...")
    
    sites_ip = [
        ("IPInfo", f"https://ipinfo.io/{ip}"),
        ("WhatIsMyIP", f"https://whatismyipaddress.com/ip/{ip}"),
        ("IP2Location", f"https://www.ip2location.com/demo/{ip}"),
        ("GeoIPTool", f"https://www.geoiptool.com/pt/?ip={ip}"),
        ("AbuseIPDB", f"https://www.abuseipdb.com/check/{ip}"),
        ("VirusTotal", f"https://www.virustotal.com/gui/ip-address/{ip}"),
    ]
    
    for nome, url in sites_ip:
        print(f"    Abrindo {nome}...")
        abrir_site_no_navegador(url)
        time.sleep(0.3)
    
    print(f"\n[+] {len(sites_ip)} sites abertos para consulta do IP!")


# ==========================================
# DNS
# ==========================================

def consulta_dns_menu():
    print("\n╔══════════════════════════════════════════╗")
    print("║             CONSULTA DNS                ║")
    print("╚══════════════════════════════════════════╝")
    
    dominio = input("\nDigite o domínio: ").strip()

    if not dominio:
        print("\n[!] Digite um domínio.")
        return

    if not dominio_valido(dominio):
        print("\n[-] Domínio inválido.")
        return

    print(f"\n[~] Abrindo sites para consulta de DNS do domínio {dominio}...")
    
    sites_dns = [
        ("DNS Checker", f"https://dnschecker.org/all-dns-records-of-domain/{dominio}"),
        ("MXToolbox", f"https://mxtoolbox.com/DNSLookup.aspx?domain={dominio}"),
        ("NSLookup", f"https://www.nslookup.io/domains/{dominio}"),
        ("WhatIsMyDNS", f"https://whatismydns.net/hostname/{dominio}"),
    ]
    
    for nome, url in sites_dns:
        print(f"    Abrindo {nome}...")
        abrir_site_no_navegador(url)
        time.sleep(0.3)
    
    print(f"\n[+] {len(sites_dns)} sites abertos para consulta de DNS!")


# ==========================================
# MENU CONSULTAS
# ==========================================

def menu_consultas():
    while True:

        print("\n╔══════════════════════════════════════╗")
        print("║              CONSULTAS              ║")
        print("╠══════════════════════════════════════╣")
        print("║ [1] Consultar CPF                   ║")
        print("║ [2] Consultar CNPJ                  ║")
        print("║ [3] Consultar Veículo               ║")
        print("║ [4] Consultar Domínio               ║")
        print("║ [5] Consultar IP                    ║")
        print("║ [6] Consultar DNS                   ║")
        print("║ [0] Voltar                           ║")
        print("╚══════════════════════════════════════╝")

        opcao = input(
            "\nCONKS@Consultas > "
        ).strip()

        if opcao == "1":
            print("\n[1] Consulta completa (vários sites)")
            print("[2] Consulta específica (escolher site)")
            sub_opcao = input("\nEscolha: ").strip()
            if sub_opcao == "2":
                consulta_cpf_especifico()
            else:
                consulta_cpf()

        elif opcao == "2":
            consulta_cnpj_menu()

        elif opcao == "3":
            consulta_veiculo()

        elif opcao == "4":
            consulta_dominio_menu()

        elif opcao == "5":
            consulta_ip_menu()

        elif opcao == "6":
            consulta_dns_menu()

        elif opcao == "0":
            break

        else:
            print("\n[!] Opção inválida.")

        input(
            "\nPressione ENTER para continuar..."
        )