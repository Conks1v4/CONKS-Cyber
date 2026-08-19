import os
import random
from datetime import date, timedelta


# ==========================================
# DIRETÓRIOS
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)


# ==========================================
# CARREGAR NOMES
# ==========================================

def carregar_lista(nome_arquivo):

    caminho = os.path.join(
        DATA_DIR,
        nome_arquivo
    )

    try:

        with open(
            caminho,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return [
                linha.strip()
                for linha in arquivo
                if linha.strip()
            ]

    except (
        FileNotFoundError,
        OSError,
        UnicodeError
    ):

        return []


# ==========================================
# NOMES
# ==========================================

def gerar_nome():

    nomes = carregar_lista("names.txt")

    if not nomes:
        return "Pessoa"

    return random.choice(nomes)


def gerar_sobrenome():

    sobrenomes = carregar_lista(
        "surnames.txt"
    )

    if not sobrenomes:
        return "Sobrenome"

    return random.choice(
        sobrenomes
    )


def gerar_nome_completo():

    return (
        gerar_nome()
        + " "
        + gerar_sobrenome()
    )


# ==========================================
# DATA DE NASCIMENTO
# ==========================================

def gerar_data_nascimento(
    idade_minima=18,
    idade_maxima=80
):

    hoje = date.today()

    data_maxima = (
        hoje -
        timedelta(
            days=idade_minima * 365
        )
    )

    data_minima = (
        hoje -
        timedelta(
            days=idade_maxima * 365
        )
    )

    intervalo = (
        data_maxima -
        data_minima
    ).days

    nascimento = (
        data_minima +
        timedelta(
            days=random.randint(
                0,
                intervalo
            )
        )
    )

    return nascimento.strftime(
        "%d/%m/%Y"
    )


# ==========================================
# IDENTIFICADOR NUMÉRICO DE TESTE
# ==========================================

def gerar_numero_teste(
    quantidade
):

    return "".join(
        str(random.randint(0, 9))
        for _ in range(quantidade)
    )


# ==========================================
# CPF FICTÍCIO
# ==========================================

def gerar_cpf_teste():

    # 11 dígitos numéricos.
    # Mantido como dado fictício e marcado
    # como TESTE na apresentação.

    numero = gerar_numero_teste(11)

    return numero


def formatar_cpf_teste(cpf):

    cpf = str(cpf).zfill(11)

    return (
        f"{cpf[:3]}."
        f"{cpf[3:6]}."
        f"{cpf[6:9]}-"
        f"{cpf[9:]}"
    )


# ==========================================
# CNPJ FICTÍCIO
# ==========================================

def gerar_cnpj_teste():

    # 14 dígitos numéricos fictícios.

    return gerar_numero_teste(14)


def formatar_cnpj_teste(cnpj):

    cnpj = str(cnpj).zfill(14)

    return (
        f"{cnpj[:2]}."
        f"{cnpj[2:5]}."
        f"{cnpj[5:8]}/"
        f"{cnpj[8:12]}-"
        f"{cnpj[12:]}"
    )


# ==========================================
# RG FICTÍCIO
# ==========================================

def gerar_rg_teste():

    # RG fictício com 9 posições numéricas.

    return gerar_numero_teste(9)


def formatar_rg_teste(rg):

    rg = str(rg).zfill(9)

    return (
        f"{rg[:2]}."
        f"{rg[2:5]}."
        f"{rg[5:8]}-"
        f"{rg[8]}"
    )


# ==========================================
# DATA DE EMISSÃO
# ==========================================

def gerar_data_emissao(
    nascimento
):

    try:

        dia, mes, ano = map(
            int,
            nascimento.split("/")
        )

        nascimento_data = date(
            ano,
            mes,
            dia
        )

    except (
        ValueError,
        TypeError
    ):

        return date.today().strftime(
            "%d/%m/%Y"
        )

    hoje = date.today()

    idade_18 = (
        nascimento_data +
        timedelta(
            days=18 * 365
        )
    )

    if idade_18 > hoje:
        idade_18 = hoje

    intervalo = (
        hoje - idade_18
    ).days

    if intervalo <= 0:

        emissao = hoje

    else:

        emissao = (
            idade_18 +
            timedelta(
                days=random.randint(
                    0,
                    intervalo
                )
            )
        )

    return emissao.strftime(
        "%d/%m/%Y"
    )


# ==========================================
# IDENTIDADE FICTÍCIA
# ==========================================

def gerar_identidade_teste():

    nome = gerar_nome_completo()

    nascimento = gerar_data_nascimento()

    emissao = gerar_data_emissao(
        nascimento
    )

    cpf = gerar_cpf_teste()

    rg = gerar_rg_teste()

    estados = [
        ("ES", "Espírito Santo"),
        ("SP", "São Paulo"),
        ("RJ", "Rio de Janeiro"),
        ("MG", "Minas Gerais"),
        ("PR", "Paraná"),
        ("SC", "Santa Catarina"),
        ("BA", "Bahia"),
        ("GO", "Goiás"),
        ("PE", "Pernambuco")
    ]

    uf, estado = random.choice(
        estados
    )

    sexo = random.choice(
        [
            "Masculino",
            "Feminino"
        ]
    )

    return {
        "nome": nome,
        "nascimento": nascimento,
        "cpf": cpf,
        "rg": rg,
        "emissao": emissao,
        "sexo": sexo,
        "uf": uf,
        "estado": estado,
        "nacionalidade": "Brasileira"
    }


# ==========================================
# EXIBIR IDENTIDADE
# ==========================================

def mostrar_identidade_teste():

    dados = gerar_identidade_teste()

    cpf = formatar_cpf_teste(
        dados["cpf"]
    )

    rg = formatar_rg_teste(
        dados["rg"]
    )

    print(
        "\n╔══════════════════════════════════════════╗"
    )

    print(
        "║           IDENTIDADE FICTÍCIA           ║"
    )

    print(
        "╠══════════════════════════════════════════╣"
    )

    print(
        f"║ Nome: {dados['nome']:<33} ║"
    )

    print(
        f"║ Nascimento: "
        f"{dados['nascimento']:<25} ║"
    )

    print(
        f"║ CPF TESTE: "
        f"{cpf:<25} ║"
    )

    print(
        f"║ RG TESTE: "
        f"{rg:<26} ║"
    )

    print(
        f"║ Emissão: "
        f"{dados['emissao']:<27} ║"
    )

    print(
        f"║ Sexo: "
        f"{dados['sexo']:<30} ║"
    )

    print(
        f"║ UF: "
        f"{dados['uf']:<33} ║"
    )

    print(
        f"║ Estado: "
        f"{dados['estado']:<29} ║"
    )

    print(
        f"║ Nacionalidade: "
        f"{dados['nacionalidade']:<23} ║"
    )

    print(
        "╠══════════════════════════════════════════╣"
    )

    print(
        "║       DADOS FICTÍCIOS / TESTE           ║"
    )

    print(
        "║       NÃO É DOCUMENTO OFICIAL           ║"
    )

    print(
        "╚══════════════════════════════════════════╝"
    )


# ==========================================
# MENU
# ==========================================

def menu_geradores():

    while True:

        print(
            "\n╔══════════════════════════════════════╗"
        )

        print(
            "║              GERADORES              ║"
        )

        print(
            "╠══════════════════════════════════════╣"
        )

        print(
            "║ [1] Gerar CPF de teste              ║"
        )

        print(
            "║ [2] Gerar CNPJ de teste             ║"
        )

        print(
            "║ [3] Gerar identidade de teste       ║"
        )

        print(
            "║ [0] Voltar                           ║"
        )

        print(
            "╚══════════════════════════════════════╝"
        )

        opcao = input(
            "\nCONKS@Geradores > "
        ).strip()

        if opcao == "1":

            cpf = gerar_cpf_teste()

            print(
                "\n[+] CPF TESTE:"
            )

            print(
                formatar_cpf_teste(cpf)
            )

        elif opcao == "2":

            cnpj = gerar_cnpj_teste()

            print(
                "\n[+] CNPJ TESTE:"
            )

            print(
                formatar_cnpj_teste(cnpj)
            )

        elif opcao == "3":

            mostrar_identidade_teste()

        elif opcao == "0":

            break

        else:

            print(
                "\n[!] Opção inválida."
            )

        if opcao != "0":

            input(
                "\nPressione ENTER para continuar..."
            )