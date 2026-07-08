"""Validações (ETAPA 4 da aula): estrutura do ficheiro, NIF e NIB.

Todas as funções são *puras* (não têm efeitos secundários) e devolvem
resultados simples (bool ou listas de mensagens), no espírito do paradigma
funcional.
"""
from __future__ import annotations
from datetime import datetime
from .modelo import Ficheiro


# ---------------------------------------------------------------- utilitários
def so_numeros(txt: str) -> bool:
    """True se ``txt`` contém apenas dígitos."""
    return txt.isdigit()


def data_valida(txt: str) -> bool:
    """True se ``txt`` é uma data no formato AAAAMMDD."""
    try:
        datetime.strptime(txt, "%Y%m%d")
        return True
    except ValueError:
        return False


# ------------------------------------------------------------------- NIF / NIB
def valida_nif(nif: str) -> bool:
    """Valida um NIF português (Anexo A do enunciado).

    Regras: 9 dígitos, primeiro dígito em ``{1,2,5,6,8,9}`` e dígito de
    controlo (9º) coerente com o resto da soma ponderada módulo 11.
    """
    if len(nif) != 9 or not nif.isdigit():
        return False
    if nif[0] not in "125689":
        return False
    soma = sum(int(nif[i]) * (9 - i) for i in range(8))
    resto = soma % 11
    controlo = 0 if resto in (0, 1) else 11 - resto
    return controlo == int(nif[8])


def valida_nib(nib: str) -> bool:
    """Valida um NIB pela regra do Anexo B: 21 dígitos e ``int(nib) % 97 == 1``.

    NOTA: com os dados fornecidos, esta regra literal marca todos os NIBs como
    inválidos (o próprio exemplo do Anexo B não satisfaz ``% 97 == 1``).
    Confirmar o algoritmo pretendido com o docente.
    """
    return len(nib) == 21 and nib.isdigit() and int(nib) % 97 == 1


# --------------------------------------------------------------- estrutura
def valida_estrutura(nome: str, linhas: list[str]) -> list[str]:
    """Valida a estrutura de um ficheiro PS2 e devolve a lista de erros.

    Lista vazia significa ficheiro estruturalmente válido. Verifica:
    ordem dos registos (1 … 2+ … 9), a data do cabeçalho, e a coerência
    entre o cabeçalho, os movimentos e o totalizador.
    """
    erros: list[str] = []
    if len(linhas) < 3:
        return [f"{nome}: ficheiro tem menos de 3 registos"]
    if linhas[0][:1] != "1":
        erros.append(f"{nome}: primeira linha não é registo tipo 1")
    if linhas[-1][:1] != "9":
        erros.append(f"{nome}: última linha não é registo tipo 9")
    if any(l[:1] != "2" for l in linhas[1:-1]):
        erros.append(f"{nome}: existem registos de detalhe que não são tipo 2")

    data = linhas[0][1:9]
    if not data_valida(data):
        erros.append(f"{nome}: data de processamento inválida ({data})")

    # coerência de totais e contagem
    movimentos = linhas[1:-1]
    try:
        soma = sum(int(l[41:55]) for l in movimentos)
        total_cab = int(linhas[0][-20:-6])
        total_fim = int(linhas[-1][1:15])
        n_fim = int(linhas[-1][15:21])
        if not (soma == total_cab == total_fim):
            erros.append(
                f"{nome}: totais não coincidem "
                f"(detalhe={soma}, cabeçalho={total_cab}, fim={total_fim})"
            )
        if not (len(movimentos) == n_fim):
            erros.append(
                f"{nome}: nº de registos difere "
                f"(reais={len(movimentos)}, declarado={n_fim})"
            )
    except ValueError:
        erros.append(f"{nome}: campos numéricos malformados")

    return erros


def valida_ficheiro(fich: Ficheiro) -> list[str]:
    """Valida NIF do ordenante e NIBs dos clientes de um :class:`Ficheiro`."""
    erros: list[str] = []
    if not valida_nif(fich.inicio.nif):
        erros.append(f"{fich.nome}: NIF do ordenante inválido ({fich.inicio.nif})")
    for m in fich.movimentos:
        if not valida_nib(m.nib):
            erros.append(f"{fich.nome}: NIB inválido ({m.nib}) [{m.descricao}]")
    return erros
