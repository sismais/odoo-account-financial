"""
Biblitoeca de funções proprias diversas em Python, a serem usadas no projeto.
"""


def caracteres_rm(num):
    """
    Função remover caracteres da string passada por parametro. Inicialmente possui apenas caracteres que compoem numero
    de telefones, mas conforme a necessidade, só acrescentar na variavel caracteres_rm.
    """
    caracteres_rm = '() -'  # Caracteres a remover da string passada na função, incrementear se necessário

    if num:
        for n in caracteres_rm:
            num = num.replace(n, '')

        return num

    return None



