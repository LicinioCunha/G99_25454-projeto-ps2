"""Listagem e leitura de ficheiros PS2 (ETAPAS 1 e 2 da aula).

Comunica com o sistema de ficheiros para descobrir e ler os `.ps2`,
sem depender de nomes escritos manualmente.
"""
from __future__ import annotations
from pathlib import Path
from typing import Iterator


def listar_ficheiros_ps2(pasta: str) -> list[Path]:
    """Devolve, ordenados, os caminhos dos ficheiros ``DD_*.ps2`` numa pasta.

    :param pasta: caminho da pasta (ex.: ``"./data"``).
    :return: lista de :class:`pathlib.Path`.
    """
    return sorted(Path(pasta).glob("DD_*.ps2"))


def ler_linhas(caminho: Path) -> list[str]:
    """Lê todas as linhas de um ficheiro, já sem o ``\\n`` final.

    Para ficheiros muito grandes pode preferir-se :func:`ler_linhas_lazy`.
    """
    with open(caminho, encoding="utf-8") as f:
        return [linha.rstrip("\n") for linha in f]


def ler_linhas_lazy(caminho: Path) -> Iterator[str]:
    """Versão com gerador — lê uma linha de cada vez (mais eficiente)."""
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            yield linha.rstrip("\n")
