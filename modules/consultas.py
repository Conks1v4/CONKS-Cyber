import urllib.request
import urllib.error
import json
import re
import subprocess
import webbrowser
from datetime import datetime
import requests
import hashlib
import base64
import random
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
# CPF - MÚLTIPLAS FONTES
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


# FONTE 1: BrasilAPI
def fonte_brasilapi(cpf_limpo):
    try:
        url = f"https://brasilapi.com.br/api/cpf/v1/{cpf_limpo}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            return {
                "nome": dados.get("nome"),
                "data_nascimento": dados.get("data_nascimento"),
                "sexo": dados.get("sexo"),
                "nome_mae": dados.get("nome_mae"),
                "nome_pai": dados.get("nome_pai"),
                "situacao": dados.get("situacao"),
                "fonte": "BrasilAPI"
            }
    except:
        pass
    return None


# FONTE 2: ReceitaWS
def fonte_receitaws(cpf_limpo):
    try:
        url = f"https://api.receitaws.com.br/v1/cpf/{cpf_limpo}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            if not dados.get("erro"):
                return {
                    "nome": dados.get("nome"),
                    "data_nascimento": dados.get("data_nascimento"),
                    "sexo": dados.get("sexo"),
                    "nome_mae": dados.get("mae"),
                    "nome_pai": dados.get("pai"),
                    "situacao": dados.get("situacao"),
                    "fonte": "ReceitaWS"
                }
    except:
        pass
    return None


# FONTE 3: 4Devs
def fonte_4devs(cpf_limpo, nascimento):
    try:
        url = "https://www.4devs.com.br/ferramentas_online.php"
        payload = {
            "acao": "validar_cpf",
            "txt_cpf": cpf_limpo,
            "txt_data_nascimento": nascimento
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
                    "fonte": "4Devs"
                }
    except:
        pass
    return None


# FONTE 4: CPFReais
def fonte_cpfreais(cpf_limpo):
    try:
        url = f"https://api.cpfreais.com/api/v1/consulta/{cpf_limpo}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            return {
                "nome": dados.get("nome"),
                "data_nascimento": dados.get("data_nascimento"),
                "sexo": dados.get("sexo"),
                "nome_mae": dados.get("nome_mae"),
                "situacao": dados.get("situacao"),
                "fonte": "CPFReais"
            }
    except:
        pass
    return None


# FONTE 5: Havell Alldata
def fonte_havell(cpf_limpo):
    try:
        url = f"https://www.havelalldata.com/api/v1/cpf/{cpf_limpo}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
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
                    "fonte": "Havell"
                }
    except:
        pass
    return None


# FONTE 6: LeakCheck (dados vazados)
def fonte_leakcheck(cpf_limpo):
    try:
        url = f"https://leakcheck.io/api/v1/check?key=YOUR_KEY&check={cpf_limpo}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            if dados.get("found"):
                leak_data = dados.get("sources", [{}])[0] if dados.get("sources") else {}
                return {
                    "nome": leak_data.get("name", dados.get("name")),
                    "email": leak_data.get("email"),
                    "telefone": leak_data.get("phone"),
                    "endereco": leak_data.get("address"),
                    "fonte": "LeakCheck"
                }
    except:
        pass
    return None


# FONTE 7: DeHashed (dados vazados)
def fonte_dehashed(cpf_limpo):
    try:
        url = f"https://api.dehashed.com/search?query=cpf:{cpf_limpo}"
        headers = {
            "Authorization": "Basic " + base64.b64encode(b"email:api_key").decode(),
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            if dados.get("entries"):
                entry = dados["entries"][0]
                return {
                    "nome": entry.get("name"),
                    "email": entry.get("email"),
                    "telefone": entry.get("phone"),
                    "senha_hash": entry.get("password"),
                    "fonte": "DeHashed"
                }
    except:
        pass
    return None


# FONTE 8: Have I Been Pwned
def fonte_hibp(cpf_limpo):
    try:
        email = f"{cpf_limpo}@gmail.com"
        hash_sufix = hashlib.sha1(email.encode()).hexdigest().upper()
        url = f"https://api.pwnedpasswords.com/range/{hash_sufix[:5]}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            hashes = response.text.split('\n')
            for h in hashes:
                if h.startswith(hash_sufix[5:]):
                    return {
                        "status": "VAZADO",
                        "fonte": "HIBP",
                        "observacao": "CPF/Email encontrado em vazamento",
                        "email": email
                    }
    except:
        pass
    return None


# FONTE 9: Scraping de sites públicos
def fonte_scraping_publico(cpf_limpo):
    try:
        urls = [
            f"https://www.google.com/search?q={cpf_limpo}+cpf",
            f"https://www.bing.com/search?q={cpf_limpo}+cpf",
        ]
        
        resultados = []
        for url in urls:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                html = response.text
                nomes = re.findall(r'[A-Z][a-záéíóúãõç]+ [A-Z][a-záéíóúãõç]+', html)
                emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)
                telefones = re.findall(r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}', html)
                
                if nomes or emails or telefones:
                    resultado = {
                        "fonte": "Scraping",
                        "url": url,
                        "possiveis_nomes": nomes[:5] if nomes else [],
                        "possiveis_emails": emails[:5] if emails else [],
                        "possiveis_telefones": telefones[:5] if telefones else []
                    }
                    resultados.append(resultado)
        return resultados if resultados else None
    except:
        pass
    return None


