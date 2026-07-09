"""Teste de integração: carregar a pasta ./data completa. Executar com: pytest"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ps2.carregador import carregar_pasta

DATA_DIR = str(Path(__file__).resolve().parent.parent / "data")


def test_carregar_pasta_sem_erros_de_estrutura():
    ficheiros, avisos = carregar_pasta(DATA_DIR)
    assert avisos == []
    assert len(ficheiros) == 35


def test_carregar_pasta_ficheiros_tem_movimentos():
    ficheiros, _ = carregar_pasta(DATA_DIR)
    assert all(len(f.movimentos) == f.fim.n_registos for f in ficheiros)
