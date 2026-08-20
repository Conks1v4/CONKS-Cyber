import urllib.request
import urllib.error
import json
import re
import subprocess
import webbrowser
from datetime import datetime
import requests
import os
import sqlite3
import hashlib
import base64

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
# CPF - SEM API
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


# ==========================================
# MÉTODO 1: Busca em arquivos locais
# ==========================================

def buscar_em_arquivos_locais(cpf_limpo):
    """Busca o CPF em arquivos de texto locais"""
    try:
        # Cria um arquivo de exemplo se não existir
        if not os.path.exists("bases_cpf.txt"):
            with open("bases_cpf.txt", "w", encoding="utf-8") as f:
                f.write("# Arquivo de bases de CPF\n")
                f.write("# Formato: CPF;NOME;DATA_NASC;MAE;PAI\n")
                f.write("# Exemplo: 12345678901;João Silva;01/01/1990;Maria Silva;José Silva\n")
        
        with open("bases_cpf.txt", "r", encoding="utf-8") as f:
            for linha in f:
                if cpf_limpo in linha and not linha.startswith("#"):
                    partes = linha.strip().split(";")
                    if len(partes) >= 3:
                        return {
                            "nome": partes[1] if len(partes) > 1 else None,
                            "data_nascimento": partes[2] if len(partes) > 2 else None,
                            "nome_mae": partes[3] if len(partes) > 3 else None,
                            "nome_pai": partes[4] if len(partes) > 4 else None,
                            "fonte": "Arquivo Local"
                        }
    except:
        pass
    return None


# ==========================================
# MÉTODO 2: Busca em banco SQLite local
# ==========================================