# FONTE 10: API SERPRO (pagamento)
def fonte_serpro(cpf_limpo):
    try:
        url = f"https://api.serpro.gov.br/cpf/v1/{cpf_limpo}"
        headers = {
            "Authorization": "Bearer SEU_TOKEN_SERPRO",
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


# FONTE 11: API do TSE
def fonte_tse(cpf_limpo):
    try:
        url = f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/consulta/2022/BR/candidato/{cpf_limpo}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            return {
                "nome": dados.get("nomeCompleto"),
                "data_nascimento": dados.get("dataNascimento"),
                "cargo": dados.get("cargo"),
                "fonte": "TSE"
            }
    except:
        pass
    return None


# FONTE 12: API CNPJ (sócios)
def fonte_cnpj_socios(cpf_limpo):
    try:
        url = f"https://api.cnpja.com.br/companies?cpf={cpf_limpo}"
        headers = {"Authorization": "Bearer SUA_CHAVE_CNPJA"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            if dados.get("companies"):
                empresas = []
                for empresa in dados["companies"][:5]:
                    empresas.append({
                        "cnpj": empresa.get("cnpj"),
                        "nome": empresa.get("nome"),
                        "cargo": empresa.get("cargo")
                    })
                return {
                    "empresas": empresas,
                    "fonte": "CNPJA"
                }
    except:
        pass
    return None


# FONTE 13: Google Dorks
def fonte_google_dorks(cpf_limpo):
    try:
        dorks = [
            f"site:*.gov.br {cpf_limpo}",
            f"site:*.edu.br {cpf_limpo}",
            f"filetype:pdf {cpf_limpo}",
            f"filetype:xlsx {cpf_limpo}",
            f"intitle:{cpf_limpo}"
        ]
        resultados = []
        for dork in dorks[:2]:
            url = f"https://www.google.com/search?q={dork.replace(' ', '+')}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                resultados.append({
                    "dork": dork,
                    "url": url,
                    "fonte": "GoogleDorks"
                })
        return resultados if resultados else None
    except:
        pass
    return None


# FONTE 14: Busca em PDFs públicos
def fonte_pdfs_publicos(cpf_limpo):
    try:
        url = f"https://www.google.com/search?q={cpf_limpo}+filetype:pdf"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # Extrai links de PDF
            pdf_links = re.findall(r'https?://[^\s]+\.pdf', response.text)
            if pdf_links:
                return {
                    "fonte": "PDFsPublicos",
                    "quantidade": len(pdf_links),
                    "links": pdf_links[:5]
                }
    except:
        pass
    return None


# FONTE 15: Busca em redes sociais
def fonte_redes_sociais(cpf_limpo):
    try:
        redes = [
            ("Facebook", f"https://www.facebook.com/search/top?q={cpf_limpo}"),
            ("LinkedIn", f"https://www.linkedin.com/search/results/all/?keywords={cpf_limpo}"),
            ("Instagram", f"https://www.instagram.com/web/search/topsearch/?query={cpf_limpo}")
        ]
        
        resultados = []
        for nome, url in redes:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                resultados.append({
                    "rede": nome,
                    "url": url,
                    "fonte": "RedesSociais",
                    "status": "Acessível"
                })
        return resultados if resultados else None
    except:
        pass
    return None


def exibir_dados_completos(dados, cpf_limpo):
    """Exibe dados completos formatados"""
    print(f"\n{'='*50}")
    print(f"[+] DADOS COMPLETOS ENCONTRADOS!")
    print(f"Fonte: {dados.get('fonte', 'Desconhecida')}")
    print("="*50)
    print("\n╔══════════════════════════════════════════╗")
    print("║           RESULTADO COMPLETO           ║")
    print("╠══════════════════════════════════════════╣")
    
    campos = [
        ("CPF", cpf_limpo),
        ("Nome", dados.get("nome")),
        ("Data Nascimento", dados.get("data_nascimento")),
        ("Sexo", dados.get("sexo")),
        ("Nome da Mãe", dados.get("nome_mae")),
        ("Nome do Pai", dados.get("nome_pai")),
        ("Situação", dados.get("situacao")),
        ("RG", dados.get("rg")),
        ("Email", dados.get("email")),
        ("Telefone", dados.get("telefone")),
        ("Endereço", dados.get("endereco")),
        ("Cargo", dados.get("cargo")),
        ("Fonte", dados.get("fonte"))
    ]
    
    for nome, valor in campos:
        if valor is not None and valor != "" and str(valor) != "None":
            valor_str = str(valor)
            if len(valor_str) > 20:
                valor_str = valor_str[:17] + "..."
            print(f"║ {nome:<18}: {valor_str:<20} ║")
    
    print("╚══════════════════════════════════════════╝")


