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

    data: str
    """Data de processamento, formato ``AAAAMMDD``."""
    empresa: str
    """Nome da empresa ordenante."""
    nif: str
    """NIF da empresa ordenante (9 dígitos, ver Anexo A)."""
    total_cent: int
    """Importância total declarada, em cêntimos."""
    n_registos: int
    """Nº de registos de movimento declarado no cabeçalho."""


@dataclass(frozen=True)
class RegistoMovimento:
    """Registo de movimento (tipo 2) — um por cliente/operação."""

    referencia: str
    """Referência/ADC do movimento (10 dígitos)."""
    nib: str
    """NIB do cliente (21 dígitos, ver Anexo B)."""
    importancia_cent: int
    """Importância do movimento, em cêntimos."""
    descricao: str
    """Descrição livre do movimento (ex.: ``"Fatura Eletricidade 10/2025"``)."""


@dataclass(frozen=True)
class RegistoFim:
    """Registo de fim/totalizador (tipo 9) — um por ficheiro."""

    total_cent: int
    """Importância total repetida do cabeçalho, em cêntimos."""
    n_registos: int
    """Nº de registos de movimento repetido do cabeçalho."""


@dataclass(frozen=True)
class Ficheiro:
    """Ficheiro PS2 completo, já estruturado."""

    nome: str
    """Nome do ficheiro de origem (ex.: ``"DD_2025_10.ps2"``)."""
    inicio: RegistoInicio
    """Registo de cabeçalho (tipo 1)."""
    movimentos: tuple[RegistoMovimento, ...]
    """Registos de movimento (tipo 2), um por cliente/operação."""
    fim: RegistoFim
    """Registo de fim/totalizador (tipo 9)."""
