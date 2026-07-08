"""Carregamento de alto nível: da pasta de dados para objetos :class:`Ficheiro`.

Junta leitura + parsing e devolve a lista de ficheiros já estruturados,
ignorando (mas assinalando) os que falham a validação de estrutura.
"""
from __future__ import annotations
from pathlib import Path
from .leitura import listar_ficheiros_ps2, ler_linhas
from .parsing import parse_inicio, parse_movimento, parse_fim
from .validacao import valida_estrutura
from .modelo import Ficheiro


def carregar_ficheiro(caminho: Path) -> Ficheiro:
    """Lê e estrutura um único ficheiro PS2."""
    linhas = ler_linhas(caminho)
    return Ficheiro(
        nome=caminho.name,
        inicio=parse_inicio(linhas[0]),
        movimentos=tuple(parse_movimento(l) for l in linhas[1:-1]),
        fim=parse_fim(linhas[-1]),
    )


def carregar_pasta(pasta: str = "./data") -> tuple[list[Ficheiro], list[str]]:
    """Carrega todos os ficheiros válidos de uma pasta.

    :return: par ``(ficheiros, avisos)`` onde ``avisos`` lista os problemas de
        estrutura encontrados (ficheiros com erro de estrutura não entram na
        lista de ficheiros carregados).
    """
    ficheiros: list[Ficheiro] = []
    avisos: list[str] = []
    for caminho in listar_ficheiros_ps2(pasta):
        erros = valida_estrutura(caminho.name, ler_linhas(caminho))
        if erros:
            avisos.extend(erros)
        else:
            ficheiros.append(carregar_ficheiro(caminho))
    return ficheiros, avisos