def exibir_dados_parciais(dados_parciais):
    """Exibe todos os dados parciais encontrados"""
    print(f"\n[+] ENCONTRADOS {len(dados_parciais)} DADOS PARCIAIS")
    print("\n╔══════════════════════════════════════════╗")
    print("║           DADOS PARCIAIS               ║")
    print("╠══════════════════════════════════════════╣")
    
    for i, item in enumerate(dados_parciais, 1):
        if isinstance(item, dict):
            fonte = item.get("fonte", "Desconhecida")
            
            # Se for scraping com múltiplos dados
            if "possiveis_nomes" in item:
                print(f"║ {i}. {fonte:<15}                             ║")
                if item.get("possiveis_nomes"):
                    nomes = item["possiveis_nomes"][:3]
                    print(f"║    Nomes encontrados: {', '.join(nomes):<22} ║")
                if item.get("possiveis_emails"):
                    emails = item["possiveis_emails"][:3]
                    print(f"║    Emails: {', '.join(emails):<28} ║")
                if item.get("possiveis_telefones"):
                    tels = item["possiveis_telefones"][:3]
                    print(f"║    Telefones: {', '.join(tels):<24} ║")
                if item.get("url"):
                    print(f"║    URL: {str(item['url'])[:20]:<31} ║")
            
            # Se for dados de vazamento
            elif item.get("status") == "VAZADO":
                print(f"║ {i}. {fonte:<15}: STATUS VAZADO         ║")
                print(f"║    {item.get('observacao', ''):<35} ║")
                if item.get("email"):
                    print(f"║    Email: {item['email']:<26} ║")
            
            # Se for empresas (CNPJ)
            elif "empresas" in item:
                print(f"║ {i}. {fonte:<15}: {len(item['empresas'])} empresas     ║")
                for empresa in item["empresas"][:3]:
                    nome_emp = empresa.get("nome", "")[:20]
                    print(f"║    - {nome_emp:<28} ║")
            
            # Se for resultado de redes sociais
            elif "rede" in item:
                print(f"║ {i}. {item['rede']:<15}: {item.get('status', 'Encontrado')} ║")
                print(f"║    URL: {str(item.get('url', ''))[:20]:<31} ║")
            
            # Dados de PDFs
            elif "quantidade" in item:
                print(f"║ {i}. {fonte:<15}: {item['quantidade']} PDFs encontrados ║")
                if item.get("links"):
                    print(f"║    Links: {str(item['links'][0])[:20]:<31} ║")
            
            # Dados de Google Dorks
            elif "dork" in item:
                print(f"║ {i}. {fonte:<15}: {item['dork'][:20]} ║")
                print(f"║    URL: {str(item.get('url', ''))[:20]:<31} ║")
            
            # Dados genéricos
            else:
                # Mostra todos os campos do dicionário
                campos_mostrados = 0
                print(f"║ {i}. {fonte:<15}                             ║")
                for chave, valor in item.items():
                    if chave != "fonte" and valor and str(valor) != "None":
                        valor_str = str(valor)
                        if len(valor_str) > 20:
                            valor_str = valor_str[:17] + "..."
                        if campos_mostrados < 5:  # Limita a 5 campos para não poluir
                            print(f"║    {chave}: {valor_str:<24} ║")
                            campos_mostrados += 1
                if campos_mostrados == 0:
                    print(f"║    {str(item)[:30]:<35} ║")
        else:
            # Se for uma lista de strings ou outro tipo
            print(f"║ {i}. {str(item)[:35]:<35} ║")
        
        print("║                                          ║")
    
    print("╚══════════════════════════════════════════╝")


