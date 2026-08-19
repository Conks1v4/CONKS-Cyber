import socket
import urllib.request
import urllib.error
import json
import re
import ipaddress


def dominio_valido(dominio):
    dominio = dominio.strip().lower()

    if not dominio or len(dominio) > 253:
        return False

    if dominio.startswith(".") or dominio.endswith("."):
        return False

    if ".." in dominio:
        return False

    padrao = r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$"

    return bool(re.match(padrao, dominio))


def ip_valido(ip):
    try:
        ipaddress.ip_address(ip.strip())
        return True
    except ValueError:
        return False


def requisicao_json(url, timeout=5):
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
        socket.timeout,
        OSError,
        UnicodeError,
        json.JSONDecodeError
    ):
        return None


def consultar_ip_publico():
    dados = requisicao_json(
        "https://ipwho.is/",
        timeout=5
    )

    if not dados or not dados.get("success"):
        return None

    return dados.get("ip")


def consultar_ip(ip):
    ip = ip.strip()

    if not ip_valido(ip):
        return None

    dados = requisicao_json(
        f"https://ipwho.is/{ip}",
        timeout=5
    )

    if not dados or not dados.get("success"):
        return None

    return dados


def consultar_dns(dominio):
    dominio = dominio.strip().lower()

    if not dominio_valido(dominio):
        return None

    try:
        resultado = socket.gethostbyname_ex(dominio)

        return {
            "dominio": resultado[0],
            "aliases": resultado[1],
            "ips": resultado[2]
        }

    except (
        socket.gaierror,
        socket.herror,
        UnicodeError,
        OSError
    ):
        return None


def consultar_dominio(dominio):
    dominio = dominio.strip().lower()

    if not dominio_valido(dominio):
        return None

    try:
        resultado = socket.gethostbyname_ex(dominio)

        return {
            "dominio": resultado[0],
            "aliases": resultado[1],
            "ips": resultado[2]
        }

    except (
        socket.gaierror,
        socket.herror,
        UnicodeError,
        OSError
    ):
        return None


def testar_conexao():
    try:
        socket.create_connection(
            ("1.1.1.1", 53),
            timeout=5
        )

        return True

    except OSError:
        return False