def buscar_em_banco_local(cpf_limpo):
    """Busca CPF em banco de dados SQLite local"""
    try:
        db_path = "bases_cpf.db"
        
        # Cria banco se não existir
        if not os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cpfs (
                    cpf TEXT PRIMARY KEY,
                    nome TEXT,
                    data_nasc TEXT,
                    mae TEXT,
                    pai TEXT,
                    fonte TEXT
                )
            """)
            conn.commit()
            conn.close()
        
        # Busca no banco
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cpfs WHERE cpf = ?", (cpf_limpo,))
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado:
            return {
                "nome": resultado[1] if len(resultado) > 1 else None,
                "data_nascimento": resultado[2] if len(resultado) > 2 else None,
                "nome_mae": resultado[3] if len(resultado) > 3 else None,
                "nome_pai": resultado[4] if len(resultado) > 4 else None,
                "fonte": resultado[5] if len(resultado) > 5 else "Banco Local"
            }
    except:
        pass
    return None


# ==========================================
# MÉTODO 3: Scraping em sites públicos
# ==========================================

def buscar_scraping_sites(cpf_limpo):
    """Faz scraping em sites públicos para encontrar dados do CPF"""
    try:
        sites = [
            f"https://www.google.com/search?q={cpf_limpo}+cpf+nome",
            f"https://www.bing.com/search?q={cpf_limpo}+cpf+nome",
            f"https://duckduckgo.com/html/?q={cpf_limpo}+cpf+nome"
        ]
        
        for url in sites:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                html = response.text
                
                # Procura por padrões de nome completo
                nomes = re.findall(r'[A-Z][a-záéíóúãõç]+ [A-Z][a-záéíóúãõç]+(?: [A-Z][a-záéíóúãõç]+)?', html)
                
                # Procura por datas
                datas = re.findall(r'\d{2}/\d{2}/\d{4}', html)
                
                # Procura por emails
                emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)
                
                if nomes or datas or emails:
                    return {
                        "possiveis_nomes": nomes[:5] if nomes else [],
                        "possiveis_datas": datas[:5] if datas else [],
                        "possiveis_emails": emails[:5] if emails else [],
                        "fonte": "Scraping",
                        "url": url
                    }
    except:
        pass
    return None


# ==========================================
# MÉTODO 4: Busca em arquivos PDF públicos
# ==========================================

def buscar_em_pdfs(cpf_limpo):
    """Busca CPF em arquivos PDF indexados"""
    try:
        # Simula busca em PDFs públicos
        pdf_sites = [
            f"https://www.google.com/search?q={cpf_limpo}+filetype:pdf",
            f"https://www.bing.com/search?q={cpf_limpo}+filetype:pdf"
        ]
        
        for url in pdf_sites:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Procura por links de PDF
                pdf_links = re.findall(r'https?://[^\s"]+\.pdf', response.text)
                if pdf_links:
                    return {
                        "quantidade": len(pdf_links),
                        "links": pdf_links[:3],
                        "fonte": "PDFs Públicos"
                    }
    except:
        pass
    return None


# ==========================================
# MÉTODO 5: Busca em fóruns e sites de discussão
# ==========================================

def buscar_em_foruns(cpf_limpo):
    """Busca CPF em fóruns públicos"""
    try:
        foruns = [
            f"https://www.reddit.com/search/?q={cpf_limpo}",
            f"https://www.quora.com/search?q={cpf_limpo}",
            f"https://stackoverflow.com/search?q={cpf_limpo}"
        ]
        
        for url in foruns:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Procura por padrões de texto
                texto = response.text
                if cpf_limpo in texto:
                    # Extrai contexto ao redor do CPF
                    pos = texto.find(cpf_limpo)
                    inicio = max(0, pos - 200)
                    fim = min(len(texto), pos + 200)
                    contexto = texto[inicio:fim]
                    
                    # Procura por nomes no contexto
                    nomes = re.findall(r'[A-Z][a-záéíóúãõç]+ [A-Z][a-záéíóúãõç]+', contexto)
                    
                    return {
                        "contexto": contexto[:200],
                        "possiveis_nomes": nomes[:3] if nomes else [],
                        "fonte": "Fóruns Públicos",
                        "url": url
                    }
    except:
        pass
    return None


# ==========================================
# MÉTODO 6: Busca em dados vazados (arquivos locais)
# ==========================================

def buscar_dados_vazados(cpf_limpo):
    """Busca em arquivos de dados vazados locais"""
    try:
        # Verifica se existe arquivo de dados vazados
        arquivos = ["vazados.txt", "leaks.txt", "dados_publicos.txt"]
        
        for arquivo in arquivos:
            if os.path.exists(arquivo):
                with open(arquivo, "r", encoding="utf-8", errors="ignore") as f:
                    for linha in f:
                        if cpf_limpo in linha:
                            # Tenta extrair informações da linha
                            partes = linha.strip().split(";")
                            if len(partes) >= 3:
                                return {
                                    "nome": partes[1] if len(partes) > 1 else None,
                                    "data_nascimento": partes[2] if len(partes) > 2 else None,
                                    "email": partes[3] if len(partes) > 3 else None,
                                    "senha": partes[4] if len(partes) > 4 else None,
                                    "fonte": f"Dados Vazados ({arquivo})"
                                }
    except:
        pass
    return None


# ==========================================
# MÉTODO 7: Busca em sites de transparência
# ==========================================

def buscar_sites_transparencia(cpf_limpo):
    """Busca em sites de transparência pública"""
    try:
        # Sites de transparência (exemplos)
        sites_transparencia = [
            "https://www.portaltransparencia.gov.br/",
            "https://transparencia.tse.jus.br/",
            "https://transparencia.gov.br/"
        ]
        
        for site in sites_transparencia:
            url = f"{site}busca?q={cpf_limpo}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                html = response.text
                # Procura por padrões de nome
                nomes = re.findall(r'[A-Z][a-záéíóúãõç]+ [A-Z][a-záéíóúãõç]+', html)
                if nomes:
                    return {
                        "possiveis_nomes": nomes[:5],
                        "fonte": "Sites Transparência",
                        "url": url
                    }
    except:
        pass
    return None


# ==========================================
# MÉTODO 8: Busca em redes sociais via scrap
# ==========================================

def buscar_redes_sociais(cpf_limpo):
    """Busca CPF em redes sociais (perfis públicos)"""
    try:
        # Busca em perfis públicos do Facebook
        url = f"https://www.facebook.com/search/top?q={cpf_limpo}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            html = response.text
            # Procura por padrões de nomes
            nomes = re.findall(r'[A-Z][a-záéíóúãõç]+ [A-Z][a-záéíóúãõç]+', html)
            if nomes:
                return {
                    "possiveis_nomes": nomes[:5],
                    "fonte": "Redes Sociais",
                    "url": url
                }
    except:
        pass
    return None


# ==========================================
# MÉTODO 9: Busca em listas telefônicas
# ==========================================

def buscar_listas_telefonicas(cpf_limpo):
    """Busca em listas telefônicas públicas"""
    try:
        # Simula busca em lista telefônica
        lista_telefonica = """
        # Lista telefônica pública
        # Formato: NOME;TELEFONE;CPF;ENDEREÇO
        """
        
        # Procura em listas online
        url = f"https://www.paginasamarelas.com.br/busca?q={cpf_limpo}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            html = response.text
            # Extrai telefones
            telefones = re.findall(r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}', html)
            if telefones:
                return {
                    "possiveis_telefones": telefones[:5],
                    "fonte": "Listas Telefônicas"
                }
    except:
        pass
    return None


# ==========================================
# MÉTODO 10: Busca por hash do CPF
# ==========================================

def buscar_por_hash(cpf_limpo):
    """Busca o hash do CPF em bases de dados públicos"""
    try:
        # Gera hash do CPF
        hash_md5 = hashlib.md5(cpf_limpo.encode()).hexdigest()
        hash_sha1 = hashlib.sha1(cpf_limpo.encode()).hexdigest()
        
        # Busca em sites que indexam hashes
        url = f"https://md5decrypt.net/en/Sha1/{hash_sha1}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            html = response.text
            # Se encontrou correspondência
            if "found" in html.lower() or "result" in html.lower():
                return {
                    "hash_md5": hash_md5,
                    "hash_sha1": hash_sha1,
                    "fonte": "Hash Database",
                    "status": "Hash encontrado em banco de dados"
                }
    except:
        pass
    return None


def consulta_cpf():
    print("\n╔══════════════════════════════════════════╗")
    print("║              CONSULTA CPF               ║")
    print("║        BUSCA SEM API EXTERNA           ║")
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
    print("\n[~] Buscando dados SEM usar APIs externas...")
    
    cpf_limpo = limpar_cpf(cpf)
    dados_encontrados = None
    todas_informacoes = []
    
    # ==========================================
    # MÉTODO 1: Arquivos locais
    # ==========================================
    print("\n[~] Buscando em arquivos locais...")
    resultado = buscar_em_arquivos_locais(cpf_limpo)
    if resultado:
        dados_encontrados = resultado
        print("[+] Dados encontrados em arquivos locais!")
    
    # ==========================================
    # MÉTODO 2: Banco SQLite
    # ==========================================
    if not dados_encontrados:
        print("\n[~] Buscando em banco de dados local...")
        resultado = buscar_em_banco_local(cpf_limpo)
        if resultado:
            dados_encontrados = resultado
            print("[+] Dados encontrados no banco de dados!")
    
    # ==========================================
    # MÉTODO 3: Scraping sites públicos
    # ==========================================
    if not dados_encontrados:
        print("\n[~] Buscando em sites públicos (Scraping)...")
        resultado = buscar_scraping_sites(cpf_limpo)
        if resultado:
            todas_informacoes.append(resultado)
            print("[+] Informações encontradas via scraping!")
    
    # ==========================================
    # MÉTODO 4: PDFs públicos
    # ==========================================
    if not dados_encontrados:
        print("\n[~] Buscando em PDFs públicos...")
        resultado = buscar_em_pdfs(cpf_limpo)
        if resultado:
            todas_informacoes.append(resultado)
            print("[+] PDFs encontrados contendo o CPF!")
    
    # ==========================================
    # MÉTODO 5: Fóruns
    # ==========================================
    if not dados_encontrados:
        print("\n[~] Buscando em fóruns públicos...")
        resultado = buscar_em_foruns(cpf_limpo)
        if resultado:
            todas_informacoes.append(resultado)
            print("[+] Informações encontradas em fóruns!")
    
    # ==========================================
    # MÉTODO 6: Dados vazados
    # ==========================================
    if not dados_encontrados:
        print("\n[~] Buscando em dados vazados locais...")
        resultado = buscar_dados_vazados(cpf_limpo)
        if resultado:
            dados_encontrados = resultado
            print("[+] Dados encontrados em vazamentos!")
    
    # ==========================================
    # MÉTODO 7: Transparência
    # ==========================================
    if not dados_encontrados:
        print("\n[~] Buscando em sites de transparência...")
        resultado = buscar_sites_transparencia(cpf_limpo)
        if resultado:
            todas_informacoes.append(resultado)
            print("[+] Informações encontradas em sites de transparência!")
    
    # ==========================================
    # MÉTODO 8: Redes sociais
    # ==========================================
    if not dados_encontrados:
        print("\n[~] Buscando em redes sociais...")
        resultado = buscar_redes_sociais(cpf_limpo)
        if resultado:
            todas_informacoes.append(resultado)
            print("[+] Informações encontradas em redes sociais!")
    
    # ==========================================
    # MÉTODO 9: Listas telefônicas
    # ==========================================
    if not dados_encontrados:
        print("\n[~] Buscando em listas telefônicas...")
        resultado = buscar_listas_telefonicas(cpf_limpo)
        if resultado:
            todas_informacoes.append(resultado)
            print("[+] Telefones encontrados em listas!")
    
    # ==========================================
    # MÉTODO 10: Hash
    # ==========================================
    if not dados_encontrados:
        print("\n[~] Buscando hash do CPF...")
        resultado = buscar_por_hash(cpf_limpo)
        if resultado:
            todas_informacoes.append(resultado)
            print("[+] Hash encontrado em bancos de dados!")
    
    # ==========================================
    # EXIBE RESULTADOS
    # ==========================================
    if dados_encontrados:
        print("\n[+] DADOS COMPLETOS ENCONTRADOS!")
        print("="*50)
        print("\n╔══════════════════════════════════════════╗")
        print("║           RESULTADO DA BUSCA            ║")
        print("╠══════════════════════════════════════════╣")
        
        campos = [
            ("CPF", cpf_limpo),
            ("Nome", dados_encontrados.get("nome")),
            ("Data Nascimento", dados_encontrados.get("data_nascimento")),
            ("Nome da Mãe", dados_encontrados.get("nome_mae")),
            ("Nome do Pai", dados_encontrados.get("nome_pai")),
            ("Email", dados_encontrados.get("email")),
            ("Telefone", dados_encontrados.get("telefone")),
            ("Fonte", dados_encontrados.get("fonte"))
        ]
        
        for nome, valor in campos:
            if valor is not None and valor != "" and str(valor) != "None":
                print(f"║ {nome:<18}: {str(valor):<20} ║")
        
        print("╚══════════════════════════════════════════╝")
    
    # Mostra informações parciais
    if todas_informacoes:
        print("\n[+] INFORMAÇÕES PARCIAIS ENCONTRADAS:")
        print("="*50)
        print("\n╔══════════════════════════════════════════╗")
        print("║         INFORMAÇÕES ADICIONAIS          ║")
        print("╠══════════════════════════════════════════╣")
        
        for info in todas_informacoes:
            fonte = info.get("fonte", "Desconhecida")
            print(f"║ {fonte}:                                ║")
            
            if info.get("possiveis_nomes"):
                nomes = ", ".join(info["possiveis_nomes"][:3])
                print(f"║    Nomes: {nomes[:25]:<25} ║")
            
            if info.get("possiveis_emails"):
                emails = ", ".join(info["possiveis_emails"][:3])
                print(f"║    Emails: {emails[:25]:<25} ║")
            
            if info.get("possiveis_telefones"):
                tels = ", ".join(info["possiveis_telefones"][:3])
                print(f"║    Telefones: {tels[:25]:<25} ║")
            
            if info.get("quantidade"):
                print(f"║    Quantidade: {info['quantidade']:>22} ║")
            
            if info.get("url"):
                url = info["url"][:25]
                print(f"║    URL: {url:<25} ║")
            
            print("║                                          ║")
        
        print("╚══════════════════════════════════════════╝")
    
    # Se não encontrou nada
    if not dados_encontrados and not todas_informacoes:
        print("\n[!] NENHUM DADO ENCONTRADO!")
        print("\n╔══════════════════════════════════════════╗")
        print("║           VALIDAÇÃO LOCAL               ║")
        print("╠══════════════════════════════════════════╣")
        print(f"║ CPF: {mascarar_cpf(cpf):<32} ║")
        print(f"║ Nascimento: {nascimento:<23} ║")
        print("║ Status: CPF e Data válidos              ║")
        print("╚══════════════════════════════════════════╝")
        
        print("\n[i] Como adicionar dados manualmente:")
        print("    1. Crie um arquivo 'bases_cpf.txt'")
        print("    2. Adicione linhas no formato:")
        print("       CPF;NOME;DATA_NASC;MAE;PAI")
        print("    3. Exemplo: 12345678901;João Silva;01/01/1990;Maria Silva;José Silva")
        print("\n[i] Ou crie um banco SQLite com a tabela 'cpfs'")
    else:
        print("\n[~] RESUMO DA BUSCA:")
        print(f"    Dados completos: {'SIM' if dados_encontrados else 'NÃO'}")
        print(f"    Informações parciais: {len(todas_informacoes)}")
        if dados_encontrados:
            print(f"    Fonte principal: {dados_encontrados.get('fonte', 'Desconhecida')}")


# ==========================================
# FUNÇÃO PARA ADICIONAR DADOS AO BANCO LOCAL
# ==========================================

def adicionar_cpf_ao_banco(cpf, nome, data_nasc, mae="", pai=""):
    """Adiciona um CPF ao banco de dados local"""
    try:
        cpf_limpo = limpar_cpf(cpf)
        
        # Adiciona ao arquivo texto
        with open("bases_cpf.txt", "a", encoding="utf-8") as f:
            f.write(f"{cpf_limpo};{nome};{data_nasc};{mae};{pai}\n")
        
        # Adiciona ao SQLite
        conn = sqlite3.connect("bases_cpf.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO cpfs (cpf, nome, data_nasc, mae, pai, fonte)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (cpf_limpo, nome, data_nasc, mae, pai, "Adicionado Manualmente"))
        conn.commit()
        conn.close()
        
        print(f"[+] CPF {cpf_limpo} adicionado ao banco local!")
        return True
    except Exception as e:
        print(f"[-] Erro ao adicionar: {str(e)}")
        return False


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