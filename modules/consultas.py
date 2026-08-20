import urllib.request
import urllib.error
import json
import re
import subprocess
import webbrowser
from datetime import datetime
import requests
import hashlib

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
# CPF
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


def consultar_havel_alldata(cpf_limpo):
    """Consulta via Havell Alldata (API pública)"""
    try:
        url = f"https://www.havelalldata.com/api/v1/cpf/{cpf_limpo}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            dados = response.json()
            if dados.get("status") == "success":
                return {
                    "nome": dados.get("nome_completo"),
                    "data_nascimento": dados.get("data_nascimento"),
                    "sexo": dados.get("sexo"),
                    "nome_mae": dados.get("nome_mae"),
                    "nome_pai": dados.get("nome_pai"),
                    "situacao": dados.get("situacao_cpf"),
                    "rg": dados.get("rg"),
                    "orgao_emissor": dados.get("orgao_emissor"),
                    "uf": dados.get("uf")
                }
    except:
        pass
    return None


def consultar_api_4devs_public(cpf_limpo, data_nascimento):
    """Consulta via 4Devs (serviço público)"""
    try:
        url = "https://www.4devs.com.br/ferramentas_online.php"
        
        payload = {
            "acao": "validar_cpf",
            "txt_cpf": cpf_limpo,
            "txt_data_nascimento": data_nascimento
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            dados = response.json()
            if dados.get("status") == "1":
                return {
                    "nome": dados.get("nome"),
                    "data_nascimento": dados.get("data_nascimento"),
                    "sexo": dados.get("sexo"),
                    "nome_mae": dados.get("nome_mae"),
                    "nome_pai": dados.get("nome_pai"),
                    "situacao": dados.get("situacao_cpf"),
                    "codigo_cpf": dados.get("codigo_cpf")
                }
    except:
        pass
    return None


def consultar_base_publica(cpf_limpo):
    """Consulta em bases públicas de dados vazados"""
    try:
        # Simula consulta em base pública (exemplo)
        # Na prática, você pode usar serviços como:
        # - LeakCheck
        # - DeHashed
        # - Have I Been Pwned
        
        url = f"https://leakcheck.io/api/public?key=suachave&check={cpf_limpo}"
        # Nota: Isso é apenas um exemplo, você precisa de uma chave válida
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            dados = response.json()
            if dados.get("found"):
                return {
                    "nome": dados.get("nome"),
                    "data_nascimento": dados.get("data_nascimento"),
                    "email": dados.get("email"),
                    "telefone": dados.get("telefone"),
                    "endereco": dados.get("endereco"),
                    "fonte": "LeakCheck"
                }
    except:
        pass
    return None


def consultar_situacao_cpf(cpf_limpo):
    """Consulta situação do CPF na Receita"""
    try:
        # API simplificada para verificar situação
        url = f"https://api.cpfreais.com/api/v1/consulta/{cpf_limpo}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            dados = response.json()
            return {
                "situacao": dados.get("situacao", "Ativo"),
                "data_consulta": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "fonte": "CPFReais"
            }
    except:
        pass
    return None


def consultar_email_by_cpf(cpf_limpo):
    """Tenta encontrar emails associados ao CPF"""
    try:
        # Busca em bases de email públicos
        url = f"https://emailrep.io/query?q={cpf_limpo}@gmail.com"
        # Isso é apenas ilustrativo - precisa de API real
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            if dados.get("email"):
                return {
                    "email": dados.get("email"),
                    "dominio": dados.get("domain"),
                    "fonte": "EmailRep"
                }
    except:
        pass
    return None


def consultar_telefone_by_cpf(cpf_limpo):
    """Tenta encontrar telefones associados ao CPF"""
    try:
        # Exemplo com NumVerify (precisa de chave)
        url = f"https://api.numverify.com/validate?access_key=suachave&number={cpf_limpo}"
        # Isso é apenas ilustrativo
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            if dados.get("valid"):
                return {
                    "telefone": dados.get("number"),
                    "operadora": dados.get("carrier"),
                    "pais": dados.get("country_name")
                }
    except:
        pass
    return None


def consultar_cpf_via_serpro(cpf_limpo):
    """Consulta via SERPRO (requer autenticação)"""
    try:
        # SERPRO tem APIs pagas
        # Este é apenas um placeholder
        url = f"https://api.serpro.gov.br/cpf/v1/{cpf_limpo}"
        headers = {
            "Authorization": "Bearer SEU_TOKEN_AQUI",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            dados = response.json()
            return {
                "nome": dados.get("nome"),
                "data_nascimento": dados.get("dataNascimento"),
                "nome_mae": dados.get("nomeMae"),
                "situacao": dados.get("situacao"),
                "fonte": "SERPRO"
            }
    except:
        pass
    return None


def consulta_cpf():
    print("\n╔══════════════════════════════════════════╗")
    print("║              CONSULTA CPF               ║")
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
    print("\n[~] Buscando dados em múltiplas fontes...")

    cpf_limpo = limpar_cpf(cpf)
    dados_completos = None
    fontes_consultadas = []
    
    # Lista de funções de consulta com seus nomes
    consultas = [
        ("Havell Alldata", consultar_havel_alldata),
        ("4Devs", consultar_api_4devs_public),
        ("Base Pública", consultar_base_publica),
        ("Situação CPF", consultar_situacao_cpf)
    ]
    
    print("\n[~] Tentando fontes de dados...")
    
    for nome_fonte, funcao in consultas:
        print(f"[~] {nome_fonte}...")
        resultado = funcao(cpf_limpo)
        if resultado and resultado.get("nome"):
            dados_completos = resultado
            dados_completos["fonte_usada"] = nome_fonte
            break
        elif resultado and resultado.get("situacao"):
            # Dados parciais são melhores que nada
            if not dados_completos:
                dados_completos = resultado
                dados_completos["fonte_usada"] = nome_fonte
        fontes_consultadas.append(nome_fonte)
    
    if dados_completos and dados_completos.get("nome"):
        print(f"\n[+] Dados encontrados via: {dados_completos.get('fonte_usada')}")
        print("\n╔══════════════════════════════════════════╗")
        print("║           RESULTADO COMPLETO           ║")
        print("╠══════════════════════════════════════════╣")
        
        # Campos a exibir
        campos = [
            ("CPF", cpf_limpo),
            ("Nome", dados_completos.get("nome")),
            ("Data Nascimento", dados_completos.get("data_nascimento")),
            ("Sexo", dados_completos.get("sexo")),
            ("Nome da Mãe", dados_completos.get("nome_mae")),
            ("Nome do Pai", dados_completos.get("nome_pai")),
            ("Situação", dados_completos.get("situacao")),
            ("RG", dados_completos.get("rg")),
            ("Órgão Emissor", dados_completos.get("orgao_emissor")),
            ("UF", dados_completos.get("uf")),
            ("Email", dados_completos.get("email")),
            ("Telefone", dados_completos.get("telefone")),
            ("Fonte", dados_completos.get("fonte_usada"))
        ]
        
        for nome, valor in campos:
            if valor is not None and valor != "" and str(valor) != "None":
                valor_str = str(valor)
                if len(valor_str) > 20:
                    valor_str = valor_str[:17] + "..."
                print(f"║ {nome:<18}: {valor_str:<20} ║")
        
        print("╚══════════════════════════════════════════╝")
        return
    
    # Se chegou aqui, tenta dados básicos da Receita
    print("\n[~] Tentando obter dados básicos da Receita...")
    dados_receita = consultar_situacao_cpf(cpf_limpo)
    
    if dados_receita:
        print("\n╔══════════════════════════════════════════╗")
        print("║           DADOS DA RECEITA             ║")
        print("╠══════════════════════════════════════════╣")
        print(f"║ CPF: {cpf_limpo:<32} ║")
        print(f"║ Situação: {dados_receita.get('situacao', 'Ativo'):<24} ║")
        print(f"║ Data Consulta: {dados_receita.get('data_consulta'):<20} ║")
        print("╚══════════════════════════════════════════╝")
        return
    
    # Fallback - mostra apenas validação local
    print("\n[!] Todas as fontes de dados estão indisponíveis.")
    print("[i] Fontes consultadas: " + ", ".join(fontes_consultadas))
    
    print("\n╔══════════════════════════════════════════╗")
    print("║                RESULTADO               ║")
    print("╠══════════════════════════════════════════╣")
    print(f"║ CPF: {mascarar_cpf(cpf):<32} ║")
    print(f"║ Nascimento: {nascimento:<23} ║")
    print("║ Status: VALIDAÇÃO LOCAL                 ║")
    print("╚══════════════════════════════════════════╝")
    
    print("\n[i] A validação local não confirma a")
    print("[i] situação cadastral na Receita Federal.")
    print("\n[i] Sugestões:")
    print("    1. Verifique sua conexão com a internet")
    print("    2. Tente novamente em alguns minutos")
    print("    3. Use um serviço pago para consultas completas")


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
    cnpj = input("\nDigite o CNPJ: ").strip()

    if not cnpj:
        print("\n[!] Digite um CNPJ.")
        return

    if not validar_cnpj_local(cnpj):
        print("\n[-] CNPJ inválido.")
        return

    print("\n[~] Consultando CNPJ...")

    dados = consultar_cnpj(cnpj)

    if not dados:
        print(
            "\n[-] CNPJ não encontrado "
            "ou serviço indisponível."
        )
        return

    mostrar_cnpj(dados)


# ==========================================
# VEÍCULO
# ==========================================

def limpar_placa(placa):
    return re.sub(r"[^A-Za-z0-9]", "", placa).upper()


def validar_placa(placa):
    placa = limpar_placa(placa)

    # Modelo antigo: ABC1234
    modelo_antigo = re.fullmatch(
        r"[A-Z]{3}[0-9]{4}",
        placa
    )

    # Modelo Mercosul: ABC1D23
    modelo_mercosul = re.fullmatch(
        r"[A-Z]{3}[0-9][A-Z][0-9]{2}",
        placa
    )

    return bool(
        modelo_antigo or modelo_mercosul
    )


def abrir_consulta_senatran():
    url = (
        "https://www.gov.br/pt-br/servicos/"
        "consultar-online-os-dados-de-placa-veicular/"
    )

    # Termux: tenta abrir pelo comando oficial do Termux:API.
    try:
        subprocess.Popen(
            ["termux-open-url", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return True

    except (
        FileNotFoundError,
        OSError
    ):
        pass

    # Fallback para o navegador padrão.
    try:
        webbrowser.open(url)
        return True

    except Exception:
        return False


def consulta_veiculo():
    print("\n╔══════════════════════════════════════════╗")
    print("║            CONSULTA VEÍCULO             ║")
    print("╠══════════════════════════════════════════╣")
    print("║ Consulta oficial SENATRAN               ║")
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

    print(
        "\n[i] A consulta oficial da SENATRAN"
        "\n[i] exige o número de série do QR Code"
        "\n[i] da placa Mercosul."
    )

    serie = input(
        "\nNúmero de série do QR Code "
        "(ENTER para abrir o portal): "
    ).strip()

    print("\n[~] Abrindo consulta oficial...")

    abriu = abrir_consulta_senatran()

    if abriu:
        print("\n[+] Portal oficial aberto.")
        print(
            "[i] Informe a placa e o número de série "
            "do QR Code no portal."
        )
    else:
        print(
            "\n[-] Não foi possível abrir o navegador."
        )
        print(
            "[i] Acesse manualmente o portal oficial "
            "da SENATRAN."
        )

    if serie:
        print(
            "\n[i] Placa informada: "
            f"{placa}"
        )
        print(
            "[i] O código do QR Code foi recebido "
            "apenas localmente pelo painel."
        )


# ==========================================
# DOMÍNIO
# ==========================================

def consulta_dominio_menu():
    dominio = input("\nDigite o domínio: ").strip()

    if not dominio:
        print("\n[!] Digite um domínio.")
        return

    if not dominio_valido(dominio):
        print("\n[-] Domínio inválido.")
        return

    print("\n[~] Consultando domínio...")

    resultado = consultar_dominio(dominio)

    if not resultado:
        print(
            "\n[-] Não foi possível consultar o domínio."
        )
        return

    print("\n╔══════════════════════════════════════════╗")
    print("║            RESULTADO DOMÍNIO            ║")
    print("╠══════════════════════════════════════════╣")

    print(
        f"║ Domínio: {resultado['dominio']:<29} ║"
    )

    print("║ IPs:                                     ║")

    for ip in resultado["ips"]:
        print(f"║   - {ip:<34} ║")

    if resultado["aliases"]:
        print("║ Aliases:                                 ║")

        for alias in resultado["aliases"]:
            print(f"║   - {alias:<34} ║")

    print("╚══════════════════════════════════════════╝")


# ==========================================
# IP
# ==========================================

def consulta_ip_menu():
    ip = input("\nDigite o IP: ").strip()

    if not ip:
        print("\n[!] Digite um IP.")
        return

    if not ip_valido(ip):
        print("\n[-] IP inválido.")
        return

    print("\n[~] Consultando IP...")

    dados = consultar_ip(ip)

    if not dados:
        print(
            "\n[-] Não foi possível consultar esse IP."
        )
        return

    connection = dados.get("connection") or {}
    timezone = dados.get("timezone") or {}

    print("\n╔══════════════════════════════════════════╗")
    print("║              RESULTADO IP               ║")
    print("╠══════════════════════════════════════════╣")

    campos = [
        ("IP", dados.get("ip")),
        ("Tipo", dados.get("type")),
        ("Continente", dados.get("continent")),
        ("País", dados.get("country")),
        ("Código", dados.get("country_code")),
        ("Região", dados.get("region")),
        ("Cidade", dados.get("city")),
        ("CEP", dados.get("postal")),
        ("Latitude", dados.get("latitude")),
        ("Longitude", dados.get("longitude")),
        ("ASN", connection.get("asn")),
        ("Organização", connection.get("org")),
        ("ISP", connection.get("isp")),
        ("Domínio", connection.get("domain")),
        ("Timezone", timezone.get("id"))
    ]

    for nome, valor in campos:
        if valor is not None and valor != "":
            print(
                f"║ {nome:<18}: "
                f"{str(valor)[:20]:<20} ║"
            )

    print("╚══════════════════════════════════════════╝")
    print("\n[i] A localização de IP é aproximada.")


# ==========================================
# DNS
# ==========================================

def consulta_dns_menu():
    dominio = input("\nDigite o domínio: ").strip()

    if not dominio:
        print("\n[!] Digite um domínio.")
        return

    if not dominio_valido(dominio):
        print("\n[-] Domínio inválido.")
        return

    print("\n[~] Consultando DNS...")

    resultado = consultar_dns(dominio)

    if not resultado:
        print(
            "\n[-] Não foi possível consultar o DNS."
        )
        return

    print("\n╔══════════════════════════════════════════╗")
    print("║              RESULTADO DNS              ║")
    print("╠══════════════════════════════════════════╣")

    print(
        f"║ Domínio: {resultado['dominio']:<29} ║"
    )

    print("║ IPs:                                     ║")

    for ip in resultado["ips"]:
        print(f"║   - {ip:<34} ║")

    if resultado["aliases"]:
        print("║ Aliases:                                 ║")

        for alias in resultado["aliases"]:
            print(f"║   - {alias:<34} ║")

    print("╚══════════════════════════════════════════╝")


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