"""Testes das funções de agregação. Executar com: pytest"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ps2.modelo import Ficheiro, RegistoInicio, RegistoMovimento, RegistoFim
from ps2 import agregacao as ag

NIB_A = "003506510000258741254"
NIB_B = "003300004521087459615"


def _ficheiro(ano_mes: str, nif: str, valores: list[tuple[str, int]]) -> Ficheiro:
    movimentos = tuple(
        RegistoMovimento(referencia="0000000001", nib=nib,
                          importancia_cent=cent, descricao="teste")
        for nib, cent in valores
    )
    total = sum(cent for _, cent in valores)
    ano, mes = ano_mes.split("-")
    return Ficheiro(
        nome=f"DD_{ano}_{mes}.ps2",
        inicio=RegistoInicio(data=f"{ano}{mes}01", empresa="Teste", nif=nif,
                              total_cent=total, n_registos=len(valores)),
        movimentos=movimentos,
        fim=RegistoFim(total_cent=total, n_registos=len(valores)),
    )


def _dados():
    return [
        _ficheiro("2025-01", "501234567", [(NIB_A, 1000), (NIB_B, 2000)]),
        _ficheiro("2025-02", "501442600", [(NIB_A, 1500)]),
    ]


def test_periodo():
    assert ag.periodo(_dados()[0]) == "2025-01"


def test_total_por_mes():
    tot = ag.total_por_mes(_dados())
    assert tot == {"2025-01": 30.0, "2025-02": 15.0}


def test_total_por_cliente():
    tot = ag.total_por_cliente(_dados())
    assert tot[NIB_A] == 25.0
    assert tot[NIB_B] == 20.0


def test_serie_cliente():
    serie = ag.serie_cliente(_dados(), NIB_A)
    assert serie == {"2025-01": 10.0, "2025-02": 15.0}


def test_clientes():
    assert ag.clientes(_dados()) == sorted([NIB_A, NIB_B])


def test_resumo_alertas():
    resumo = ag.resumo_alertas(_dados())
    assert len(resumo) == 2
    primeiro = resumo[0]
    assert primeiro["periodo"] == "2025-01"
    assert primeiro["nif_valido"] is False   # 501234567 falha o dígito de controlo
    assert primeiro["n_movimentos"] == 2
    assert primeiro["n_nibs_invalidos"] == 2  # NIB_A e NIB_B falham a regra do Anexo B
