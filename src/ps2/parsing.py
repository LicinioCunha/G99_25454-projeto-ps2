"""Interpretação (parsing) das linhas de largura fixa em objetos de domínio.

Cada campo é extraído por *slicing* (ETAPA 3 da aula). As posições abaixo
usam índices de Python (base 0). As posições em base 1 (como no enunciado)
estão indicadas em comentário.

Layout SIMPLIFICADO usado nos ficheiros de dados:

Cabeçalho (tipo 1)::

    [0]      tipo = '1'
    [1:9]    data AAAAMMDD              (pos 2-9)
    ...      nome empresa (largura variável)
    [-29:-20] NIF do ordenante          (9 dígitos)
    [-20:-6]  importância total         (14 dígitos, cêntimos)
    [-6:]     nº de registos            (6 dígitos)

Movimento (tipo 2)::

    [0]      tipo = '2'
    [1:11]   referência / ADC          (pos 2-11, 10 díg)
    [11:32]  NIB do cliente            (pos 12-32, 21 díg)
    [32:41]  referência auxiliar       (pos 33-41, 9 díg)
    [41:55]  importância               (pos 42-55, 14 díg, cêntimos)
    [55:]    descrição                 (pos 56-...)

Fim (tipo 9)::

    [0]      tipo = '9'
    [1:15]   importância total         (14 díg, cêntimos)
    [15:21]  nº de registos            (6 díg)
"""
from __future__ import annotations
from .modelo import RegistoInicio, RegistoMovimento, RegistoFim


def parse_inicio(linha: str) -> RegistoInicio:
    """Interpreta uma linha de cabeçalho (tipo 1)."""
    return RegistoInicio(
        data=linha[1:9],
        empresa=linha[9:-29].strip(),
        nif=linha[-29:-20],
        total_cent=int(linha[-20:-6]),
        n_registos=int(linha[-6:]),
    )


def parse_movimento(linha: str) -> RegistoMovimento:
    """Interpreta uma linha de movimento (tipo 2)."""
    return RegistoMovimento(
        referencia=linha[1:11],
        nib=linha[11:32],
        importancia_cent=int(linha[41:55]),
        descricao=linha[55:].strip(),
    )


def parse_fim(linha: str) -> RegistoFim:
    """Interpreta uma linha de fim (tipo 9)."""
    return RegistoFim(
        total_cent=int(linha[1:15]),
        n_registos=int(linha[15:21]),
    )
