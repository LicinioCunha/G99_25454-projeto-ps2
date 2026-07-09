"""Testes (TDD — ETAPA da aula). Executar com: pytest"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ps2.validacao import valida_nif, valida_nib, valida_estrutura, so_numeros, data_valida


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


def test_valida_nif_primeiro_digito_invalido():
    # primeiro dígito tem de pertencer a {1,2,5,6,8,9}
    assert not valida_nif("301442600")


def test_valida_nif_tamanho_ou_formato_invalido():
    assert not valida_nif("50144260")       # só 8 dígitos
    assert not valida_nif("5014426AB")      # tem letras


def test_valida_nib_exemplo_anexo_b():
    # exemplo do Anexo B: o enunciado afirma que o resto é 1, mas
    # 003506510000258741254 mod 97 == 96 — o próprio exemplo do anexo
    # não passa na regra literal (ver nota no README).
    assert int("003506510000258741254") % 97 == 96
    assert not valida_nib("003506510000258741254")


def test_valida_nib_formato_invalido():
    assert not valida_nib("12345")                  # tamanho errado
    assert not valida_nib("00350651000025874125A")   # tem letra


def test_valida_estrutura_ficheiro_valido():
    linhas = [
        "120251026IPCA Energy                   50123456700000000045375000002",
        "2000000100100350651000025874125423568914200000000024750Fatura Eletricidade 10/2025",
        "2000000100200330000452108745961550184592300000000020625Fatura Eletricidade 10/2025",
        "900000000045375000002",
    ]
    assert valida_estrutura("exemplo.ps2", linhas) == []


def test_valida_estrutura_totais_nao_coincidem():
    linhas = [
        "120251026IPCA Energy                   50123456700000000099999000002",
        "2000000100100350651000025874125423568914200000000024750Fatura Eletricidade 10/2025",
        "2000000100200330000452108745961550184592300000000020625Fatura Eletricidade 10/2025",
        "900000000045375000002",
    ]
    erros = valida_estrutura("exemplo.ps2", linhas)
    assert any("totais não coincidem" in e for e in erros)


def test_valida_estrutura_primeiro_registo_invalido():
    linhas = [
        "220251026IPCA Energy                   50123456700000000045375000002",
        "2000000100100350651000025874125423568914200000000024750Fatura Eletricidade 10/2025",
        "900000000045375000002",
    ]
    erros = valida_estrutura("exemplo.ps2", linhas)
    assert any("primeira linha não é registo tipo 1" in e for e in erros)
