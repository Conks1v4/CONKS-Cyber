import re
import ipaddress
import uuid


def limpar_numeros(valor):
    return re.sub(r"\D", "", valor)


def validar_cpf(cpf):
    cpf = limpar_numeros(cpf)

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    numeros = [int(x) for x in cpf]

    soma = sum(numeros[i] * (10 - i) for i in range(9))
    digito1 = (soma * 10) % 11

    if digito1 == 10:
        digito1 = 0

    if digito1 != numeros[9]:
        return False

    soma = sum(numeros[i] * (11 - i) for i in range(10))
    digito2 = (soma * 10) % 11

    if digito2 == 10:
        digito2 = 0

    return digito2 == numeros[10]


def calcular_cnpj_digito(numeros, pesos):
    soma = sum(
        numero * peso
        for numero, peso in zip(numeros, pesos)
    )

    resto = soma % 11

    if resto < 2:
        return 0

    return 11 - resto


def validar_cnpj(cnpj):
    cnpj = limpar_numeros(cnpj)

    if len(cnpj) != 14:
        return False

    if cnpj == cnpj[0] * 14:
        return False

    numeros = [int(x) for x in cnpj]

    primeiro = calcular_cnpj_digito(
        numeros[:12],
        [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    )

    if primeiro != numeros[12]:
        return False

    segundo = calcular_cnpj_digito(
        numeros[:13],
        [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    )

    return segundo == numeros[13]


def validar_ip(ip):
    try:
        ipaddress.ip_address(ip.strip())
        return True
    except ValueError:
        return False


def validar_uuid(valor):
    try:
        uuid.UUID(valor.strip())
        return True
    except (ValueError, AttributeError):
        return False