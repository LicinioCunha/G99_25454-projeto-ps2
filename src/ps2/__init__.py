"""Pacote ``ps2``: leitura, validação e agregação de ficheiros de débitos diretos.

Cada módulo tem uma única responsabilidade:

- :mod:`ps2.leitura` — listar e ler ficheiros ``.ps2`` do disco.
- :mod:`ps2.modelo` — objetos de domínio imutáveis (``dataclasses``).
- :mod:`ps2.parsing` — interpretar linhas de largura fixa em objetos de domínio.
- :mod:`ps2.validacao` — validar estrutura, NIF (Anexo A) e NIB (Anexo B).
- :mod:`ps2.agregacao` — agregações para o dashboard (totais, alertas).
- :mod:`ps2.carregador` — combina leitura + parsing + validação de alto nível.
"""