def consulta_cpf():
    print("\n╔══════════════════════════════════════════╗")
    print("║              CONSULTA CPF               ║")
    print("║           BUSCA COMPLETA               ║")
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
    print("\n[~] Buscando em TODAS as fontes disponíveis...")
    print("[~] Isso pode levar alguns segundos...\n")

    cpf_limpo = limpar_cpf(cpf)
    dados_completos = None
    dados_parciais = []
    fontes_tentadas = []
    fontes_com_resultado = []
    
    # Lista completa de fontes
    fontes = [
        ("BrasilAPI", lambda: fonte_brasilapi(cpf_limpo)),
        ("ReceitaWS", lambda: fonte_receitaws(cpf_limpo)),
        ("4Devs", lambda: fonte_4devs(cpf_limpo, nascimento)),
        ("CPFReais", lambda: fonte_cpfreais(cpf_limpo)),
        ("Havell", lambda: fonte_havell(cpf_limpo)),
        ("LeakCheck", lambda: fonte_leakcheck(cpf_limpo)),
        ("DeHashed", lambda: fonte_dehashed(cpf_limpo)),
        ("HIBP", lambda: fonte_hibp(cpf_limpo)),
        ("Scraping", lambda: fonte_scraping_publico(cpf_limpo)),
        ("TSE", lambda: fonte_tse(cpf_limpo)),
        ("CNPJA", lambda: fonte_cnpj_socios(cpf_limpo)),
        ("GoogleDorks", lambda: fonte_google_dorks(cpf_limpo)),
        ("PDFsPublicos", lambda: fonte_pdfs_publicos(cpf_limpo)),
        ("RedesSociais", lambda: fonte_redes_sociais(cpf_limpo))
    ]
    
    print("[~] Testando fontes:")
    
    for nome_fonte, funcao in fontes:
        print(f"[~] {nome_fonte}...", end="")
        try:
            resultado = funcao()
            fontes_tentadas.append(nome_fonte)
            
            if resultado:
                # Se for lista de resultados
                if isinstance(resultado, list):
                    for item in resultado:
                        dados_parciais.append(item)
                    fontes_com_resultado.append(nome_fonte)
                    print(" ✓ ENCONTRADO")
                # Se for dicionário com dados
                elif isinstance(resultado, dict):
                    # Verifica se tem nome (dados completos)
                    if resultado.get("nome") and len(str(resultado.get("nome"))) > 3:
                        # Se já tem dados completos, compara qual tem mais campos
                        if not dados_completos or len(resultado.keys()) > len(dados_completos.keys()):
                            dados_completos = resultado
                        fontes_com_resultado.append(nome_fonte)
                        print(" ✓ DADOS COMPLETOS")
                    else:
                        # Dados parciais
                        dados_parciais.append(resultado)
                        fontes_com_resultado.append(nome_fonte)
                        print(" ✓ DADOS PARCIAIS")
                else:
                    print(" ✗ Sem dados")
            else:
                print(" ✗ Sem dados")
        except Exception as e:
            print(f" ✗ Erro")
        
        time.sleep(0.3)
    
    # EXIBE TODOS OS RESULTADOS
    if dados_completos:
        exibir_dados_completos(dados_completos, cpf_limpo)
    
    if dados_parciais:
        exibir_dados_parciais(dados_parciais)
    
    # Se não encontrou nada
    if not dados_completos and not dados_parciais:
        print("\n[!] NENHUM DADO ENCONTRADO EM NENHUMA FONTE!")
        print(f"[i] Fontes consultadas: {len(fontes_tentadas)}")
        
        print("\n╔══════════════════════════════════════════╗")
        print("║           APENAS VALIDAÇÃO LOCAL       ║")
        print("╠══════════════════════════════════════════╣")
        print(f"║ CPF: {mascarar_cpf(cpf):<32} ║")
        print(f"║ Nascimento: {nascimento:<23} ║")
        print("║ Status: CPF E DATA VÁLIDOS             ║")
        print("╚══════════════════════════════════════════╝")
        
        print("\n[i] Motivos da falha:")
        print("    1. APIs gratuitas com limite diário atingido")
        print("    2. CPF não está em bases públicas/vazamentos")
        print("    3. Servidores temporariamente offline")
        print("    4. Configuração de rede bloqueando acesso")
        
        print("\n[i] Sugestões:")
        print("    1. Tente novamente em alguns minutos")
        print("    2. Use um serviço pago para mais dados")
        print("    3. Verifique sua conexão com a internet")
    else:
        print("\n[~] RESUMO DA BUSCA:")
        print(f"    Total de fontes consultadas: {len(fontes_tentadas)}")
        print(f"    Fontes com resultados: {len(fontes_com_resultado)}")
        if fontes_com_resultado:
            print(f"    Fontes: {', '.join(fontes_com_resultado[:5])}")
            if len(fontes_com_resultado) > 5:
                print(f"    ... e mais {len(fontes_com_resultado)-5} fontes")
    
    # Mostra sugestões de busca manual
    print("\n[i] Links úteis para busca manual:")
    print("    - https://www.google.com/search?q=" + cpf_limpo)
    print("    - https://www.bing.com/search?q=" + cpf_limpo)
    print("    - https://www.receitaws.com.br/")
    print("    - https://www.4devs.com.br/validar_cpf")


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