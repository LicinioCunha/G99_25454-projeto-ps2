"""Modelo de domínio para os ficheiros PS2 (versão simplificada).

Define objetos imutáveis (`frozen=True`) que representam cada tipo de registo.
O uso de `dataclass` segue a ETAPA 5 da aula (criar objetos de domínio a partir
de texto).
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class RegistoInicio:
    """Registo de cabeçalho (tipo 1) — um por ficheiro."""
    data: str          # AAAAMMDD
    empresa: str       # nome do ordenante
    nif: str           # NIF do ordenante (9 dígitos)
    total_cent: int    # importância total em cêntimos
    n_registos: int    # nº de registos de movimento declarado


@dataclass(frozen=True)
class RegistoMovimento:
    """Registo de movimento (tipo 2) — um por cliente/operação."""
    referencia: str    # ref/ADC (10 dígitos)
    nib: str           # NIB do cliente (21 dígitos)
    importancia_cent: int
    descricao: str


@dataclass(frozen=True)
class RegistoFim:
    """Registo de fim/totalizador (tipo 9) — um por ficheiro."""
    total_cent: int
    n_registos: int


@dataclass(frozen=True)
class Ficheiro:
    """Ficheiro PS2 completo, já estruturado."""
    nome: str
    inicio: RegistoInicio
    movimentos: tuple[RegistoMovimento, ...]
    fim: RegistoFim
