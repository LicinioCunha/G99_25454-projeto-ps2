"""Testes de parsing das linhas de largura fixa. Executar com: pytest"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ps2.parsing import parse_inicio, parse_movimento, parse_fim

LINHA_INICIO = "120251026IPCA Energy                   50123456700000000045375000002"
LINHA_MOVIMENTO = "2000000100100350651000025874125423568914200000000024750Fatura Eletricidade 10/2025"
LINHA_FIM = "900000000045375000002"


def test_parse_inicio():
    r = parse_inicio(LINHA_INICIO)
    assert r.data == "20251026"
    assert r.empresa == "IPCA Energy"
    assert r.nif == "501234567"
    assert r.total_cent == 45375
    assert r.n_registos == 2


def test_parse_movimento():
    r = parse_movimento(LINHA_MOVIMENTO)
    assert r.referencia == "0000001001"
    assert r.nib == "003506510000258741254"
    assert len(r.nib) == 21
    assert r.importancia_cent == 24750
    assert r.descricao == "Fatura Eletricidade 10/2025"


def test_parse_fim():
    r = parse_fim(LINHA_FIM)
    assert r.total_cent == 45375
    assert r.n_registos == 2
