"""Runner de linha de comandos: valida todos os ficheiros de ``./data``.

Uso::

    python src/main.py            # usa ./data
    python src/main.py ./data     # pasta explícita
"""
from __future__ import annotations
import sys
from ps2.leitura import listar_ficheiros_ps2, ler_linhas
from ps2.carregador import carregar_ficheiro
from ps2.validacao import valida_estrutura, valida_ficheiro


def main(pasta: str = "./data") -> None:
    ficheiros = listar_ficheiros_ps2(pasta)
    print(f"{len(ficheiros)} ficheiros encontrados em {pasta}\n")
    for cam in ficheiros:
        linhas = ler_linhas(cam)
        erros_estrutura = valida_estrutura(cam.name, linhas)
        erros_dados = valida_ficheiro(carregar_ficheiro(cam)) if not erros_estrutura else []
        estado = "OK" if not (erros_estrutura or erros_dados) else "ERROS"
        print(f"[{estado}] {cam.name}")
        for e in erros_estrutura + erros_dados:
            print(f"    - {e}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "./data")
