"""Testes (TDD — ETAPA da aula). Executar com: pytest"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ps2.validacao import valida_nif, so_numeros, data_valida


def test_so_numeros():
    assert so_numeros("1234")
    assert not so_numeros("12A4")


def test_data_valida():
    assert data_valida("20251026")
    assert not data_valida("20251340")


def test_valida_nif_exemplo_anexo_a():
    # exemplo do Anexo A: 501845923 é INVÁLIDO (dígito controlo devia ser 5, é 3)
    assert not valida_nif("501845923")


def test_valida_nif_valido():
    # 501442600 é um NIF com dígito de controlo correto
    assert valida_nif("501442600")
