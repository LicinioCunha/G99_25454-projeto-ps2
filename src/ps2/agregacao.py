"""Agregação de dados (ETAPA 6 da aula).

Depois de ler e validar, agrupamos a informação para o dashboard: totais por
mês, por cliente (NIB), evolução temporal, etc. Usam-se dicionários e funções
de ordem superior, no espírito do paradigma funcional.
"""
from __future__ import annotations
from collections import defaultdict
from functools import reduce
from .modelo import Ficheiro
from .validacao import valida_nif, valida_nib


def periodo(fich: Ficheiro) -> str:
    """Devolve o período AAAA-MM a partir da data do cabeçalho."""
    d = fich.inicio.data
    return f"{d[0:4]}-{d[4:6]}"


def total_por_mes(ficheiros: list[Ficheiro]) -> dict[str, float]:
    """Soma da importância (em euros) por período AAAA-MM, ordenado por chave."""
    acc: dict[str, float] = defaultdict(float)
    for f in ficheiros:
        acc[periodo(f)] += f.inicio.total_cent / 100
    return dict(sorted(acc.items()))


def total_por_cliente(ficheiros: list[Ficheiro]) -> dict[str, float]:
    """Soma da importância (em euros) por NIB de cliente, em todo o período."""
    movimentos = (m for f in ficheiros for m in f.movimentos)
    return dict(sorted(
        reduce(
            lambda acc, m: {**acc, m.nib: acc.get(m.nib, 0.0) + m.importancia_cent / 100},
            movimentos, {},
        ).items()
    ))


def serie_cliente(ficheiros: list[Ficheiro], nib: str) -> dict[str, float]:
    """Evolução mensal (AAAA-MM -> euros) de um único cliente (NIB)."""
    acc: dict[str, float] = defaultdict(float)
    for f in ficheiros:
        for m in f.movimentos:
            if m.nib == nib:
                acc[periodo(f)] += m.importancia_cent / 100
    return dict(sorted(acc.items()))


def clientes(ficheiros: list[Ficheiro]) -> list[str]:
    """Lista ordenada de NIBs distintos presentes nos ficheiros."""
    return sorted({m.nib for f in ficheiros for m in f.movimentos})


def resumo_alertas(ficheiros: list[Ficheiro]) -> list[dict]:
    """Funcionalidade própria: resumo de alertas de NIF/NIB por ficheiro.

    Para cada ficheiro, indica o período, se o NIF do ordenante é válido, e
    quantos dos NIBs de cliente (movimentos tipo 2) falham a validação do
    Anexo B. Serve de base à vista "Alertas de Validação" do dashboard.
    """
    return [
        {
            "periodo": periodo(f),
            "nif": f.inicio.nif,
            "nif_valido": valida_nif(f.inicio.nif),
            "n_movimentos": len(f.movimentos),
            "n_nibs_invalidos": sum(1 for m in f.movimentos if not valida_nib(m.nib)),
        }
        for f in ficheiros
    ]
